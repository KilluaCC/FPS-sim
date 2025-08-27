const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

// Database service class for FPS Estimator
class DatabaseService {
  constructor() {
    this.prisma = prisma;
  }

  // Get all available data for dropdowns
  async getAllData() {
    try {
      const [gpus, cpus, games, rams] = await Promise.all([
        this.prisma.gpu.findMany({
          select: {
            id: true,
            name: true,
            tier: true,
            brand: true,
            vramGb: true,
            priceUsd: true
          },
          orderBy: { tier: 'asc' }
        }),
        this.prisma.cpu.findMany({
          select: {
            id: true,
            name: true,
            tier: true,
            brand: true,
            cores: true,
            threads: true,
            priceUsd: true
          },
          orderBy: { tier: 'asc' }
        }),
        this.prisma.game.findMany({
          select: {
            id: true,
            name: true,
            genre: true,
            gpuIntensive: true,
            cpuIntensive: true,
            rayTracingSupport: true
          },
          orderBy: { name: 'asc' }
        }),
        this.prisma.ram.findMany({
          select: {
            id: true,
            sizeGb: true,
            speedMhz: true,
            type: true,
            brand: true,
            priceUsd: true
          },
          orderBy: { speedMhz: 'desc' }
        })
      ]);

      // Static data that doesn't need to be in database
      const resolutions = [
        { id: '1080p', name: '1920x1080 (1080p)', multiplier: 1.0 },
        { id: '1440p', name: '2560x1440 (1440p)', multiplier: 1.78 },
        { id: '4K', name: '3840x2160 (4K)', multiplier: 4.0 }
      ];

      const settings = [
        { id: 'Low', name: 'Low', multiplier: 1.0 },
        { id: 'Medium', name: 'Medium', multiplier: 0.7 },
        { id: 'High', name: 'High', multiplier: 0.5 },
        { id: 'Ultra', name: 'Ultra', multiplier: 0.3 }
      ];

      return {
        gpus: gpus.map(gpu => ({ 
          id: gpu.id.toString(), 
          name: gpu.name, 
          tier: gpu.tier,
          brand: gpu.brand,
          vram: gpu.vramGb,
          price: gpu.priceUsd
        })),
        cpus: cpus.map(cpu => ({ 
          id: cpu.id.toString(), 
          name: cpu.name, 
          tier: cpu.tier,
          brand: cpu.brand,
          cores: cpu.cores,
          threads: cpu.threads,
          price: cpu.priceUsd
        })),
        games: games.map(game => ({ 
          id: game.id.toString(), 
          name: game.name, 
          genre: game.genre,
          gpuIntensive: game.gpuIntensive,
          cpuIntensive: game.cpuIntensive,
          rayTracingSupport: game.rayTracingSupport
        })),
        rams: rams.map(ram => ({ 
          id: ram.id.toString(), 
          size: ram.sizeGb,
          speed: ram.speedMhz,
          type: ram.type,
          brand: ram.brand,
          price: ram.priceUsd
        })),
        resolutions,
        settings
      };
    } catch (error) {
      console.error('Database error in getAllData:', error);
      throw new Error('Failed to fetch data from database');
    }
  }

  // Get FPS estimate from database or calculate estimated
  async getFPSEstimate(gpuId, cpuId, gameId, resolution, settings) {
    try {
      // First, try to find an exact match in benchmarks
      const benchmark = await this.prisma.benchmark.findFirst({
        where: {
          gpuId: parseInt(gpuId),
          cpuId: parseInt(cpuId),
          gameId: parseInt(gameId),
          resolution,
          settings
        },
        include: {
          gpu: true,
          cpu: true,
          game: true,
          ram: true
        }
      });

      if (benchmark) {
        // Return real benchmark data
        return {
          avgFPS: parseFloat(benchmark.avgFps),
          minFPS: parseFloat(benchmark.minFps || benchmark.avgFps * 0.85),
          maxFPS: parseFloat(benchmark.maxFps || benchmark.avgFps * 1.15),
          source: 'database',
          benchmarkId: benchmark.id,
          components: {
            gpu: { id: benchmark.gpu.id.toString(), name: benchmark.gpu.name, tier: benchmark.gpu.tier },
            cpu: { id: benchmark.cpu.id.toString(), name: benchmark.cpu.name, tier: benchmark.cpu.tier },
            game: { id: benchmark.game.id.toString(), name: benchmark.game.name, genre: benchmark.game.genre },
            ram: { id: benchmark.ram.id.toString(), size: benchmark.ram.sizeGb, speed: benchmark.ram.speedMhz },
            resolution,
            settings
          }
        };
      }

      // If no exact match, calculate estimated FPS
      return await this.calculateEstimatedFPS(gpuId, cpuId, gameId, resolution, settings);
    } catch (error) {
      console.error('Database error in getFPSEstimate:', error);
      throw new Error('Failed to get FPS estimate');
    }
  }

  // Calculate estimated FPS when no benchmark exists
  async calculateEstimatedFPS(gpuId, cpuId, gameId, resolution, settings) {
    try {
      const [gpu, cpu, game] = await Promise.all([
        this.prisma.gpu.findUnique({ where: { id: parseInt(gpuId) } }),
        this.prisma.cpu.findUnique({ where: { id: parseInt(cpuId) } }),
        this.prisma.game.findUnique({ where: { id: parseInt(gameId) } })
      ]);

      if (!gpu || !cpu || !game) {
        throw new Error('Invalid hardware or game specified');
      }

      // Get resolution and settings multipliers
      const resolutionMultipliers = { '1080p': 1.0, '1440p': 1.78, '4K': 4.0 };
      const settingsMultipliers = { 'Low': 1.0, 'Medium': 0.7, 'High': 0.5, 'Ultra': 0.3 };

      const resolutionMultiplier = resolutionMultipliers[resolution] || 1.0;
      const settingsMultiplier = settingsMultipliers[settings] || 1.0;

      // Base FPS calculation based on GPU tier and game requirements
      const gpuTierScores = { 'flagship': 100, 'high-end': 85, 'mid-high': 70, 'mid': 55, 'budget': 40 };
      const cpuTierScores = { 'flagship': 100, 'high-end': 85, 'mid-high': 70, 'mid': 55, 'budget': 40 };

      const gpuScore = gpuTierScores[gpu.tier] || 50;
      const cpuScore = cpuTierScores[cpu.tier] || 50;

      // Game intensity factors
      let gameIntensity = 1.0;
      if (game.gpuIntensive && game.cpuIntensive) gameIntensity = 0.8;
      else if (game.gpuIntensive) gameIntensity = 0.9;
      else if (game.cpuIntensive) gameIntensity = 0.95;

      // Calculate base FPS
      let baseFPS = (gpuScore * 0.7 + cpuScore * 0.3) * gameIntensity;

      // Apply resolution and settings multipliers
      let estimatedFPS = baseFPS / (resolutionMultiplier * settingsMultiplier);

      // Ensure reasonable FPS range
      estimatedFPS = Math.max(30, Math.min(300, estimatedFPS));

      // Calculate min/max with variance
      const variance = 0.15;
      const minFPS = estimatedFPS * (1 - variance);
      const maxFPS = estimatedFPS * (1 + variance);

      // Determine bottleneck
      let bottleneck = 'balanced';
      if (gpuScore < cpuScore * 0.8) bottleneck = 'gpu';
      else if (cpuScore < gpuScore * 0.8) bottleneck = 'cpu';

      return {
        avgFPS: Math.round(estimatedFPS),
        minFPS: Math.round(minFPS),
        maxFPS: Math.round(maxFPS),
        source: 'estimated',
        bottleneck,
        components: {
          gpu: { id: gpu.id.toString(), name: gpu.name, tier: gpu.tier },
          cpu: { id: cpu.id.toString(), name: cpu.name, tier: cpu.tier },
          game: { id: game.id.toString(), name: game.name, genre: game.genre },
          resolution,
          settings
        }
      };
    } catch (error) {
      console.error('Error calculating estimated FPS:', error);
      throw new Error('Failed to calculate FPS estimate');
    }
  }

  // Get detailed component information
  async getComponentDetails(type, id) {
    try {
      let component = null;
      
      switch (type) {
        case 'gpu':
          component = await this.prisma.gpu.findUnique({
            where: { id: parseInt(id) },
            include: { benchmarks: { take: 5, include: { game: true } } }
          });
          break;
        case 'cpu':
          component = await this.prisma.cpu.findUnique({
            where: { id: parseInt(id) },
            include: { benchmarks: { take: 5, include: { game: true } } }
          });
          break;
        case 'game':
          component = await this.prisma.game.findUnique({
            where: { id: parseInt(id) },
            include: { benchmarks: { take: 5, include: { gpu: true, cpu: true } } }
          });
          break;
        case 'ram':
          component = await this.prisma.ram.findUnique({
            where: { id: parseInt(id) }
          });
          break;
        default:
          throw new Error('Invalid component type');
      }

      if (!component) {
        throw new Error('Component not found');
      }

      return component;
    } catch (error) {
      console.error('Database error in getComponentDetails:', error);
      throw new Error('Failed to fetch component details');
    }
  }

  // Submit user FPS data for crowd-sourcing
  async submitUserFPS(data) {
    try {
      const { gpuId, cpuId, gameId, resolution, settings, avgFps, minFps, maxFps, userId, notes } = data;

      // Find or create benchmark record
      let benchmark = await this.prisma.benchmark.findFirst({
        where: {
          gpuId: parseInt(gpuId),
          cpuId: parseInt(cpuId),
          gameId: parseInt(gameId),
          resolution,
          settings
        }
      });

      if (!benchmark) {
        // Create new benchmark if it doesn't exist
        benchmark = await this.prisma.benchmark.create({
          data: {
            gpuId: parseInt(gpuId),
            cpuId: parseInt(cpuId),
            gameId: parseInt(gameId),
            ramId: 1, // Default RAM ID
            resolution,
            settings,
            avgFps: avgFps,
            minFps: minFps || avgFps * 0.85,
            maxFps: maxFps || avgFps * 1.15,
            source: 'community'
          }
        });
      }

      // Create user submission
      const submission = await this.prisma.userSubmission.create({
        data: {
          benchmarkId: benchmark.id,
          userId: userId || 'anonymous',
          avgFps: avgFps,
          minFps: minFps,
          maxFps: maxFps,
          notes: notes,
          confidenceRating: 4, // Default confidence
          hardwareMatch: true
        }
      });

      return {
        success: true,
        submissionId: submission.id,
        benchmarkId: benchmark.id,
        message: 'FPS submission recorded successfully'
      };
    } catch (error) {
      console.error('Database error in submitUserFPS:', error);
      throw new Error('Failed to submit FPS data');
    }
  }

  // Get performance statistics
  async getPerformanceStats() {
    try {
      const stats = await this.prisma.benchmark.groupBy({
        by: ['gpuId', 'cpuId'],
        _count: { id: true },
        _avg: { avgFps: true },
        _min: { avgFps: true },
        _max: { avgFps: true }
      });

      return stats.map(stat => ({
        gpuId: stat.gpuId,
        cpuId: stat.cpuId,
        benchmarkCount: stat._count.id,
        avgFPS: parseFloat(stat._avg.avgFps || 0),
        minFPS: parseFloat(stat._min.avgFps || 0),
        maxFPS: parseFloat(stat._max.avgFps || 0)
      }));
    } catch (error) {
      console.error('Database error in getPerformanceStats:', error);
      throw new Error('Failed to fetch performance statistics');
    }
  }

  // Health check
  async healthCheck() {
    try {
      await this.prisma.$queryRaw`SELECT 1`;
      return { status: 'healthy', database: 'connected' };
    } catch (error) {
      return { status: 'unhealthy', database: 'disconnected', error: error.message };
    }
  }

  // Close database connection
  async disconnect() {
    await this.prisma.$disconnect();
  }
}

module.exports = new DatabaseService();

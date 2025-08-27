const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

// Sample benchmark data to add
const benchmarks = [
  // RTX 4090 + i9-14900K combinations
  {
    gpuId: 1, cpuId: 3, gameId: 2, ramId: 1, resolution: '1080p', settings: 'Ultra',
    avgFps: 180, minFps: 155, maxFps: 210, notes: 'RTX 4090 + i9-14900K, Minecraft RTX, 1080p Ultra'
  },
  {
    gpuId: 1, cpuId: 3, gameId: 4, ramId: 1, resolution: '1080p', settings: 'Ultra',
    avgFps: 165, minFps: 142, maxFps: 188, notes: 'RTX 4090 + i9-14900K, Fortnite RTX, 1080p Ultra'
  },
  {
    gpuId: 1, cpuId: 3, gameId: 10, ramId: 1, resolution: '1080p', settings: 'High',
    avgFps: 195, minFps: 168, maxFps: 220, notes: 'RTX 4090 + i9-14900K, Warzone, 1080p High'
  },
  
  // RTX 4080 + i7-14700K combinations
  {
    gpuId: 2, cpuId: 2, gameId: 1, ramId: 1, resolution: '1080p', settings: 'Ultra',
    avgFps: 98, minFps: 82, maxFps: 115, notes: 'RTX 4080 + i7-14700K, Cyberpunk 2077, 1080p Ultra'
  },
  {
    gpuId: 2, cpuId: 2, gameId: 4, ramId: 1, resolution: '1080p', settings: 'High',
    avgFps: 142, minFps: 125, maxFps: 165, notes: 'RTX 4080 + i7-14700K, Fortnite, 1080p High'
  },
  
  // RTX 4070 + i5-14600K combinations
  {
    gpuId: 3, cpuId: 1, gameId: 1, ramId: 1, resolution: '1080p', settings: 'High',
    avgFps: 67, minFps: 58, maxFps: 78, notes: 'RTX 4070 + i5-14600K, Cyberpunk 2077, 1080p High'
  },
  {
    gpuId: 3, cpuId: 1, gameId: 5, ramId: 1, resolution: '1080p', settings: 'Ultra',
    avgFps: 185, minFps: 165, maxFps: 210, notes: 'RTX 4070 + i5-14600K, CS2, 1080p Ultra'
  },
  
  // AMD combinations
  {
    gpuId: 6, cpuId: 7, gameId: 1, ramId: 1, resolution: '1080p', settings: 'Ultra',
    avgFps: 134, minFps: 118, maxFps: 152, notes: 'RX 7900 XTX + Ryzen 9 7950X3D, Cyberpunk 2077, 1080p Ultra'
  },
  {
    gpuId: 5, cpuId: 5, gameId: 4, ramId: 1, resolution: '1080p', settings: 'High',
    avgFps: 128, minFps: 112, maxFps: 145, notes: 'RX 7800 XT + Ryzen 7 7800X3D, Fortnite, 1080p High'
  }
];

async function addBenchmarks() {
  try {
    console.log('🚀 Adding benchmark data...');
    
    for (const benchmark of benchmarks) {
      // Check if benchmark already exists
      const existing = await prisma.benchmark.findFirst({
        where: {
          gpuId: benchmark.gpuId,
          cpuId: benchmark.cpuId,
          gameId: benchmark.gameId,
          resolution: benchmark.resolution,
          settings: benchmark.settings
        }
      });
      
      if (existing) {
        console.log(`⚠️  Benchmark already exists: ${benchmark.notes}`);
        continue;
      }
      
      // Add new benchmark
      const result = await prisma.benchmark.create({
        data: {
          gpuId: benchmark.gpuId,
          cpuId: benchmark.cpuId,
          gameId: benchmark.gameId,
          ramId: benchmark.ramId,
          resolution: benchmark.resolution,
          settings: benchmark.settings,
          avgFps: benchmark.avgFps,
          minFps: benchmark.minFps,
          maxFps: benchmark.maxFps,
          source: 'community'
        }
      });
      
      console.log(`✅ Added: ${benchmark.notes}`);
    }
    
    console.log('\n🎉 Benchmark data addition complete!');
    
    // Show summary
    const totalBenchmarks = await prisma.benchmark.count();
    console.log(`📊 Total benchmarks in database: ${totalBenchmarks}`);
    
  } catch (error) {
    console.error('❌ Error adding benchmarks:', error);
  } finally {
    await prisma.$disconnect();
  }
}

addBenchmarks();
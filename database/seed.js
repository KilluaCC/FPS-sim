const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seeding...');

  // Clear existing data
  console.log('🧹 Clearing existing data...');
  await prisma.userSubmission.deleteMany();
  await prisma.benchmark.deleteMany();
  await prisma.game.deleteMany();
  await prisma.ram.deleteMany();
  await prisma.gpu.deleteMany();
  await prisma.cpu.deleteMany();

  // Seed CPUs
  console.log('🖥️ Seeding CPUs...');
  const cpus = await Promise.all([
    prisma.cpu.create({
      data: {
        name: 'Intel Core i9-14900K',
        brand: 'Intel',
        cores: 24,
        threads: 32,
        baseClock: 3.20,
        boostClock: 6.00,
        tdp: 253,
        releaseDate: new Date('2023-10-17'),
        tier: 'flagship',
        priceUsd: 589.99,
        socket: 'LGA1700',
        architecture: 'Raptor Lake Refresh'
      }
    }),
    prisma.cpu.create({
      data: {
        name: 'Intel Core i7-14700K',
        brand: 'Intel',
        cores: 20,
        threads: 28,
        baseClock: 3.40,
        boostClock: 5.60,
        tdp: 253,
        releaseDate: new Date('2023-10-17'),
        tier: 'high-end',
        priceUsd: 409.99,
        socket: 'LGA1700',
        architecture: 'Raptor Lake Refresh'
      }
    }),
    prisma.cpu.create({
      data: {
        name: 'Intel Core i5-14600K',
        brand: 'Intel',
        cores: 14,
        threads: 20,
        baseClock: 3.50,
        boostClock: 5.30,
        tdp: 181,
        releaseDate: new Date('2023-10-17'),
        tier: 'mid-high',
        priceUsd: 319.99,
        socket: 'LGA1700',
        architecture: 'Raptor Lake Refresh'
      }
    }),
    prisma.cpu.create({
      data: {
        name: 'Intel Core i5-12400F',
        brand: 'Intel',
        cores: 6,
        threads: 12,
        baseClock: 2.50,
        boostClock: 4.40,
        tdp: 65,
        releaseDate: new Date('2022-01-04'),
        tier: 'mid',
        priceUsd: 179.99,
        socket: 'LGA1700',
        architecture: 'Alder Lake'
      }
    }),
    prisma.cpu.create({
      data: {
        name: 'AMD Ryzen 9 7950X3D',
        brand: 'AMD',
        cores: 16,
        threads: 32,
        baseClock: 4.20,
        boostClock: 5.70,
        tdp: 120,
        releaseDate: new Date('2023-02-28'),
        tier: 'flagship',
        priceUsd: 699.99,
        socket: 'AM5',
        architecture: 'Zen 4'
      }
    }),
    prisma.cpu.create({
      data: {
        name: 'AMD Ryzen 7 7800X3D',
        brand: 'AMD',
        cores: 8,
        threads: 16,
        baseClock: 4.20,
        boostClock: 5.00,
        tdp: 120,
        releaseDate: new Date('2023-04-06'),
        tier: 'high-end',
        priceUsd: 449.99,
        socket: 'AM5',
        architecture: 'Zen 4'
      }
    }),
    prisma.cpu.create({
      data: {
        name: 'AMD Ryzen 5 7600X',
        brand: 'AMD',
        cores: 6,
        threads: 12,
        baseClock: 4.70,
        boostClock: 5.30,
        tdp: 105,
        releaseDate: new Date('2022-09-27'),
        tier: 'mid-high',
        priceUsd: 299.99,
        socket: 'AM5',
        architecture: 'Zen 4'
      }
    }),
    prisma.cpu.create({
      data: {
        name: 'AMD Ryzen 5 5600',
        brand: 'AMD',
        cores: 6,
        threads: 12,
        baseClock: 3.50,
        boostClock: 4.40,
        tdp: 65,
        releaseDate: new Date('2022-04-04'),
        tier: 'mid',
        priceUsd: 159.99,
        socket: 'AM4',
        architecture: 'Zen 3'
      }
    })
  ]);

  // Seed GPUs
  console.log('🎮 Seeding GPUs...');
  const gpus = await Promise.all([
    prisma.gpu.create({
      data: {
        name: 'NVIDIA RTX 4090',
        brand: 'NVIDIA',
        vramGb: 24,
        baseClock: 2235,
        boostClock: 2520,
        tdp: 450,
        releaseDate: new Date('2022-10-12'),
        tier: 'flagship',
        priceUsd: 1599.99,
        memoryType: 'GDDR6X',
        memoryBusWidth: 384,
        rayTracingCores: 144,
        tensorCores: 576
      }
    }),
    prisma.gpu.create({
      data: {
        name: 'NVIDIA RTX 4080',
        brand: 'NVIDIA',
        vramGb: 16,
        baseClock: 2205,
        boostClock: 2505,
        tdp: 320,
        releaseDate: new Date('2022-11-16'),
        tier: 'high-end',
        priceUsd: 1199.99,
        memoryType: 'GDDR6X',
        memoryBusWidth: 256,
        rayTracingCores: 76,
        tensorCores: 304
      }
    }),
    prisma.gpu.create({
      data: {
        name: 'NVIDIA RTX 4070 Ti',
        brand: 'NVIDIA',
        vramGb: 12,
        baseClock: 2310,
        boostClock: 2610,
        tdp: 285,
        releaseDate: new Date('2023-01-05'),
        tier: 'high-end',
        priceUsd: 799.99,
        memoryType: 'GDDR6X',
        memoryBusWidth: 192,
        rayTracingCores: 60,
        tensorCores: 240
      }
    }),
    prisma.gpu.create({
      data: {
        name: 'NVIDIA RTX 4070',
        brand: 'NVIDIA',
        vramGb: 12,
        baseClock: 1980,
        boostClock: 2475,
        tdp: 200,
        releaseDate: new Date('2023-04-13'),
        tier: 'mid-high',
        priceUsd: 599.99,
        memoryType: 'GDDR6X',
        memoryBusWidth: 192,
        rayTracingCores: 46,
        tensorCores: 184
      }
    }),
    prisma.gpu.create({
      data: {
        name: 'NVIDIA RTX 4060 Ti',
        brand: 'NVIDIA',
        vramGb: 8,
        baseClock: 2310,
        boostClock: 2535,
        tdp: 160,
        releaseDate: new Date('2023-05-24'),
        tier: 'mid',
        priceUsd: 399.99,
        memoryType: 'GDDR6',
        memoryBusWidth: 128,
        rayTracingCores: 32,
        tensorCores: 128
      }
    }),
    prisma.gpu.create({
      data: {
        name: 'AMD RX 7900 XTX',
        brand: 'AMD',
        vramGb: 24,
        baseClock: 1500,
        boostClock: 2500,
        tdp: 355,
        releaseDate: new Date('2022-12-13'),
        tier: 'flagship',
        priceUsd: 999.99,
        memoryType: 'GDDR6',
        memoryBusWidth: 384,
        rayTracingCores: 96,
        tensorCores: 192
      }
    }),
    prisma.gpu.create({
      data: {
        name: 'AMD RX 7900 XT',
        brand: 'AMD',
        vramGb: 20,
        baseClock: 1500,
        boostClock: 2400,
        tdp: 315,
        releaseDate: new Date('2022-12-13'),
        tier: 'high-end',
        priceUsd: 899.99,
        memoryType: 'GDDR6',
        memoryBusWidth: 320,
        rayTracingCores: 84,
        tensorCores: 168
      }
    }),
    prisma.gpu.create({
      data: {
        name: 'AMD RX 7800 XT',
        brand: 'AMD',
        vramGb: 16,
        baseClock: 1295,
        boostClock: 2430,
        tdp: 263,
        releaseDate: new Date('2023-09-06'),
        tier: 'high-end',
        priceUsd: 499.99,
        memoryType: 'GDDR6',
        memoryBusWidth: 256,
        rayTracingCores: 60,
        tensorCores: 120
      }
    }),
    prisma.gpu.create({
      data: {
        name: 'AMD RX 7700 XT',
        brand: 'AMD',
        vramGb: 12,
        baseClock: 1900,
        boostClock: 2544,
        tdp: 245,
        releaseDate: new Date('2023-09-06'),
        tier: 'mid-high',
        priceUsd: 449.99,
        memoryType: 'GDDR6',
        memoryBusWidth: 192,
        rayTracingCores: 48,
        tensorCores: 96
      }
    }),
    prisma.gpu.create({
      data: {
        name: 'AMD RX 7600',
        brand: 'AMD',
        vramGb: 8,
        baseClock: 1720,
        boostClock: 2655,
        tdp: 165,
        releaseDate: new Date('2023-05-25'),
        tier: 'mid',
        priceUsd: 269.99,
        memoryType: 'GDDR6',
        memoryBusWidth: 128,
        rayTracingCores: 32,
        tensorCores: 64
      }
    })
  ]);

  // Seed RAM
  console.log('💾 Seeding RAM...');
  const rams = await Promise.all([
    prisma.ram.create({
      data: {
        sizeGb: 32,
        speedMhz: 6000,
        type: 'DDR5',
        brand: 'Corsair',
        model: 'Vengeance RGB',
        casLatency: 36,
        voltage: 1.35,
        priceUsd: 129.99
      }
    }),
    prisma.ram.create({
      data: {
        sizeGb: 32,
        speedMhz: 5600,
        type: 'DDR5',
        brand: 'G.Skill',
        model: 'Trident Z5',
        casLatency: 36,
        voltage: 1.25,
        priceUsd: 119.99
      }
    }),
    prisma.ram.create({
      data: {
        sizeGb: 16,
        speedMhz: 6000,
        type: 'DDR5',
        brand: 'Corsair',
        model: 'Vengeance',
        casLatency: 36,
        voltage: 1.35,
        priceUsd: 69.99
      }
    }),
    prisma.ram.create({
      data: {
        sizeGb: 16,
        speedMhz: 3600,
        type: 'DDR4',
        brand: 'Corsair',
        model: 'Vengeance LPX',
        casLatency: 18,
        voltage: 1.35,
        priceUsd: 59.99
      }
    }),
    prisma.ram.create({
      data: {
        sizeGb: 32,
        speedMhz: 3600,
        type: 'DDR4',
        brand: 'G.Skill',
        model: 'Ripjaws V',
        casLatency: 18,
        voltage: 1.35,
        priceUsd: 99.99
      }
    })
  ]);

  // Seed Games
  console.log('🎯 Seeding Games...');
  const games = await Promise.all([
    prisma.game.create({
      data: {
        name: 'Cyberpunk 2077',
        genre: 'RPG',
        releaseDate: new Date('2020-12-10'),
        developer: 'CD Projekt Red',
        publisher: 'CD Projekt',
        engine: 'REDengine 4',
        gpuIntensive: true,
        cpuIntensive: true,
        ramIntensive: true,
        rayTracingSupport: true,
        dlssSupport: true,
        fsrSupport: true
      }
    }),
    prisma.game.create({
      data: {
        name: 'Red Dead Redemption 2',
        genre: 'Action-Adventure',
        releaseDate: new Date('2019-12-05'),
        developer: 'Rockstar Games',
        publisher: 'Rockstar Games',
        engine: 'RAGE',
        gpuIntensive: true,
        cpuIntensive: false,
        ramIntensive: true,
        rayTracingSupport: false,
        dlssSupport: false,
        fsrSupport: false
      }
    }),
    prisma.game.create({
      data: {
        name: 'Microsoft Flight Simulator',
        genre: 'Simulation',
        releaseDate: new Date('2020-08-18'),
        developer: 'Asobo Studio',
        publisher: 'Xbox Game Studios',
        engine: 'Asobo Engine',
        gpuIntensive: true,
        cpuIntensive: true,
        ramIntensive: true,
        rayTracingSupport: false,
        dlssSupport: true,
        fsrSupport: false
      }
    }),
    prisma.game.create({
      data: {
        name: 'Assassin\'s Creed Valhalla',
        genre: 'Action-RPG',
        releaseDate: new Date('2020-11-10'),
        developer: 'Ubisoft',
        publisher: 'Ubisoft',
        engine: 'AnvilNext 2.0',
        gpuIntensive: true,
        cpuIntensive: false,
        ramIntensive: true,
        rayTracingSupport: false,
        dlssSupport: true,
        fsrSupport: true
      }
    }),
    prisma.game.create({
      data: {
        name: 'Call of Duty: Warzone',
        genre: 'Battle Royale',
        releaseDate: new Date('2020-03-10'),
        developer: 'Infinity Ward',
        publisher: 'Activision',
        engine: 'IW Engine',
        gpuIntensive: true,
        cpuIntensive: true,
        ramIntensive: false,
        rayTracingSupport: false,
        dlssSupport: true,
        fsrSupport: false
      }
    }),
    prisma.game.create({
      data: {
        name: 'Fortnite',
        genre: 'Battle Royale',
        releaseDate: new Date('2017-07-25'),
        developer: 'Epic Games',
        publisher: 'Epic Games',
        engine: 'Unreal Engine 5',
        gpuIntensive: true,
        cpuIntensive: false,
        ramIntensive: false,
        rayTracingSupport: true,
        dlssSupport: true,
        fsrSupport: true
      }
    }),
    prisma.game.create({
      data: {
        name: 'Minecraft',
        genre: 'Sandbox',
        releaseDate: new Date('2011-11-18'),
        developer: 'Mojang Studios',
        publisher: 'Mojang Studios',
        engine: 'Custom Java',
        gpuIntensive: false,
        cpuIntensive: true,
        ramIntensive: true,
        rayTracingSupport: true,
        dlssSupport: false,
        fsrSupport: false
      }
    }),
    prisma.game.create({
      data: {
        name: 'Counter-Strike 2',
        genre: 'FPS',
        releaseDate: new Date('2023-09-27'),
        developer: 'Valve',
        publisher: 'Valve',
        engine: 'Source 2',
        gpuIntensive: false,
        cpuIntensive: true,
        ramIntensive: false,
        rayTracingSupport: false,
        dlssSupport: false,
        fsrSupport: false
      }
    }),
    prisma.game.create({
      data: {
        name: 'League of Legends',
        genre: 'MOBA',
        releaseDate: new Date('2009-10-27'),
        developer: 'Riot Games',
        publisher: 'Riot Games',
        engine: 'Custom',
        gpuIntensive: false,
        cpuIntensive: true,
        ramIntensive: false,
        rayTracingSupport: false,
        dlssSupport: false,
        fsrSupport: false
      }
    }),
    prisma.game.create({
      data: {
        name: 'Grand Theft Auto V',
        genre: 'Action-Adventure',
        releaseDate: new Date('2013-09-17'),
        developer: 'Rockstar North',
        publisher: 'Rockstar Games',
        engine: 'RAGE',
        gpuIntensive: true,
        cpuIntensive: false,
        ramIntensive: false,
        rayTracingSupport: false,
        dlssSupport: false,
        fsrSupport: false
      }
    })
  ]);

  // Seed Sample Benchmarks
  console.log('📊 Seeding Sample Benchmarks...');
  const benchmarks = await Promise.all([
    // High-end setup benchmarks
    prisma.benchmark.create({
      data: {
        cpuId: cpus[0].id, // i9-14900K
        gpuId: gpus[0].id, // RTX 4090
        ramId: rams[0].id, // 32GB DDR5-6000
        gameId: games[0].id, // Cyberpunk 2077
        resolution: '4K',
        settings: 'Ultra',
        avgFps: 78.5,
        minFps: 65.2,
        maxFps: 95.8,
        source: 'community',
        testDate: new Date('2024-01-15'),
        driverVersion: '546.33',
        osVersion: 'Windows 11 23H2'
      }
    }),
    prisma.benchmark.create({
      data: {
        cpuId: cpus[4].id, // Ryzen 9 7950X3D
        gpuId: gpus[5].id, // RX 7900 XTX
        ramId: rams[1].id, // 32GB DDR5-5600
        gameId: games[0].id, // Cyberpunk 2077
        resolution: '4K',
        settings: 'Ultra',
        avgFps: 72.3,
        minFps: 58.9,
        maxFps: 88.7,
        source: 'community',
        testDate: new Date('2024-01-14'),
        driverVersion: '23.12.1',
        osVersion: 'Windows 11 23H2'
      }
    }),
    // Mid-range setup benchmarks
    prisma.benchmark.create({
      data: {
        cpuId: cpus[2].id, // i5-14600K
        gpuId: gpus[3].id, // RTX 4070
        ramId: rams[2].id, // 16GB DDR5-6000
        gameId: games[0].id, // Cyberpunk 2077
        resolution: '1440p',
        settings: 'High',
        avgFps: 95.2,
        minFps: 78.4,
        maxFps: 112.6,
        source: 'community',
        testDate: new Date('2024-01-13'),
        driverVersion: '546.33',
        osVersion: 'Windows 11 23H2'
      }
    }),
    prisma.benchmark.create({
      data: {
        cpuId: cpus[6].id, // Ryzen 5 7600X
        gpuId: gpus[8].id, // RX 7700 XT
        ramId: rams[2].id, // 16GB DDR5-6000
        gameId: games[0].id, // Cyberpunk 2077
        resolution: '1440p',
        settings: 'High',
        avgFps: 88.7,
        minFps: 72.1,
        maxFps: 105.3,
        source: 'community',
        testDate: new Date('2024-01-12'),
        driverVersion: '23.12.1',
        osVersion: 'Windows 11 23H2'
      }
    }),
    // Budget setup benchmarks
    prisma.benchmark.create({
      data: {
        cpuId: cpus[3].id, // i5-12400F
        gpuId: gpus[4].id, // RTX 4060 Ti
        ramId: rams[3].id, // 16GB DDR4-3600
        gameId: games[0].id, // Cyberpunk 2077
        resolution: '1080p',
        settings: 'Medium',
        avgFps: 75.8,
        minFps: 62.3,
        maxFps: 89.4,
        source: 'community',
        testDate: new Date('2024-01-11'),
        driverVersion: '546.33',
        osVersion: 'Windows 11 23H2'
      }
    }),
    prisma.benchmark.create({
      data: {
        cpuId: cpus[7].id, // Ryzen 5 5600
        gpuId: gpus[9].id, // RX 7600
        ramId: rams[4].id, // 32GB DDR4-3600
        gameId: games[0].id, // Cyberpunk 2077
        resolution: '1080p',
        settings: 'Medium',
        avgFps: 68.9,
        minFps: 55.7,
        maxFps: 82.1,
        source: 'community',
        testDate: new Date('2024-01-10'),
        driverVersion: '23.12.1',
        osVersion: 'Windows 11 23H2'
      }
    })
  ]);

  // Seed Sample User Submissions
  console.log('👥 Seeding Sample User Submissions...');
  await Promise.all([
    prisma.userSubmission.create({
      data: {
        benchmarkId: benchmarks[0].id,
        userId: 'user_001',
        avgFps: 79.2,
        minFps: 66.8,
        maxFps: 96.5,
        hardwareMatch: true,
        confidenceRating: 5,
        notes: 'Excellent performance, ray tracing looks amazing!'
      }
    }),
    prisma.userSubmission.create({
      data: {
        benchmarkId: benchmarks[1].id,
        userId: 'user_002',
        avgFps: 71.8,
        minFps: 59.2,
        maxFps: 87.9,
        hardwareMatch: true,
        confidenceRating: 4,
        notes: 'Great performance for 4K gaming'
      }
    }),
    prisma.userSubmission.create({
      data: {
        benchmarkId: benchmarks[2].id,
        userId: 'user_003',
        avgFps: 94.7,
        minFps: 77.9,
        maxFps: 111.8,
        hardwareMatch: true,
        confidenceRating: 5,
        notes: 'Perfect for 1440p gaming, smooth experience'
      }
    })
  ]);

  console.log('✅ Database seeding completed successfully!');
  console.log(`📊 Seeded ${cpus.length} CPUs, ${gpus.length} GPUs, ${rams.length} RAM kits, ${games.length} games, ${benchmarks.length} benchmarks, and 3 user submissions`);
}

main()
  .catch((e) => {
    console.error('❌ Error during seeding:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

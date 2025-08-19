const fpsData = {
  gpus: [
    { id: 'rtx4090', name: 'NVIDIA RTX 4090', tier: 'flagship', vram: 24, power: 450 },
    { id: 'rtx4080', name: 'NVIDIA RTX 4080', tier: 'high-end', vram: 16, power: 320 },
    { id: 'rtx4070ti', name: 'NVIDIA RTX 4070 Ti', tier: 'high-end', vram: 12, power: 285 },
    { id: 'rtx4070', name: 'NVIDIA RTX 4070', tier: 'mid-high', vram: 12, power: 200 },
    { id: 'rtx4060ti', name: 'NVIDIA RTX 4060 Ti', tier: 'mid', vram: 8, power: 160 },
    { id: 'rtx4060', name: 'NVIDIA RTX 4060', tier: 'mid', vram: 8, power: 115 },
    { id: 'rtx3080', name: 'NVIDIA RTX 3080', tier: 'high-end', vram: 10, power: 320 },
    { id: 'rtx3070', name: 'NVIDIA RTX 3070', tier: 'mid-high', vram: 8, power: 220 },
    { id: 'rtx3060ti', name: 'NVIDIA RTX 3060 Ti', tier: 'mid', vram: 8, power: 200 },
    { id: 'rtx3060', name: 'NVIDIA RTX 3060', tier: 'mid', vram: 12, power: 170 },
    { id: 'rx7900xtx', name: 'AMD RX 7900 XTX', tier: 'flagship', vram: 24, power: 355 },
    { id: 'rx7900xt', name: 'AMD RX 7900 XT', tier: 'high-end', vram: 20, power: 315 },
    { id: 'rx7800xt', name: 'AMD RX 7800 XT', tier: 'high-end', vram: 16, power: 263 },
    { id: 'rx7700xt', name: 'AMD RX 7700 XT', tier: 'mid-high', vram: 12, power: 245 },
    { id: 'rx7600', name: 'AMD RX 7600', tier: 'mid', vram: 8, power: 165 },
    { id: 'rx6700xt', name: 'AMD RX 6700 XT', tier: 'mid-high', vram: 12, power: 230 },
    { id: 'rx6600xt', name: 'AMD RX 6600 XT', tier: 'mid', vram: 8, power: 160 },
    { id: 'rx6600', name: 'AMD RX 6600', tier: 'mid', vram: 8, power: 132 }
  ],

  cpus: [
    { id: 'i9-14900k', name: 'Intel Core i9-14900K', tier: 'flagship', cores: 24, threads: 32, baseClock: 3.2 },
    { id: 'i7-14700k', name: 'Intel Core i7-14700K', tier: 'high-end', cores: 20, threads: 28, baseClock: 3.4 },
    { id: 'i5-14600k', name: 'Intel Core i5-14600K', tier: 'high-end', cores: 14, threads: 20, baseClock: 3.5 },
    { id: 'i5-13600k', name: 'Intel Core i5-13600K', tier: 'high-end', cores: 14, threads: 20, baseClock: 3.5 },
    { id: 'i5-12600k', name: 'Intel Core i5-12600K', tier: 'mid-high', cores: 10, threads: 16, baseClock: 3.7 },
    { id: 'i5-12400f', name: 'Intel Core i5-12400F', tier: 'mid', cores: 6, threads: 12, baseClock: 2.5 },
    { id: 'r9-7950x', name: 'AMD Ryzen 9 7950X', tier: 'flagship', cores: 16, threads: 32, baseClock: 4.5 },
    { id: 'r9-7900x', name: 'AMD Ryzen 9 7900X', tier: 'flagship', cores: 12, threads: 24, baseClock: 4.7 },
    { id: 'r7-7800x3d', name: 'AMD Ryzen 7 7800X3D', tier: 'high-end', cores: 8, threads: 16, baseClock: 4.2 },
    { id: 'r7-7700x', name: 'AMD Ryzen 7 7700X', tier: 'high-end', cores: 8, threads: 16, baseClock: 4.5 },
    { id: 'r5-7600x', name: 'AMD Ryzen 5 7600X', tier: 'high-end', cores: 6, threads: 12, baseClock: 4.7 },
    { id: 'r5-7600', name: 'AMD Ryzen 5 7600', tier: 'mid-high', cores: 6, threads: 12, baseClock: 3.8 },
    { id: 'r5-5600x', name: 'AMD Ryzen 5 5600X', tier: 'mid', cores: 6, threads: 12, baseClock: 3.7 },
    { id: 'r5-5600', name: 'AMD Ryzen 5 5600', tier: 'mid', cores: 6, threads: 12, baseClock: 3.5 }
  ],

  games: [
    { id: 'cyberpunk2077', name: 'Cyberpunk 2077', genre: 'rpg', gpuIntensive: true, cpuIntensive: true },
    { id: 'reddead2', name: 'Red Dead Redemption 2', genre: 'action-adventure', gpuIntensive: true, cpuIntensive: false },
    { id: 'witcher3', name: 'The Witcher 3: Wild Hunt', genre: 'rpg', gpuIntensive: true, cpuIntensive: false },
    { id: 'gta5', name: 'Grand Theft Auto V', genre: 'action-adventure', gpuIntensive: true, cpuIntensive: true },
    { id: 'fortnite', name: 'Fortnite', genre: 'battle-royale', gpuIntensive: false, cpuIntensive: true },
    { id: 'valorant', name: 'Valorant', genre: 'fps', gpuIntensive: false, cpuIntensive: true },
    { id: 'cs2', name: 'Counter-Strike 2', genre: 'fps', gpuIntensive: false, cpuIntensive: true },
    { id: 'apex', name: 'Apex Legends', genre: 'battle-royale', gpuIntensive: false, cpuIntensive: true },
    { id: 'warzone', name: 'Call of Duty: Warzone', genre: 'battle-royale', gpuIntensive: true, cpuIntensive: true },
    { id: 'minecraft', name: 'Minecraft', genre: 'sandbox', gpuIntensive: false, cpuIntensive: true },
    { id: 'assassinscreed', name: 'Assassin\'s Creed Valhalla', genre: 'action-adventure', gpuIntensive: true, cpuIntensive: false },
    { id: 'farcy6', name: 'Far Cry 6', genre: 'fps', gpuIntensive: true, cpuIntensive: false },
    { id: 'metro', name: 'Metro Exodus', genre: 'fps', gpuIntensive: true, cpuIntensive: false },
    { id: 'control', name: 'Control', genre: 'action-adventure', gpuIntensive: true, cpuIntensive: false },
    { id: 'deathstranding', name: 'Death Stranding', genre: 'action-adventure', gpuIntensive: true, cpuIntensive: false },
    { id: 'horizon', name: 'Horizon Zero Dawn', genre: 'action-adventure', gpuIntensive: true, cpuIntensive: false },
    { id: 'godofwar', name: 'God of War', genre: 'action-adventure', gpuIntensive: true, cpuIntensive: false },
    { id: 'spiderman', name: 'Marvel\'s Spider-Man', genre: 'action-adventure', gpuIntensive: true, cpuIntensive: false },
    { id: 'eldenring', name: 'Elden Ring', genre: 'action-rpg', gpuIntensive: true, cpuIntensive: false },
    { id: 'hogwarts', name: 'Hogwarts Legacy', genre: 'action-rpg', gpuIntensive: true, cpuIntensive: false }
  ],

  resolutions: [
    { id: '1080p', name: '1920x1080 (1080p)', multiplier: 1.0 },
    { id: '1440p', name: '2560x1440 (1440p)', multiplier: 1.78 },
    { id: '4k', name: '3840x2160 (4K)', multiplier: 4.0 }
  ],

  settings: [
    { id: 'low', name: 'Low', multiplier: 1.0 },
    { id: 'medium', name: 'Medium', multiplier: 0.7 },
    { id: 'high', name: 'High', multiplier: 0.5 },
    { id: 'ultra', name: 'Ultra', multiplier: 0.3 }
  ]
};

// FPS calculation logic
function calculateFPS(gpuId, cpuId, gameId, resolutionId, settingsId) {
  const gpu = fpsData.gpus.find(g => g.id === gpuId);
  const cpu = fpsData.cpus.find(c => c.id === cpuId);
  const game = fpsData.games.find(g => g.id === gameId);
  const resolution = fpsData.resolutions.find(r => r.id === resolutionId);
  const settings = fpsData.settings.find(s => s.id === settingsId);

  if (!gpu || !cpu || !game || !resolution || !settings) {
    throw new Error('Invalid parameters provided');
  }

  // Base FPS calculation based on GPU tier and game requirements
  let baseFPS = 0;
  
  // GPU tier scoring (0-100)
  const gpuTierScores = { 'flagship': 100, 'high-end': 85, 'mid-high': 70, 'mid': 55 };
  const gpuScore = gpuTierScores[gpu.tier] || 50;
  
  // CPU tier scoring (0-100)
  const cpuTierScores = { 'flagship': 100, 'high-end': 85, 'mid-high': 70, 'mid': 55 };
  const cpuScore = cpuTierScores[cpu.tier] || 50;
  
  // Game intensity scoring
  const gameGpuScore = game.gpuIntensive ? 1.0 : 0.7;
  const gameCpuScore = game.cpuIntensive ? 1.0 : 0.7;
  
  // Calculate base FPS
  baseFPS = (gpuScore * gameGpuScore + cpuScore * gameCpuScore) / 2;
  
  // Apply resolution multiplier
  baseFPS = baseFPS / resolution.multiplier;
  
  // Apply settings multiplier
  baseFPS = baseFPS / settings.multiplier;
  
  // Normalize to realistic FPS ranges
  baseFPS = Math.max(30, Math.min(300, baseFPS));
  
  // Calculate FPS ranges with some variance
  const minFPS = Math.round(baseFPS * 0.8);
  const avgFPS = Math.round(baseFPS);
  const maxFPS = Math.round(baseFPS * 1.2);
  
  // Determine bottleneck
  let bottleneck = 'balanced';
  const gpuContribution = gpuScore * gameGpuScore;
  const cpuContribution = cpuScore * gameCpuScore;
  
  if (gpuContribution < cpuContribution * 0.7) {
    bottleneck = 'gpu';
  } else if (cpuContribution < gpuContribution * 0.7) {
    bottleneck = 'cpu';
  }
  
  return {
    minFPS,
    avgFPS,
    maxFPS,
    bottleneck,
    gpuScore: Math.round(gpuScore),
    cpuScore: Math.round(cpuScore),
    gameIntensity: {
      gpu: game.gpuIntensive,
      cpu: game.cpuIntensive
    }
  };
}

module.exports = {
  fpsData,
  calculateFPS
};

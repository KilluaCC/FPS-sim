const express = require('express');
const router = express.Router();
const { fpsData, calculateFPS } = require('../data/fpsData');

// Get all available data for dropdowns
router.get('/data', (req, res) => {
  try {
    res.json({
      success: true,
      data: {
        gpus: fpsData.gpus.map(gpu => ({ id: gpu.id, name: gpu.name, tier: gpu.tier })),
        cpus: fpsData.cpus.map(cpu => ({ id: cpu.id, name: cpu.name, tier: cpu.tier })),
        games: fpsData.games.map(game => ({ id: game.id, name: game.name, genre: game.genre })),
        resolutions: fpsData.resolutions,
        settings: fpsData.settings
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get FPS estimate
router.post('/estimate', (req, res) => {
  try {
    const { gpuId, cpuId, gameId, resolutionId, settingsId } = req.body;
    
    if (!gpuId || !cpuId || !gameId || !resolutionId || !settingsId) {
      return res.status(400).json({
        success: false,
        error: 'Missing required parameters: gpuId, cpuId, gameId, resolutionId, settingsId'
      });
    }
    
    const result = calculateFPS(gpuId, cpuId, gameId, resolutionId, settingsId);
    
    // Get component details for response
    const gpu = fpsData.gpus.find(g => g.id === gpuId);
    const cpu = fpsData.cpus.find(c => c.id === cpuId);
    const game = fpsData.games.find(g => g.id === gameId);
    const resolution = fpsData.resolutions.find(r => r.id === resolutionId);
    const settings = fpsData.settings.find(s => s.id === settingsId);
    
    res.json({
      success: true,
      data: {
        ...result,
        components: {
          gpu: { id: gpu.id, name: gpu.name, tier: gpu.tier },
          cpu: { id: cpu.id, name: cpu.name, tier: cpu.tier },
          game: { id: game.id, name: game.name, genre: game.genre },
          resolution: resolution,
          settings: settings
        },
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get detailed component information
router.get('/components/:type/:id', (req, res) => {
  try {
    const { type, id } = req.params;
    
    let component = null;
    switch (type) {
      case 'gpu':
        component = fpsData.gpus.find(g => g.id === id);
        break;
      case 'cpu':
        component = fpsData.cpus.find(c => c.id === id);
        break;
      case 'game':
        component = fpsData.games.find(g => g.id === id);
        break;
      default:
        return res.status(400).json({ success: false, error: 'Invalid component type' });
    }
    
    if (!component) {
      return res.status(404).json({ success: false, error: 'Component not found' });
    }
    
    res.json({ success: true, data: component });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Future endpoint for crowd-sourced FPS submissions
router.post('/submit-fps', (req, res) => {
  try {
    const { gpuId, cpuId, gameId, resolutionId, settingsId, actualFPS, userRating } = req.body;
    
    // This would typically save to a database
    // For now, just return success
    res.json({
      success: true,
      message: 'FPS submission received (stored for future crowd-sourcing)',
      data: {
        gpuId,
        cpuId,
        gameId,
        resolutionId,
        settingsId,
        actualFPS,
        userRating,
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({ success: true, status: 'healthy', timestamp: new Date().toISOString() });
});

module.exports = router;

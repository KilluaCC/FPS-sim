const express = require('express');
const router = express.Router();
const dbService = require('../services/database');

// Get all available data for dropdowns
router.get('/data', async (req, res) => {
  try {
    const data = await dbService.getAllData();
    res.json({
      success: true,
      data
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get FPS estimate
router.post('/estimate', async (req, res) => {
  try {
    const { gpuId, cpuId, gameId, resolution, settings } = req.body;
    
    if (!gpuId || !cpuId || !gameId || !resolution || !settings) {
      return res.status(400).json({
        success: false,
        error: 'Missing required parameters: gpuId, cpuId, gameId, resolution, settings'
      });
    }
    
    const result = await dbService.getFPSEstimate(gpuId, cpuId, gameId, resolution, settings);
    
    res.json({
      success: true,
      data: {
        ...result,
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get detailed component information
router.get('/components/:type/:id', async (req, res) => {
  try {
    const { type, id } = req.params;
    
    const component = await dbService.getComponentDetails(type, id);
    
    res.json({ success: true, data: component });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Submit crowd-sourced FPS data
router.post('/submit-fps', async (req, res) => {
  try {
    const { gpuId, cpuId, gameId, resolution, settings, avgFps, minFps, maxFps, userId, notes } = req.body;
    
    if (!gpuId || !cpuId || !gameId || !resolution || !settings || !avgFps) {
      return res.status(400).json({
        success: false,
        error: 'Missing required parameters: gpuId, cpuId, gameId, resolution, settings, avgFps'
      });
    }
    
    const result = await dbService.submitUserFPS({
      gpuId,
      cpuId,
      gameId,
      resolution,
      settings,
      avgFps,
      minFps,
      maxFps,
      userId,
      notes
    });
    
    res.json({
      success: true,
      message: result.message,
      data: result
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get performance statistics
router.get('/stats', async (req, res) => {
  try {
    const stats = await dbService.getPerformanceStats();
    res.json({
      success: true,
      data: stats
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Health check endpoint
router.get('/health', async (req, res) => {
  try {
    const health = await dbService.healthCheck();
    res.json({ 
      success: true, 
      status: health.status, 
      database: health.database,
      timestamp: new Date().toISOString() 
    });
  } catch (error) {
    res.json({ 
      success: false, 
      status: 'unhealthy', 
      database: 'error',
      error: error.message,
      timestamp: new Date().toISOString() 
    });
  }
});

module.exports = router;

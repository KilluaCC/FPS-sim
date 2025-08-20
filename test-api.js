const fetch = require('node-fetch');

const API_BASE = 'http://localhost:5001/api';

async function testAPI() {
  console.log('🧪 Testing FPS Estimator API...\n');

  try {
    // Test health endpoint
    console.log('1. Testing health endpoint...');
    const healthResponse = await fetch(`${API_BASE}/health`);
    const healthData = await healthResponse.json();
    console.log('✅ Health check:', healthData.status);
    console.log('');

    // Test data endpoint
    console.log('2. Testing data endpoint...');
    const dataResponse = await fetch(`${API_BASE}/data`);
    const dataData = await dataResponse.json();
    if (dataData.success) {
      console.log(`✅ Data loaded: ${dataData.data.gpus.length} GPUs, ${dataData.data.cpus.length} CPUs, ${dataData.data.games.length} games`);
    } else {
      console.log('❌ Failed to load data');
    }
    console.log('');

    // Test FPS estimation
    console.log('3. Testing FPS estimation...');
    const estimateResponse = await fetch(`${API_BASE}/estimate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        gpuId: 'rtx4090',
        cpuId: 'i9-14900k',
        gameId: 'cyberpunk2077',
        resolutionId: '1080p',
        settingsId: 'high'
      }),
    });
    
    const estimateData = await estimateResponse.json();
    if (estimateData.success) {
      console.log(`✅ FPS Estimate: ${estimateData.data.avgFPS} FPS average`);
      console.log(`   Min: ${estimateData.data.minFPS}, Max: ${estimateData.data.maxFPS}`);
      console.log(`   Bottleneck: ${estimateData.data.bottleneck}`);
      console.log(`   GPU Score: ${estimateData.data.gpuScore}/100`);
      console.log(`   CPU Score: ${estimateData.data.cpuScore}/100`);
    } else {
      console.log('❌ Failed to get FPS estimate:', estimateData.error);
    }

  } catch (error) {
    console.error('❌ API test failed:', error.message);
    console.log('\n💡 Make sure the server is running on port 5000');
  }
}

// Run the test
testAPI();

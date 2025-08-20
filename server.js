const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(helmet());
app.use(compression());
app.use(cors());
app.use(express.json());

// Import data and routes
const fpsData = require('./data/fpsData');
const apiRoutes = require('./routes/api');

// API Routes
app.use('/api', apiRoutes);

// Serve static files from React build
app.use(express.static(path.join(__dirname, 'client/build')));

// Catch all handler for React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`🚀 FPS Estimator server running on port ${PORT}`);
  console.log(`📊 API available at http://localhost:${PORT}/api`);
});

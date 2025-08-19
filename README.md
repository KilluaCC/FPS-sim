# FPS Estimator - GPU/CPU Performance Calculator

A modern web application that estimates game FPS performance based on your hardware configuration. Built with Node.js, Express, React, and Tailwind CSS.

## 🚀 Features

- **Hardware Selection**: Choose from popular GPUs and CPUs with tier-based categorization
- **Game Library**: 20+ popular games with genre classification
- **Performance Analysis**: Get Min/Average/Max FPS estimates
- **Bottleneck Detection**: Identify if your system is GPU or CPU limited
- **Visual Charts**: Interactive FPS breakdown charts
- **Responsive Design**: Works perfectly on desktop and mobile
- **Share Results**: Copy or share your performance results
- **Future-Ready**: Prepared for crowd-sourced data and premium features

## 🛠️ Tech Stack

### Backend
- **Node.js** with Express.js
- **RESTful API** with comprehensive endpoints
- **Smart FPS calculation** algorithm
- **Bottleneck detection** logic
- **Future-ready** for database integration

### Frontend
- **React 18** with modern hooks
- **Tailwind CSS** for responsive design
- **Chart.js** for data visualization
- **Lucide React** for beautiful icons
- **Glass morphism** UI design

## 📊 Dataset

The application includes a comprehensive dataset of:

- **18 GPUs**: From RTX 4090 to RX 6600, categorized by tier
- **14 CPUs**: Intel and AMD processors across all performance levels
- **20 Games**: Popular titles across different genres
- **3 Resolutions**: 1080p, 1440p, and 4K
- **4 Settings**: Low, Medium, High, and Ultra

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd fps-estimator
   ```

2. **Install dependencies**
   ```bash
   npm run install-all
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Production Build

```bash
npm run build
npm start
```

## 📁 Project Structure

```
fps-estimator/
├── server.js                 # Main Express server
├── data/
│   └── fpsData.js           # Hardware and game dataset
├── routes/
│   └── api.js               # API endpoints
├── client/                   # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.js           # Main app component
│   │   └── index.js         # Entry point
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
└── package.json             # Backend dependencies
```

## 🔌 API Endpoints

### GET `/api/data`
Returns all available hardware and game data for dropdowns.

### POST `/api/estimate`
Calculate FPS estimates based on selected components.

**Request Body:**
```json
{
  "gpuId": "rtx4090",
  "cpuId": "i9-14900k",
  "gameId": "cyberpunk2077",
  "resolutionId": "1080p",
  "settingsId": "high"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "minFPS": 120,
    "avgFPS": 150,
    "maxFPS": 180,
    "bottleneck": "balanced",
    "gpuScore": 100,
    "cpuScore": 100,
    "components": { ... }
  }
}
```

### POST `/api/submit-fps`
Submit crowd-sourced FPS data (future feature).

### GET `/api/health`
Health check endpoint.

## 🎯 FPS Calculation Algorithm

The application uses a sophisticated algorithm that considers:

1. **Hardware Tier Scoring**: Each component gets a score (0-100) based on performance tier
2. **Game Intensity**: Games are classified as GPU-intensive, CPU-intensive, or both
3. **Resolution Impact**: Higher resolutions significantly reduce FPS
4. **Settings Multiplier**: Graphics settings affect performance exponentially
5. **Bottleneck Detection**: Identifies which component is limiting performance

## 🎨 UI Components

### FPSForm
- Searchable dropdowns for GPU, CPU, and game selection
- Resolution and graphics settings selection
- Form validation and submission handling

### ResultsPanel
- Large FPS display with color-coded performance
- Interactive bar chart visualization
- Bottleneck analysis with recommendations
- Component performance scores
- Configuration summary

### AdPlaceholder
- Premium feature showcase
- Future monetization integration
- Upgrade call-to-action

## 🔮 Future Features

- **User Accounts**: Save configurations and track performance over time
- **Crowd-Sourced Data**: Real user FPS submissions for more accurate estimates
- **Upgrade Recommendations**: AI-powered suggestions for hardware improvements
- **Performance Tracking**: Historical FPS data and trends
- **Affiliate Integration**: Links to purchase recommended hardware
- **Mobile App**: Native iOS/Android applications

## 🧪 Testing

```bash
# Run frontend tests
cd client
npm test

# Test API endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/data
```

## 📱 Responsive Design

The application is fully responsive with:
- **Mobile-first** approach
- **Adaptive layouts** for different screen sizes
- **Touch-friendly** interface elements
- **Optimized performance** on all devices

## 🎨 Design System

- **Color Palette**: Dark theme with blue/purple accents
- **Typography**: Inter font family for modern readability
- **Spacing**: Consistent 8px grid system
- **Animations**: Smooth transitions and hover effects
- **Glass Morphism**: Modern backdrop blur effects

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **GPUCheck** for inspiration
- **Chart.js** for beautiful data visualization
- **Tailwind CSS** for utility-first styling
- **Lucide** for beautiful icons

## 📞 Support

For questions or support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for the gaming community**

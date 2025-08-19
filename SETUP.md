# 🚀 Quick Setup Guide

## Prerequisites
- Node.js 16+ installed
- npm or yarn package manager

## 🎯 One-Command Setup

```bash
# Make the startup script executable and run it
chmod +x start.sh && ./start.sh
```

This will:
1. ✅ Install all dependencies (backend + frontend)
2. 🚀 Start both development servers
3. 🌐 Open the application in your browser

## 📱 Access Points

- **Frontend App**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 🧪 Test the API

```bash
# Test if everything is working
node test-api.js
```

## 🎮 How to Use

1. **Select Hardware**: Choose your GPU and CPU from the dropdowns
2. **Pick a Game**: Select from 20+ popular games
3. **Set Resolution**: Choose 1080p, 1440p, or 4K
4. **Choose Settings**: Low, Medium, High, or Ultra
5. **Get Results**: View FPS estimates, bottleneck analysis, and charts

## 🔧 Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Install backend dependencies
npm install

# Install frontend dependencies
cd client && npm install && cd ..

# Start development servers
npm run dev
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill processes on ports 3000 and 5000
lsof -ti:3000 | xargs kill -9
lsof -ti:5000 | xargs kill -9
```

### Dependencies Issues
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Frontend Build Issues
```bash
cd client
rm -rf node_modules package-lock.json
npm install
npm run build
```

## 📊 What You Get

- **18 GPUs**: From RTX 4090 to RX 6600
- **14 CPUs**: Intel and AMD across all tiers
- **20 Games**: Popular titles with genre classification
- **Smart Algorithm**: FPS calculation with bottleneck detection
- **Beautiful UI**: Modern, responsive design with charts
- **Future Ready**: Prepared for crowd-sourced data and premium features

## 🎯 Next Steps

1. **Test the app** with different hardware combinations
2. **Customize the dataset** in `data/fpsData.js`
3. **Add new features** like user accounts or real-time data
4. **Deploy to production** using the build command

---

**Ready to estimate some FPS? Let's go! 🎮**

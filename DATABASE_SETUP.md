# 🗄️ Database Integration Setup Guide

This guide will help you integrate the PostgreSQL database with your existing FPS Estimator app.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Setup Database
```bash
# Option A: Automated setup (recommended)
npm run db:setup

# Option B: Manual setup
cd database
chmod +x setup.sh
./setup.sh
```

### 3. Generate Prisma Client
```bash
npm run db:generate
```

### 4. Start the App
```bash
npm run dev
```

## 🔧 Environment Configuration

Create a `.env` file in your root directory:

```env
# Database Configuration
DATABASE_URL="postgresql://fps_user:fps_password_2024@localhost:5432/fps_estimator"

# App Configuration
NODE_ENV=development
PORT=5001
```

## 📊 What's Changed

### **API Endpoints Updated**
- **`GET /api/data`**: Now fetches from database instead of JSON
- **`POST /api/estimate`**: Uses real benchmark data + fallback calculations
- **`GET /api/components/:type/:id`**: Enhanced component details with benchmarks
- **`POST /api/submit-fps`**: Real crowd-sourcing data storage
- **`GET /api/health`**: Database connection status
- **`GET /api/stats`**: Performance statistics (new endpoint)

### **Data Structure Changes**
- **IDs**: Now numeric (1, 2, 3) instead of strings ('rtx4090', 'i9-14900k')
- **Enhanced Data**: Pricing, architecture, ray tracing support
- **Real Benchmarks**: Actual FPS measurements when available
- **Fallback Logic**: Smart estimation when no benchmark exists

## 🔄 Migration from JSON to Database

### **Frontend Updates Required**

Your React components need to handle the new data structure:

```javascript
// Old: String IDs
const gpuId = 'rtx4090';
const cpuId = 'i9-14900k';

// New: Numeric IDs
const gpuId = 1;  // RTX 4090
const cpuId = 1;  // i9-14900K
```

### **Component Updates**

#### **FPSForm.js**
```javascript
// Update form submission
const handleSubmit = async (e) => {
  e.preventDefault();
  
  const formData = {
    gpuId: parseInt(selectedGPU),      // Convert to number
    cpuId: parseInt(selectedCPU),      // Convert to number
    gameId: parseInt(selectedGame),    // Convert to number
    resolution: selectedResolution,    // Keep as string
    settings: selectedSettings         // Keep as string
  };
  
  // Submit to API
  const response = await fetch('/api/estimate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  });
};
```

#### **ResultsPanel.js**
```javascript
// Handle new data structure
const { avgFPS, minFPS, maxFPS, source, bottleneck, components } = results;

// Show data source
{source === 'database' && (
  <div className="text-green-500 text-sm">
    📊 Real benchmark data
  </div>
)}

{source === 'estimated' && (
  <div className="text-yellow-500 text-sm">
    ⚡ Estimated performance
  </div>
)}
```

## 🎯 New Features Available

### **1. Real Benchmark Data**
- **Database Priority**: Real FPS measurements first
- **Fallback Logic**: Smart estimation when no data exists
- **Source Tracking**: Know if you're seeing real vs estimated data

### **2. Enhanced Component Details**
```javascript
// Get detailed GPU info with benchmarks
const gpuDetails = await fetch(`/api/components/gpu/${gpuId}`);
const { benchmarks, ...gpuInfo } = await gpuDetails.json();

// Show recent benchmarks
{benchmarks.map(benchmark => (
  <div key={benchmark.id}>
    {benchmark.game.name}: {benchmark.avgFps} FPS
  </div>
))}
```

### **3. Crowdsourcing System**
```javascript
// Submit your FPS data
const submitFPS = async (data) => {
  const response = await fetch('/api/submit-fps', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      gpuId: 1,
      cpuId: 1,
      gameId: 1,
      resolution: '1080p',
      settings: 'High',
      avgFps: 120,
      minFps: 100,
      maxFps: 140,
      notes: 'Great performance!'
    })
  });
};
```

### **4. Performance Statistics**
```javascript
// Get performance stats
const stats = await fetch('/api/stats');
const performanceData = await stats.json();

// Show hardware combinations with most benchmarks
{performanceData.map(stat => (
  <div key={`${stat.gpuId}-${stat.cpuId}`}>
    GPU {stat.gpuId} + CPU {stat.cpuId}: {stat.benchmarkCount} tests
  </div>
))}
```

## 🧪 Testing the Integration

### **1. Health Check**
```bash
curl http://localhost:5001/api/health
```

Expected response:
```json
{
  "success": true,
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-XX..."
}
```

### **2. Test Data Fetching**
```bash
curl http://localhost:5001/api/data
```

Should return database data instead of JSON data.

### **3. Test FPS Estimation**
```bash
curl -X POST http://localhost:5001/api/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "gpuId": 1,
    "cpuId": 1,
    "gameId": 1,
    "resolution": "1080p",
    "settings": "High"
  }'
```

## 🚨 Troubleshooting

### **Database Connection Issues**
```bash
# Check PostgreSQL status
brew services list | grep postgresql
sudo systemctl status postgresql

# Test connection
psql -U fps_user -d fps_estimator -c "SELECT 1;"
```

### **Prisma Issues**
```bash
# Regenerate client
npm run db:generate

# Reset database
npm run db:reset

# Check Prisma status
npx prisma --version
```

### **API Errors**
```bash
# Check server logs
npm run server

# Test individual endpoints
curl http://localhost:5001/api/health
curl http://localhost:5001/api/data
```

## 📈 Performance Benefits

### **Before (JSON)**
- ❌ Static data only
- ❌ No real benchmarks
- ❌ Limited scalability
- ❌ No user contributions

### **After (Database)**
- ✅ Real benchmark data
- ✅ Smart fallback calculations
- ✅ Scalable to 1000+ components
- ✅ Crowdsourced validation
- ✅ Performance analytics
- ✅ Real-time updates

## 🔮 Next Steps

### **Immediate (Week 1)**
1. ✅ Database setup and seeding
2. ✅ API integration
3. ✅ Frontend ID handling updates
4. ✅ Testing and validation

### **Short Term (Week 2-3)**
1. 🔄 Add more hardware components
2. 🔄 Implement user authentication
3. 🔄 Add benchmark comparison tools
4. 🔄 Create admin dashboard

### **Medium Term (Month 2)**
1. 🔄 Machine learning integration
2. 🔄 Real-time pricing APIs
3. 🔄 Advanced analytics
4. 🔄 Mobile app optimization

## 📚 Additional Resources

- **Database Schema**: `database/migrations/001_initial_schema.sql`
- **Prisma Schema**: `prisma/schema.prisma`
- **Database Service**: `services/database.js`
- **API Routes**: `routes/api.js`
- **Setup Script**: `database/setup.sh`

---

**Need help?** Check the troubleshooting section or create an issue in the repository.

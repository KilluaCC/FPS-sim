# 🗄️ FPS Estimator Database Setup

This directory contains the complete database setup for the FPS Estimator application, including PostgreSQL schema, Prisma ORM configuration, and sample data seeding.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Database Schema](#database-schema)
- [Prisma Setup](#prisma-setup)
- [Seeding Data](#seeding-data)
- [API Integration](#api-integration)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The database is designed to store:
- **Hardware Components**: CPUs, GPUs, RAM with detailed specifications
- **Games**: Game metadata with performance characteristics
- **Benchmarks**: FPS test results from various hardware combinations
- **User Submissions**: Crowdsourced validation data

## 🔧 Prerequisites

- **PostgreSQL 14+** installed and running
- **Node.js 18+** and npm
- **Database user** with CREATE/DROP privileges

### PostgreSQL Installation

#### macOS (using Homebrew)
```bash
brew install postgresql
brew services start postgresql
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Windows
Download from [PostgreSQL official website](https://www.postgresql.org/download/windows/)

## 🚀 Quick Start

### 1. Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE fps_estimator;
CREATE USER fps_user WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fps_estimator TO fps_user;
\q
```

### 2. Install Dependencies
```bash
cd database
npm install
```

### 3. Configure Environment
Create `.env` file:
```env
DATABASE_URL="postgresql://fps_user:your_password@localhost:5432/fps_estimator"
```

### 4. Setup Database
```bash
# Generate Prisma client, push schema, and seed data
npm run setup
```

## 🗂️ Database Schema

### Core Tables

#### `cpu` - Processor Information
```sql
- id: Primary key
- name: Full processor name (e.g., "Intel Core i9-14900K")
- brand: Manufacturer (Intel, AMD)
- cores: Physical core count
- threads: Logical thread count
- base_clock: Base frequency in GHz
- boost_clock: Maximum boost frequency
- tdp: Thermal Design Power in watts
- tier: Performance tier (flagship, high-end, mid-high, mid, budget)
- price_usd: Current market price
- socket: CPU socket type
- architecture: Microarchitecture name
```

#### `gpu` - Graphics Card Information
```sql
- id: Primary key
- name: Full GPU name (e.g., "NVIDIA RTX 4090")
- brand: Manufacturer (NVIDIA, AMD, Intel)
- vram_gb: Video memory in GB
- base_clock: Base frequency in MHz
- boost_clock: Maximum boost frequency
- tier: Performance tier
- price_usd: Current market price
- memory_type: VRAM type (GDDR6X, GDDR6, HBM2)
- ray_tracing_cores: RT core count
- tensor_cores: AI/Tensor core count
```

#### `ram` - Memory Information
```sql
- id: Primary key
- size_gb: Memory capacity in GB
- speed_mhz: Memory frequency in MHz
- type: Memory type (DDR4, DDR5)
- brand: Manufacturer
- model: Specific model name
- cas_latency: CAS latency timing
- voltage: Operating voltage
```

#### `game` - Game Information
```sql
- id: Primary key
- name: Game title
- genre: Game genre
- developer: Development studio
- publisher: Publishing company
- engine: Game engine
- gpu_intensive: GPU-demanding game
- cpu_intensive: CPU-demanding game
- ray_tracing_support: RT support
- dlss_support: NVIDIA DLSS support
- fsr_support: AMD FSR support
```

#### `benchmark` - Performance Results
```sql
- id: Primary key
- cpu_id: Reference to CPU
- gpu_id: Reference to GPU
- ram_id: Reference to RAM
- game_id: Reference to Game
- resolution: Test resolution (1080p, 1440p, 4K)
- settings: Graphics quality (Low, Medium, High, Ultra)
- avg_fps: Average FPS achieved
- min_fps: Minimum FPS recorded
- max_fps: Maximum FPS recorded
- source: Data source (URL or 'community')
```

#### `user_submission` - Crowdsourced Data
```sql
- id: Primary key
- benchmark_id: Reference to benchmark
- user_id: Anonymous user identifier
- avg_fps: User's reported average FPS
- hardware_match: Exact hardware match flag
- confidence_rating: User confidence (1-5)
- notes: Additional user notes
```

## ⚡ Prisma Setup

### Generate Client
```bash
npm run db:generate
```

### Database Operations
```bash
# Push schema changes (development)
npm run db:push

# Create and apply migrations (production)
npm run db:migrate

# Open Prisma Studio (GUI)
npm run db:studio

# Reset database (careful!)
npm run db:reset
```

### Prisma Client Usage
```javascript
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// Query CPUs
const cpus = await prisma.cpu.findMany({
  where: { tier: 'flagship' },
  include: { benchmarks: true }
});

// Create benchmark
const benchmark = await prisma.benchmark.create({
  data: {
    cpuId: 1,
    gpuId: 1,
    ramId: 1,
    gameId: 1,
    resolution: '4K',
    settings: 'Ultra',
    avgFps: 75.5,
    minFps: 65.2,
    maxFps: 88.9
  }
});
```

## 🌱 Seeding Data

### Run Seeder
```bash
npm run db:seed
```

### Sample Data Included
- **8 CPUs**: Intel i9-14900K to AMD Ryzen 5 5600
- **10 GPUs**: RTX 4090 to RX 7600
- **5 RAM kits**: DDR4/DDR5 configurations
- **10 Games**: Popular titles with metadata
- **6 Benchmarks**: Sample performance data
- **3 User Submissions**: Crowdsourced validation

### Customize Seeding
Edit `seed.js` to:
- Add more hardware components
- Include different games
- Modify benchmark data
- Adjust pricing information

## 🔌 API Integration

### Update Your Backend
Replace the JSON-based `fpsData.js` with Prisma queries:

```javascript
// Old: JSON-based
const fpsData = require('./data/fpsData');
const result = calculateFPS(gpuId, cpuId, gameId, resolution, settings);

// New: Database-based
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function getFPSEstimate(gpuId, cpuId, gameId, resolution, settings) {
  const benchmark = await prisma.benchmark.findFirst({
    where: {
      gpuId: parseInt(gpuId),
      cpuId: parseInt(cpuId),
      gameId: parseInt(gameId),
      resolution,
      settings
    },
    include: {
      gpu: true,
      cpu: true,
      game: true
    }
  });
  
  return benchmark || calculateEstimatedFPS(gpuId, cpuId, gameId, resolution, settings);
}
```

### Environment Variables
Update your main `.env` file:
```env
# Database
DATABASE_URL="postgresql://fps_user:your_password@localhost:5432/fps_estimator"

# App
NODE_ENV=development
PORT=5001
```

## 🚨 Troubleshooting

### Common Issues

#### Connection Refused
```bash
# Check PostgreSQL status
brew services list | grep postgresql
sudo systemctl status postgresql

# Verify port
netstat -an | grep 5432
```

#### Permission Denied
```bash
# Grant privileges
psql -U postgres -d fps_estimator
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fps_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fps_user;
```

#### Prisma Client Not Generated
```bash
# Regenerate client
npm run db:generate

# Check Prisma version
npx prisma --version
```

#### Migration Conflicts
```bash
# Reset database (development only)
npm run db:reset

# Or manually drop/recreate
DROP DATABASE fps_estimator;
CREATE DATABASE fps_estimator;
```

### Performance Tips

#### Indexes
The schema includes optimized indexes for:
- Hardware tier filtering
- Game genre queries
- Benchmark lookups
- User submission tracking

#### Connection Pooling
For production, consider connection pooling:
```env
DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=20&pool_timeout=20"
```

#### Query Optimization
Use Prisma's query optimization features:
```javascript
// Include only needed relations
const result = await prisma.benchmark.findMany({
  select: {
    avgFps: true,
    gpu: { select: { name: true, tier: true } },
    cpu: { select: { name: true, tier: true } }
  }
});
```

## 📚 Additional Resources

- [Prisma Documentation](https://www.prisma.io/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Database Design Best Practices](https://www.postgresql.org/docs/current/ddl.html)

## 🤝 Contributing

When adding new hardware or games:
1. Update the seed script
2. Test with `npm run db:reset && npm run setup`
3. Verify data integrity
4. Update API endpoints if needed

---

**Need help?** Check the troubleshooting section or create an issue in the main repository.

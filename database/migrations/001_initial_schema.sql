-- Migration: 001_initial_schema.sql
-- Description: Initial database schema for FPS Estimator app
-- Created: 2024-01-XX

BEGIN;

-- CPU table
CREATE TABLE cpu (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    brand VARCHAR(50) NOT NULL,
    cores INT NOT NULL,
    threads INT NOT NULL,
    base_clock DECIMAL(4,2) NOT NULL,
    boost_clock DECIMAL(4,2),
    tdp INT,
    release_date DATE,
    tier VARCHAR(20) DEFAULT 'mid', -- flagship, high-end, mid-high, mid, budget
    price_usd DECIMAL(8,2),
    socket VARCHAR(50), -- LGA1700, AM5, etc.
    architecture VARCHAR(50), -- Zen 4, Raptor Lake, etc.
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- GPU table
CREATE TABLE gpu (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    brand VARCHAR(50) NOT NULL,
    vram_gb INT NOT NULL,
    base_clock DECIMAL(6,2) NOT NULL,
    boost_clock DECIMAL(6,2),
    tdp INT,
    release_date DATE,
    tier VARCHAR(20) DEFAULT 'mid', -- flagship, high-end, mid-high, mid, budget
    price_usd DECIMAL(8,2),
    memory_type VARCHAR(20), -- GDDR6X, GDDR6, HBM2, etc.
    memory_bus_width INT, -- 256-bit, 384-bit, etc.
    ray_tracing_cores INT,
    tensor_cores INT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- RAM table
CREATE TABLE ram (
    id SERIAL PRIMARY KEY,
    size_gb INT NOT NULL,
    speed_mhz INT NOT NULL,
    type VARCHAR(20) NOT NULL, -- DDR4, DDR5
    brand VARCHAR(100),
    model VARCHAR(255),
    cas_latency INT,
    voltage DECIMAL(3,2),
    price_usd DECIMAL(8,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Game table
CREATE TABLE game (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    genre VARCHAR(100),
    release_date DATE,
    developer VARCHAR(255),
    publisher VARCHAR(255),
    engine VARCHAR(100), -- Unreal Engine 5, Source 2, etc.
    gpu_intensive BOOLEAN DEFAULT false,
    cpu_intensive BOOLEAN DEFAULT false,
    ram_intensive BOOLEAN DEFAULT false,
    ray_tracing_support BOOLEAN DEFAULT false,
    dlss_support BOOLEAN DEFAULT false,
    fsr_support BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Benchmark results
CREATE TABLE benchmark (
    id SERIAL PRIMARY KEY,
    cpu_id INT REFERENCES cpu(id) ON DELETE CASCADE,
    gpu_id INT REFERENCES gpu(id) ON DELETE CASCADE,
    ram_id INT REFERENCES ram(id) ON DELETE CASCADE,
    game_id INT REFERENCES game(id) ON DELETE CASCADE,
    resolution VARCHAR(20) NOT NULL, -- "1080p", "1440p", "4K"
    settings VARCHAR(50) NOT NULL, -- "Low", "Medium", "High", "Ultra"
    avg_fps DECIMAL(6,2) NOT NULL,
    min_fps DECIMAL(6,2),
    max_fps DECIMAL(6,2),
    source VARCHAR(255), -- URL or 'community'
    test_date DATE,
    driver_version VARCHAR(100),
    os_version VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- User submissions (crowdsourced validation)
CREATE TABLE user_submission (
    id SERIAL PRIMARY KEY,
    benchmark_id INT REFERENCES benchmark(id) ON DELETE CASCADE,
    user_id VARCHAR(255), -- anonymous or hashed if you want
    avg_fps DECIMAL(6,2) NOT NULL,
    min_fps DECIMAL(6,2),
    max_fps DECIMAL(6,2),
    hardware_match BOOLEAN DEFAULT true, -- if user has exact same hardware
    confidence_rating INT CHECK (confidence_rating >= 1 AND confidence_rating <= 5),
    notes TEXT,
    submitted_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_cpu_brand ON cpu(brand);
CREATE INDEX idx_cpu_tier ON cpu(tier);
CREATE INDEX idx_gpu_brand ON gpu(brand);
CREATE INDEX idx_gpu_tier ON gpu(tier);
CREATE INDEX idx_gpu_vram ON gpu(vram_gb);
CREATE INDEX idx_game_genre ON game(genre);
CREATE INDEX idx_benchmark_game_resolution ON benchmark(game_id, resolution);
CREATE INDEX idx_benchmark_cpu_gpu ON benchmark(cpu_id, gpu_id);
CREATE INDEX idx_user_submission_benchmark ON user_submission(benchmark_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_cpu_updated_at BEFORE UPDATE ON cpu FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gpu_updated_at BEFORE UPDATE ON gpu FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ram_updated_at BEFORE UPDATE ON ram FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_game_updated_at BEFORE UPDATE ON game FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_benchmark_updated_at BEFORE UPDATE ON benchmark FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMIT;

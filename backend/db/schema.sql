-- ==============================================================================
-- Smart NER Logistics Control Platform
-- Pure PostgreSQL DDL for Supabase SQL Editor
-- ==============================================================================

-- 1. Users Table
CREATE TABLE IF NOT EXISTS public.users (
    id VARCHAR(64) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    role VARCHAR(50) NOT NULL,
    organization VARCHAR(255),
    encrypted_password VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'Active',
    created_at VARCHAR(50),
    last_login VARCHAR(50)
);
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);

-- 2. Vehicles Table
CREATE TABLE IF NOT EXISTS public.vehicles (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    max_payload_kg DOUBLE PRECISION NOT NULL,
    max_volume_m3 DOUBLE PRECISION NOT NULL,
    hill_grade_rating VARCHAR(255),
    fuel_type VARCHAR(50),
    current_status VARCHAR(100) DEFAULT 'Available',
    license_plate VARCHAR(50) UNIQUE NOT NULL
);

-- 3. Drivers Table
CREATE TABLE IF NOT EXISTS public.drivers (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    experience_years INT DEFAULT 0,
    hill_driving_certified BOOLEAN DEFAULT TRUE,
    languages JSONB DEFAULT '[]'::jsonb,
    status VARCHAR(50) DEFAULT 'Available',
    rating DOUBLE PRECISION DEFAULT 4.8,
    avatar_url VARCHAR(500),
    current_trip_id VARCHAR(64),
    busy_until TIMESTAMP WITH TIME ZONE,
    assigned_at TIMESTAMP WITH TIME ZONE,
    deadline_hours DOUBLE PRECISION
);

-- 4. Shipments Table
CREATE TABLE IF NOT EXISTS public.shipments (
    id VARCHAR(64) PRIMARY KEY,
    origin VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    cargo_items JSONB NOT NULL,
    required_delivery_hours DOUBLE PRECISION NOT NULL,
    selected_vehicle_id VARCHAR(64),
    selected_route_id VARCHAR(64),
    status VARCHAR(50) DEFAULT 'Draft',
    created_at VARCHAR(50) NOT NULL
);

-- 5. Trips Table
CREATE TABLE IF NOT EXISTS public.trips (
    id VARCHAR(64) PRIMARY KEY,
    shipment_id VARCHAR(64),
    route_id VARCHAR(64),
    route_name VARCHAR(255),
    driver_id VARCHAR(64),
    driver_name VARCHAR(255),
    vehicle_id VARCHAR(64),
    vehicle_name VARCHAR(255),
    origin VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    manifest JSONB,
    current_status VARCHAR(100) DEFAULT 'Assigned',
    connectivity_mode VARCHAR(50) DEFAULT 'Online',
    checkpoints JSONB DEFAULT '[]'::jsonb,
    offline_sync_pending BOOLEAN DEFAULT FALSE,
    last_sync_time VARCHAR(50),
    active_alert VARCHAR(500)
);

-- 6. Disruptions Table
CREATE TABLE IF NOT EXISTS public.disruptions (
    id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    corridor_name VARCHAR(255) NOT NULL,
    highway_ref VARCHAR(100) NOT NULL,
    affected_segment VARCHAR(255) NOT NULL,
    disruption_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'Active',
    coordinates JSONB,
    estimated_clearance_hours DOUBLE PRECISION DEFAULT 4.0,
    recommended_reroute_id VARCHAR(64),
    reported_at VARCHAR(50) NOT NULL,
    source_type VARCHAR(100) DEFAULT 'SIMULATED DATA'
);

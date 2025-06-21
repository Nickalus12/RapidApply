-- Initial PostgreSQL setup for RapidApply v2.0

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS "pgvector"; -- Will add this later with proper image
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database if not exists
SELECT 'CREATE DATABASE rapidapply'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'rapidapply')\gexec

-- Connect to rapidapply database
\c rapidapply

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email_trgm ON users USING gin (email gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_jobs_company_trgm ON jobs USING gin (company gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_jobs_title_trgm ON jobs USING gin (title gin_trgm_ops);

-- Create function for updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE rapidapply TO rapidapply;
GRANT ALL ON SCHEMA public TO rapidapply;
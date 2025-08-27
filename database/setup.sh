#!/bin/bash

# 🗄️ FPS Estimator Database Setup Script
# This script automates the PostgreSQL database setup for the FPS Estimator app

set -e  # Exit on any error

echo "🚀 Starting FPS Estimator Database Setup..."
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if PostgreSQL is running
check_postgres() {
    print_status "Checking PostgreSQL status..."
    
    if command -v pg_isready &> /dev/null; then
        if pg_isready -q; then
            print_success "PostgreSQL is running"
            return 0
        else
            print_error "PostgreSQL is not responding"
            return 1
        fi
    else
        print_error "PostgreSQL is not installed or not in PATH"
        return 1
    fi
}

# Check if database exists
check_database() {
    local db_name="$1"
    local user="$2"
    
    print_status "Checking if database '$db_name' exists..."
    
    if psql -U "$user" -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
        print_success "Database '$db_name' exists"
        return 0
    else
        print_warning "Database '$db_name' does not exist"
        return 1
    fi
}

# Create database and user
create_database() {
    local db_name="$1"
    local user="$2"
    local password="$3"
    
    print_status "Creating database and user..."
    
    # Create user if it doesn't exist
    if ! psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$user'" | grep -q 1; then
        print_status "Creating user '$user'..."
        psql -U postgres -c "CREATE USER $user WITH ENCRYPTED PASSWORD '$password';"
        print_success "User '$user' created"
    else
        print_status "User '$user' already exists"
    fi
    
    # Create database
    print_status "Creating database '$db_name'..."
    psql -U postgres -c "CREATE DATABASE $db_name OWNER $user;"
    print_success "Database '$db_name' created"
    
    # Grant privileges
    print_status "Granting privileges..."
    psql -U postgres -d "$db_name" -c "GRANT ALL PRIVILEGES ON DATABASE $db_name TO $user;"
    psql -U postgres -d "$db_name" -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $user;"
    psql -U postgres -d "$db_name" -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $user;"
    psql -U postgres -d "$db_name" -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $user;"
    print_success "Privileges granted"
}

# Install Node.js dependencies
install_dependencies() {
    print_status "Installing Node.js dependencies..."
    
    if [ ! -f "package.json" ]; then
        print_error "package.json not found in current directory"
        return 1
    fi
    
    npm install
    print_success "Dependencies installed"
}

# Setup Prisma
setup_prisma() {
    print_status "Setting up Prisma..."
    
    # Generate Prisma client
    print_status "Generating Prisma client..."
    npm run db:generate
    
    # Push schema to database
    print_status "Pushing schema to database..."
    npm run db:push
    
    print_success "Prisma setup completed"
}

# Seed database
seed_database() {
    print_status "Seeding database with sample data..."
    
    npm run db:seed
    
    print_success "Database seeded successfully"
}

# Create .env file
create_env_file() {
    local db_name="$1"
    local user="$2"
    local password="$3"
    
    print_status "Creating .env file..."
    
    cat > .env << EOF
# Database Configuration
DATABASE_URL="postgresql://$user:$password@localhost:5432/$db_name"

# App Configuration
NODE_ENV=development
PORT=5001
EOF
    
    print_success ".env file created"
}

# Main setup function
main() {
    local db_name="fps_estimator"
    local user="fps_user"
    local password="fps_password_2024"
    
    echo ""
    print_status "Configuration:"
    echo "  Database: $db_name"
    echo "  User: $user"
    echo "  Password: $password"
    echo ""
    
    # Check PostgreSQL
    if ! check_postgres; then
        print_error "Please start PostgreSQL and try again"
        echo ""
        echo "macOS: brew services start postgresql"
        echo "Ubuntu: sudo systemctl start postgresql"
        echo "Windows: Start PostgreSQL service"
        exit 1
    fi
    
    # Check if database exists
    if check_database "$db_name" "$user"; then
        read -p "Database already exists. Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Dropping existing database..."
            psql -U postgres -c "DROP DATABASE IF EXISTS $db_name;"
            print_success "Database dropped"
        else
            print_warning "Using existing database"
        fi
    fi
    
    # Create database if it doesn't exist
    if ! check_database "$db_name" "$user"; then
        create_database "$db_name" "$user" "$password"
    fi
    
    # Install dependencies
    install_dependencies
    
    # Create .env file
    create_env_file "$db_name" "$user" "$password"
    
    # Setup Prisma
    setup_prisma
    
    # Seed database
    seed_database
    
    echo ""
    echo "🎉 Database setup completed successfully!"
    echo ""
    echo "📊 Database Details:"
    echo "  Name: $db_name"
    echo "  User: $user"
    echo "  Host: localhost"
    echo "  Port: 5432"
    echo ""
    echo "🔧 Next Steps:"
    echo "  1. Update your main .env file with the DATABASE_URL"
    echo "  2. Modify your API to use Prisma instead of JSON data"
    echo "  3. Test the connection with: npm run db:studio"
    echo ""
    echo "📚 Documentation: database/README.md"
    echo "🐛 Troubleshooting: Check the README or run 'npm run db:reset' to start over"
}

# Check if script is run with correct permissions
if [ "$EUID" -eq 0 ]; then
    print_warning "This script should not be run as root"
    exit 1
fi

# Run main function
main "$@"

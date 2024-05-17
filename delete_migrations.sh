#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define the project directory
PROJECT_DIR=$(pwd)

# Define the path to the migrations folder
MIGRATIONS_DIR="$PROJECT_DIR/migrations"

# Check if the flask command is available
# if ! command -v flask &> /dev/null; then
#     echo "flask command not found. Please ensure Flask is installed and available in your PATH."
#     exit 1
# fi

# Check if the migrations folder exists and delete it if it does
if [ -d "$MIGRATIONS_DIR" ]; then
    echo "Deleting migrations folder..."
    rm -rf "$MIGRATIONS_DIR"
    echo "Migrations folder deleted."
else
    echo "Migrations folder does not exist. No need to delete."
fi

# Initialize, migrate, and upgrade the database
flask db init


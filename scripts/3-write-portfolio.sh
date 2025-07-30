#!/bin/bash

# Change to project root directory
cd "$(dirname "$0")/.."

echo "Generating portfolio..."
python cli.py write-portfolio
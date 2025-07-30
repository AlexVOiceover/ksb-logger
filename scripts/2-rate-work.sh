#!/bin/bash

# Change to project root directory
cd "$(dirname "$0")/.."

echo "Rating work against KSBs..."
python cli.py rate-work
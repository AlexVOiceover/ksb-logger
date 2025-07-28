#!/bin/bash

# Load environment variables
source .env

# Check if GITHUB_USERNAME is set
if [ -z "$GITHUB_USERNAME" ]; then
    echo "Error: GITHUB_USERNAME not set in .env file"
    exit 1
fi

echo "Starting interactive repository selection for user: $GITHUB_USERNAME"
python cli.py pull-prs --username "$GITHUB_USERNAME" --days-back "$GITHUB_DAYSBACK" --interactive 
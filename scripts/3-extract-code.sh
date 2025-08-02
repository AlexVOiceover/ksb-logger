#!/bin/bash

# Load environment variables from project root
cd "$(dirname "$0")/.."
source .env

echo "Extracting code snippets from high-scoring PRs..."
python cli.py extract-code
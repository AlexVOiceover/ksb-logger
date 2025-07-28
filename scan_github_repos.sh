#!/bin/bash

# Exit on error
set -e

# Load environment variables
source .env

# Ensure token is set
if [ -z "$GITHUB_API" ]; then
  echo "Error: GITHUB_API is not set."
  echo "Run: export GITHUB_API=your_token_here"
  exit 1
fi

OUTPUT_FILE="trufflehog_results.json"
echo "{" > $OUTPUT_FILE

# Scan personal repos
echo "Scanning personal repos (AlexVOiceover)..."
trufflehog github --org=AlexVOiceover --token=$GITHUB_API --json >> $OUTPUT_FILE

# Scan organization repos
echo ", \"FoundersAndCoders\": [" >> $OUTPUT_FILE
trufflehog github --org=FoundersAndCoders --token=$GITHUB_API --json >> $OUTPUT_FILE
echo "]}" >> $OUTPUT_FILE

echo "Scan completed. Results saved to $OUTPUT_FILE"

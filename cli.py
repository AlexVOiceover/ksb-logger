#!/usr/bin/env python3
"""
Main CLI entry point for KSB Logger.
This is a thin wrapper around the main CLI in the ksb_logger package.
"""

from ksb_logger.cli import cli

if __name__ == "__main__":
    cli()
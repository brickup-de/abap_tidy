#!/usr/bin/env python3
"""
Run the Clean ABAP to Hugo conversion.
This is a convenience script to run the conversion from the repository root.
"""

import sys

from scripts.main import main

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"Error: conversion failed: {exc}", file=sys.stderr)
        sys.exit(1)

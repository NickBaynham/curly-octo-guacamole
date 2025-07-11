#!/usr/bin/env python3
"""
Simple script to run pytest with output enabled.
"""
import subprocess
import sys

def main():
    """Run pytest with output enabled."""
    cmd = [
        "pdm", "run", "pytest", 
        "-v", "-s", "--tb=short"
    ] + sys.argv[1:]  # Pass through any additional arguments
    
    print("Running pytest with output enabled...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main() 
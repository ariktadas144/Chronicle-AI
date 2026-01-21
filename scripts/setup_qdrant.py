#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant.collections import create_memory_collection

def main():
    print("Setting up Qdrant collection...")
    create_memory_collection()
    print("Collection 'memories' created successfully.")

if __name__ == "__main__":
    main()
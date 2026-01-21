#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant.ingest import ingest_documents, ingest_images

def main():
    print("Ingesting documents into Qdrant...")
    ingest_documents()
    print("Ingesting images into Qdrant...")
    ingest_images()
    print("Data ingestion completed.")

if __name__ == "__main__":
    main()
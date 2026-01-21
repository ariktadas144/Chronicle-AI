#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import json
from memory.memory_manager import MemoryManager
from reasoning.recommendation import RecommendationEngine
from qdrant.ingest import ingest_single_document

def main():
    print("Chronicle AI Demo - Institutional Memory Agent")
    print("=" * 50)

    print("\n1. Ingesting a new document...")
    new_metadata = {
        "department": "Emergency Management",
        "date": "2024-01-15",
        "outcome": "pending",
        "location": "Demo City"
    }
    test_text = "Recent infrastructure improvements have enhanced emergency response capabilities, showing promising results in preliminary tests."
    ingest_single_document(test_text, new_metadata)
    print("New document ingested successfully")

    print("\n2. Running sample queries...")
    with open("data/sample_queries.json", "r") as f:
        queries = json.load(f)

    memory_manager = MemoryManager()
    recommendation_engine = RecommendationEngine()

    for item in queries:
        query = item["query"]
        print(f"\nQuery: {query}")

        memories = memory_manager.retrieve_memories(query)
        print(f"Retrieved {len(memories)} memories")

        recommendation = recommendation_engine.generate_recommendation(query, memories)
        print(f"Recommendation: {recommendation[:300]}...")

        summary = recommendation_engine.get_summary(query, memories)
        print(f"Summary: {summary}")

        print("-" * 50)

if __name__ == "__main__":
    main()
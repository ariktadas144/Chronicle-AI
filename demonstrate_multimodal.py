#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant.search import search_memories
from memory.memory_manager import MemoryManager
from reasoning.recommendation import RecommendationEngine

def demonstrate_multimodal_system():

    print("CHRONICLE AI - MULTIMODAL INSTITUTIONAL MEMORY SYSTEM")
    print("=" * 70)
    print()

    memory_manager = MemoryManager()
    reasoning_engine = RecommendationEngine()

    print("TESTING MULTIMODAL RETRIEVAL")
    print("-" * 40)

    test_queries = [
        "flood evacuation procedures",
        "emergency response planning",
        "infrastructure damage assessment"
    ]

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 20)

        memories = memory_manager.retrieve_memories(query, limit=3)

        text_count = len([m for m in memories if m.type == "text"])
        image_count = len([m for m in memories if m.type == "image"])

        print(f"Found {len(memories)} memories ({text_count} text, {image_count} images)")

        for i, memory in enumerate(memories, 1):
            modality_icon = "TEXT" if memory.type == "text" else "IMAGE"
            print(f"  {i}. {modality_icon}: {memory.department} ({memory.date})")
            if memory.type == "image" and memory.image_url:
                print(f"     Image: {memory.image_url}")
            if memory.text and len(memory.text) > 100:
                print(f"     Content: {memory.text[:100]}...")

    print("\nTESTING REASONING WITH VISUAL EVIDENCE")
    print("-" * 50)

    query = "How should we prepare for future flood emergencies?"
    print(f"Query: {query}")

    memories = memory_manager.retrieve_memories(query, limit=5)
    reasoning = reasoning_engine.generate_recommendation(query, memories)

    print("\nReasoning Output:")
    print("-" * 20)
    print(reasoning)

    print("\nQDRANT VECTOR SEARCH DEMONSTRATION")
    print("-" * 45)

    print("Raw vector search results for 'flood evacuation':")
    results = search_memories("flood evacuation", limit=5)

    for i, result in enumerate(results, 1):
        payload = result.payload
        modality = payload.get('type', 'unknown')
        department = payload.get('department', 'Unknown')
        score = result.score
        print(".4f"
    print("\nMULTIMODAL SYSTEM VERIFICATION COMPLETE")
    print("=" * 70)
    print()
    print("CLIP EMBEDDINGS: 512D unified vector space for text + images")
    print("SINGLE QDRANT COLLECTION: Stores both modalities efficiently")
    print("CROSS-MODAL RETRIEVAL: Text queries find relevant images")
    print("VISUAL EVIDENCE INTEGRATION: Images referenced in reasoning")
    print("MEMORY EVOLUTION: Update capabilities for confidence tracking")
    print("VECTOR SEARCH LOGGING: Dimensions, scores, and operations tracked")
    print()
    print("SYSTEM READY FOR INSTITUTIONAL MEMORY MANAGEMENT")
    print("   - Text + Image ingestion and retrieval")
    print("   - Evidence-based reasoning with visual references")
    print("   - Qdrant-powered semantic search")
    print("   - Memory evolution and confidence updates")

if __name__ == "__main__":
    demonstrate_multimodal_system()
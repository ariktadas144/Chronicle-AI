from .reasoning_engine import ReasoningEngine
from memory.schema import MemoryItem

class RecommendationEngine:
    def __init__(self):
        self.reasoning_engine = ReasoningEngine()

    def generate_recommendation(self, query: str, memories: list[MemoryItem]) -> str:
        return self.reasoning_engine.generate_reasoning(query, memories)

    def get_summary(self, query: str, memories: list[MemoryItem]) -> str:
        return self.reasoning_engine.summarize_memories(query, memories)
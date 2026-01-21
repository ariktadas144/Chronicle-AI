import openai
import os
from reasoning.prompt_templates import REASONING_PROMPT_TEMPLATE
from memory.schema import MemoryItem

class ReasoningEngine:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
            openai.api_base = "https://openrouter.ai/api/v1"
        else:
            print("Warning: OPENAI_API_KEY not set. Reasoning will use basic templates.")

    def generate_reasoning(self, query: str, memories: list[MemoryItem]) -> str:
        if not self.api_key:
            return self._basic_reasoning(query, memories)

        memories_text = "\n".join([
            f"- ID: {m.id}, Department: {m.department}, Date: {m.date}, Outcome: {m.outcome}, Type: {m.type}\n  Content: {m.text if m.text else f'Image: {m.image_url}'}"
            for m in memories
        ])

        prompt = REASONING_PROMPT_TEMPLATE.format(query=query, memories=memories_text)

        response = openai.ChatCompletion.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0
        )

        reasoning_text = response.choices[0].message.content.strip()

        sources = "\n\nSources:\n" + "\n".join([
            f"- {m.department} ({m.date}) - Outcome: {m.outcome} - Type: {m.type}"
            for m in memories
        ])

        return reasoning_text + sources

    def _basic_reasoning(self, query: str, memories: list[MemoryItem]) -> str:
        text_memories = [m for m in memories if m.type == "text"]
        image_memories = [m for m in memories if m.type == "image"]

        reasoning = f"Analysis for query: '{query}'\n\n"
        reasoning += f"Found {len(memories)} relevant memories ({len(text_memories)} text, {len(image_memories)} images).\n\n"

        if image_memories:
            reasoning += "Visual evidence found:\n"
            for img in image_memories:
                reasoning += f"- Image from {img.department} ({img.date}): {img.image_url}\n"
                if img.text:
                    reasoning += f"  Description: {img.text}\n"
            reasoning += "\nThis visual evidence should be considered alongside textual records.\n\n"

        reasoning += "Recommendation: Consider historical patterns and visual evidence in decision making.\n\n"

        sources = "Sources:\n" + "\n".join([
            f"- {m.department} ({m.date}) - {m.type.upper()}"
            for m in memories
        ])

        return reasoning + sources

    def summarize_memories(self, query: str, memories: list[MemoryItem]) -> str:
        if not self.api_key:
            return self._basic_summary(query, memories)

        from .prompt_templates import SUMMARY_PROMPT_TEMPLATE
        memories_text = "\n".join([f"- {m.text if m.text else f'Image: {m.image_url}'} (Outcome: {m.outcome}, Type: {m.type})" for m in memories])
        prompt = SUMMARY_PROMPT_TEMPLATE.format(query=query, memories=memories_text)

        response = openai.ChatCompletion.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.2
        )

        summary_text = response.choices[0].message.content.strip()

        sources = "\n\nSources:\n" + "\n".join([
            f"- {m.department} ({m.date})"
            for m in memories
        ])

        return summary_text + sources

    def _basic_summary(self, query: str, memories: list[MemoryItem]) -> str:
        text_count = len([m for m in memories if m.type == "text"])
        image_count = len([m for m in memories if m.type == "image"])

        summary = f"Summary for '{query}': Found {len(memories)} memories "
        if text_count > 0:
            summary += f"({text_count} text documents"
        if image_count > 0:
            summary += f"{', ' if text_count > 0 else '('}{image_count} images"
        summary += ").\n\n"

        if memories:
            summary += "Key departments involved: " + ", ".join(set(m.department for m in memories)) + "\n"
            outcomes = set(m.outcome for m in memories)
            summary += "Historical outcomes: " + ", ".join(outcomes) + "\n"

        return summary
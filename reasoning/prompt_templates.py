REASONING_PROMPT_TEMPLATE = """
Based on the following historical institutional memories, provide a comprehensive analysis and recommendation for the query: "{query}"

Historical Memories:
{memories}

Please structure your response as follows:
1. Summary of relevant past experiences (including any visual evidence from images)
2. Key lessons learned
3. Evidence-based recommendation
4. Potential risks or considerations

When referencing images or visual evidence, explicitly mention them (e.g., "As shown in the 2019 evacuation route map..." or "The visual evidence from the incident site photograph indicates...").

Ensure your response is grounded in the provided historical data and explain the reasoning clearly.
"""

SUMMARY_PROMPT_TEMPLATE = """
Summarize the following memories in the context of the query: "{query}"

Memories:
{memories}

Provide a concise summary highlighting patterns and outcomes.
"""
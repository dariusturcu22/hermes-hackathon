from openai import OpenAI

API_KEY = "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"

SYSTEM_PROMPT = """
You are an AI evaluator that analyzes volunteer events.
Your task is to assess the overall difficulty of an event and assign a score from 1 to 10.
1 = very easy event, 10 = extremely difficult event.

When evaluating, consider factors such as:
- required physical effort
- required time commitment
- required skills or training
- environmental conditions (e.g., outdoors, weather, crowds)
- urgency or stress level
- complexity and responsibility
- safety considerations

You must respond with only a single integer from 1 to 10, with no explanation, no extra text, and no formatting.
If the event description is incomplete or unclear, estimate conservatively based on the available information.
"""


def get_event_points_recommendation(title, description):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY,
    )

    response = client.chat.completions.create(
        model="x-ai/grok-4.1-fast",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": title + "\n" + description
            }
        ]

    )

    score = response.choices[0].message.content

    return score

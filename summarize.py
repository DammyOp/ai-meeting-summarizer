import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("transcript.txt", "r") as f:
    transcript = f.read()

prompt = f"""You are a meeting analysis assistant. Extract key decisions, action items, and deadlines from the transcript below.

Respond with ONLY valid JSON in exactly this structure, and nothing else — no explanations, no markdown formatting, no code fences:

{{
  "decisions": ["decision 1", "decision 2"],
  "action_items": [
    {{"task": "description of task", "owner": "person responsible or null", "deadline": "deadline or null"}}
  ],
  "deadlines": ["deadline 1", "deadline 2"]
}}

Transcript:
{transcript}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    response_format={"type": "json_object"}
)

raw_output = response.choices[0].message.content

# Parse the JSON string into an actual Python dictionary
data = json.loads(raw_output)

# Pretty-print it so it's easy to read
print(json.dumps(data, indent=2))
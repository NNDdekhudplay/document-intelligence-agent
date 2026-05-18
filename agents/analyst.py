import json
from openai import OpenAI


class AnalystAgent:
    def __init__(self, client: OpenAI):
        self.client = client
        self.name = "AnalystAgent"

    def analyze(self, extracted: dict) -> dict:
        extracted_text = json.dumps(extracted, indent=2)

        response = self.client.chat.completions.create(
            model="openai/gpt-4o-mini",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a document intelligence analyst. Given structured data extracted "
                        "from a document, analyze it for significance and risk. "
                        "Return a JSON object with exactly these keys:\n"
                        "- important_findings: array of 3-5 notable facts or clauses that stand out\n"
                        "- risks: array of potential risks, red flags, or concerning terms (empty array if none)\n"
                        "- action_items: array of things that require follow-up or attention\n"
                        "- overall_assessment: one short sentence summarizing the document's significance\n"
                        "Return only the JSON object. No markdown, no extra text."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Analyze this extracted document data:\n\n{extracted_text}",
                },
            ],
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {
                "important_findings": [],
                "risks": [],
                "action_items": [],
                "overall_assessment": "Analysis could not be parsed.",
                "parse_error": True,
            }

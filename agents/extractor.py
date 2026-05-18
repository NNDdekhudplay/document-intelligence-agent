import json
from openai import OpenAI


class ExtractorAgent:
    def __init__(self, client: OpenAI):
        self.client = client
        self.name = "ExtractorAgent"

    def extract(self, pages: list[dict]) -> dict:
        full_text = "\n\n".join(
            f"--- Page {p['page']} ---\n{p['text']}"
            for p in pages
            if p["text"]
        )

        response = self.client.chat.completions.create(
            model="openai/gpt-4o-mini",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a document extraction specialist. Analyze the provided document text "
                        "and extract structured data. Return a JSON object with exactly these keys:\n"
                        "- document_type: string (e.g. 'Service Agreement', 'Invoice', 'NDA', 'Report')\n"
                        "- names: array of person names found\n"
                        "- organizations: array of company or organization names\n"
                        "- dates: array of dates found (as strings, e.g. '2025-01-15')\n"
                        "- amounts: array of monetary amounts found (as strings, e.g. '$50,000')\n"
                        "- main_topics: array of 3-5 main topics or subjects the document covers\n"
                        "- key_clauses: array of 3-5 important clauses, terms, or obligations\n"
                        "Return only the JSON object. No markdown, no extra text."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Extract structured data from this document:\n\n{full_text}",
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
                "document_type": "Unknown",
                "names": [],
                "organizations": [],
                "dates": [],
                "amounts": [],
                "main_topics": [],
                "key_clauses": [],
                "parse_error": True,
            }

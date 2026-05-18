from openai import OpenAI


class ReportWriterAgent:
    def __init__(self, client: OpenAI):
        self.client = client
        self.name = "ReportWriterAgent"

    def write(self, extracted: dict, analysis: dict) -> str:
        context = (
            f"Document Type: {extracted.get('document_type', 'Unknown')}\n"
            f"Parties: {', '.join(extracted.get('names', []) + extracted.get('organizations', []))}\n"
            f"Dates: {', '.join(extracted.get('dates', []))}\n"
            f"Amounts: {', '.join(extracted.get('amounts', []))}\n"
            f"Main Topics: {', '.join(extracted.get('main_topics', []))}\n"
            f"Key Clauses: {', '.join(extracted.get('key_clauses', []))}\n\n"
            f"Important Findings:\n" + "\n".join(f"- {f}" for f in analysis.get("important_findings", [])) + "\n\n"
            f"Risks Identified:\n" + "\n".join(f"- {r}" for r in analysis.get("risks", [])) + "\n\n"
            f"Action Items:\n" + "\n".join(f"- {a}" for a in analysis.get("action_items", [])) + "\n\n"
            f"Overall Assessment: {analysis.get('overall_assessment', '')}"
        )

        response = self.client.chat.completions.create(
            model="openai/gpt-4o-mini",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional intelligence report writer. "
                        "Write a structured document intelligence report of 300-400 words "
                        "using these exact section headers:\n\n"
                        "## Document Overview\n"
                        "## Key Entities\n"
                        "## Main Findings\n"
                        "## Action Items\n\n"
                        "Write in clear, professional English. "
                        "Document Overview and Key Entities use prose. "
                        "Main Findings and Action Items use bullet points. "
                        "Be direct and informative. Do not pad or repeat content."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Write an intelligence report based on this document data:\n\n{context}",
                },
            ],
        )

        return response.choices[0].message.content.strip()

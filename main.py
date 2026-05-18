import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from agents import PDFReaderAgent, ExtractorAgent, AnalystAgent, ReportWriterAgent

load_dotenv()

console = Console()


def get_pdf_path() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    console.print("[bold yellow]No PDF path provided as argument.[/bold yellow]")
    path = input("Enter path to PDF file: ").strip()
    if not path:
        console.print("[bold red]No path entered. Exiting.[/bold red]")
        sys.exit(1)
    return path


def print_entities_table(extracted: dict):
    table = Table(title="Extracted Entities", border_style="dim", show_lines=True)
    table.add_column("Category", style="bold cyan", min_width=16)
    table.add_column("Values", style="white")

    def fmt(lst): return ", ".join(lst) if lst else "[dim]none found[/dim]"

    table.add_row("Document Type", extracted.get("document_type", "Unknown"))
    table.add_row("Names", fmt(extracted.get("names", [])))
    table.add_row("Organizations", fmt(extracted.get("organizations", [])))
    table.add_row("Dates", fmt(extracted.get("dates", [])))
    table.add_row("Amounts", fmt(extracted.get("amounts", [])))
    table.add_row("Main Topics", fmt(extracted.get("main_topics", [])))
    console.print(table)


def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/bold red] OPENROUTER_API_KEY not found in .env file.")
        console.print("Copy [dim].env.example[/dim] to [dim].env[/dim] and add your key.")
        sys.exit(1)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    pdf_reader = PDFReaderAgent()
    extractor = ExtractorAgent(client)
    analyst = AnalystAgent(client)
    report_writer = ReportWriterAgent(client)

    console.print()
    console.print(Panel.fit(
        "[bold cyan]Document Intelligence Agent[/bold cyan]\n"
        "[dim]Pipeline: PDF Read -> Extract -> Analyze -> Report[/dim]",
        border_style="cyan",
    ))
    console.print()

    while True:
        pdf_path = get_pdf_path()
        console.print()

        try:
            pages = pdf_reader.read(pdf_path)
        except (FileNotFoundError, ValueError) as e:
            console.print(f"  [bold red]Error:[/bold red] {e}")
        else:
            total_chars = sum(len(p["text"]) for p in pages)
            console.print(f"  Extracted [bold]{len(pages)}[/bold] page(s), [bold]{total_chars:,}[/bold] characters total.")
            console.print()

            console.print("[bold blue][2/4] ExtractorAgent[/bold blue] — Extracting entities with gpt-4o-mini...")
            extracted = extractor.extract(pages)
            if extracted.get("parse_error"):
                console.print("  [yellow]Warning:[/yellow] Extraction response could not be parsed.")
            print_entities_table(extracted)
            console.print()

            console.print("[bold magenta][3/4] AnalystAgent[/bold magenta] — Analyzing findings with gpt-4o-mini...")
            analysis = analyst.analyze(extracted)
            if analysis.get("parse_error"):
                console.print("  [yellow]Warning:[/yellow] Analysis response could not be parsed.")
            console.print(f"  Findings identified: [bold]{len(analysis.get('important_findings', []))}[/bold]")
            console.print(f"  Risks flagged:       [bold]{len(analysis.get('risks', []))}[/bold]")
            console.print(f"  Action items:        [bold]{len(analysis.get('action_items', []))}[/bold]")
            console.print()

            console.print("[bold green][4/4] ReportWriterAgent[/bold green] — Writing intelligence report with gpt-4o-mini...")
            report = report_writer.write(extracted, analysis)
            console.print()

            console.print(Panel(
                Text(report),
                title="[bold white]Document Intelligence Report[/bold white]",
                border_style="green",
                padding=(1, 2),
            ))
            console.print()
            console.print("[dim]Pipeline complete.[/dim]")
            console.print()

        try:
            again = console.input("[dim]Press Enter for another PDF, or type 'q' to quit:[/] ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break
        if again == "q":
            break


if __name__ == "__main__":
    main()

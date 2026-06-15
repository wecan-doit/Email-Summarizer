import os
import re
import time
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.status import Status

from fetch_unread import fetch_unread_newsletters, mark_as_read
from web_extractor import extract_article_content
from batch_summarize import summarize_newsletter
from append_to_doc import create_daily_doc, append_summary_to_doc
import json

load_dotenv()
console = Console()

# --- Live Bridge Configuration ---
STATUS_FILE = os.path.join(os.path.dirname(__file__), "..", "dashboard", "status.json")

def update_live_status(step, message, type="msg", progress=0, phase="Stylize"):
    """
    Writes the current system status to a JSON file for the web dashboard.
    """
    status_data = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "step": step,
        "message": message,
        "type": type, # success, error, msg
        "progress": progress,
        "phase": phase,
        "last_updated": time.time()
    }
    try:
        with open(STATUS_FILE, "w") as f:
            json.dump(status_data, f, indent=2)
    except Exception as e:
        # Don't let bridge failures stop the main engine
        pass

def find_read_more_link(body):
    """
    Simple regex to find common 'Read More' URLs.
    """
    links = re.findall(r'(https?://[^\s]+)', body)
    for link in links:
        if any(word in link.lower() for word in ['read', 'story', 'article', 'news']):
            return link
    return None

def main():
    console.print(Panel.fit(
        "[bold cyan]🚀 B.L.A.S.T. System Pilot[/bold cyan]\n[italic white]AI Newsletter Digest Orchestrator[/italic white]",
        border_style="bright_blue"
    ))
    
    snippet_threshold = int(os.getenv("SNIPPET_THRESHOLD", 1000))

    # 1. Extraction
    update_live_status("GMAIL", "Connecting to Gmail API...", phase="Link")
    with console.status("[bold yellow]Step 1: Connecting to Gmail and fetching newsletters...", spinner="dots"):
        try:
            newsletters = fetch_unread_newsletters()
            if not newsletters:
                update_live_status("GMAIL", "No new newsletters found.", type="error", phase="Link")
                console.print("[bold red]No new newsletters found. Terminating.[/bold red]")
                return
            update_live_status("GMAIL", f"Found {len(newsletters)} newsletters in last 48h.", type="success", phase="Architect")
            console.print(f"[bold green]✓ Found {len(newsletters)} new newsletters.[/bold green]")
        except Exception as e:
            update_live_status("SYSTEM", f"Extraction failed: {e}", type="error")
            console.print(f"[bold red]Failed during email extraction: {e}[/bold red]")
            return

    # 2. Summarization & Scraping Loop
    summaries = []
    console.print("\n[bold yellow]Step 2: Processing & Summarizing (Multi-Pass Synthesis)[/bold yellow]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        console=console
    ) as progress_bar:
        task = progress_bar.add_task("[cyan]Processing Newsletters...", total=len(newsletters))
        
        for i, nl in enumerate(newsletters):
            progress_percent = int(((i) / len(newsletters)) * 100)
            update_live_status("GEMINI", f"Summarizing: {nl['subject'][:30]}...", progress=progress_percent, phase="Architect")
            
            progress_bar.update(task, description=f"[cyan]Processing: {nl['subject'][:50]}...")
            try:
                content = nl['body']
                
                if len(content) < snippet_threshold:
                    link = find_read_more_link(content)
                    if link:
                        update_live_status("SCRAPER", f"Scraping external: {link[:30]}...", progress=progress_percent)
                        progress_bar.console.print(f"  [dim]Snippet detected. Scraping link: {link}[/dim]")
                        external_content = extract_article_content(link)
                        if external_content:
                            content = external_content
                
                summary = summarize_newsletter(content, nl['subject'])
                if summary and summary.get('is_relevant'):
                    summaries.append(summary)
                    progress_bar.console.print(f"  [green]✅ Summary generated for {nl['subject'][:40]}...[/green]")
                else:
                    progress_bar.console.print(f"  [yellow]⏩ Skipped: Not relevant or failed filtering.[/yellow]")
            except Exception as e:
                progress_bar.console.print(f"  [red]❌ Failed: {nl['subject'][:40]}... Error: {e}[/red]")
            
            progress_bar.advance(task)

    update_live_status("GEMINI", "Summarization complete.", type="success", progress=100, phase="Stylize")

    # 3. Delivery
    if not summaries:
        update_live_status("SYSTEM", "No relevant items to deliver.", type="error")
        console.print("\n[bold red]No relevant news items found after filtering. Terminating.[/bold red]")
        return

    console.print(f"\n[bold yellow]Step 3: Delivering Intelligence Payload ({len(summaries)} items)[/bold yellow]")
    update_live_status("DOCS", "Creating Daily Digest Doc...", phase="Trigger")
    with console.status("[bold cyan]Creating Google Doc and appending summaries...", spinner="bouncingBar"):
        try:
            doc_title = f"Daily AI & Creator Digest - {datetime.now().strftime('%Y-%m-%d')}"
            doc_id = create_daily_doc(doc_title)
            
            for item in summaries:
                append_summary_to_doc(doc_id, item)
            
            update_live_status("DOCS", "Digest ready in Google Docs.", type="success", phase="Trigger")
            console.print(Panel(
                f"[bold green]Success! Intelligence Digest is ready.[/bold green]\n\n"
                f"[bold white]Doc Link:[/bold white] [link=https://docs.google.com/document/d/{doc_id}]https://docs.google.com/document/d/{doc_id}[/link]",
                title="[bold green]Payload Delivered[/bold green]",
                border_style="green"
            ))
        except Exception as e:
            update_live_status("DOCS", f"Delivery failed: {e}", type="error")
            console.print(f"[bold red]Failed during delivery phase: {e}[/bold red]")
            return

    # 4. Cleanup
    update_live_status("CLEANUP", "Marking processed emails as read...", phase="Trigger")
    with console.status("[bold yellow]Step 4: Cleanup (Marking emails as Read)...", spinner="dots"):
        try:
            for nl in newsletters:
                mark_as_read(nl['message_id'])
            update_live_status("SYSTEM", "All tasks completed successfully.", type="success", phase="Trigger")
            console.print("[bold green]✓ All processed emails marked as READ.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Failed during cleanup: {e}[/bold red]")

    console.print("\n[bold cyan]=== Mission Complete ===[/bold cyan]")

if __name__ == "__main__":
    main()


import time
from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.console import Console
from rich.text import Text
from datetime import datetime, timedelta

DURATION_MINUTES = 10

def format_time(seconds):
    """Convert seconds to HH:MM:SS.mmm format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_remaining = seconds % 60
    whole_seconds = int(seconds_remaining)
    milliseconds = int((seconds_remaining - whole_seconds) * 1000)
    return f"{minutes:02d}:{whole_seconds:02d}.{milliseconds:03d}"

def create_display(seconds_left, total_seconds):
    """Create a styled display for the countdown"""
    table = Table(show_header=False, show_edge=False, box=None)
    
    # Calculate progress percentage
    progress = (1 - (seconds_left / total_seconds)) * 100
    
    # Create styled time remaining text
    time_text = Text(format_time(seconds_left), style="bold cyan")
    status = Text("Stream starts in...", style="yellow")
    
    # Create progress bar
    width = 50
    completed = int((width * progress) / 100)
    bar = "█" * completed + "░" * (width - completed)
    progress_text = Text(f"{bar} {progress:.3f}%", style="blue")
    
    # Add rows to table
    table.add_row(Align(status, align="center"))
    table.add_row(Align(time_text, align="center"))
    table.add_row(Align(progress_text, align="center"))
    
    return table

def countdown():
    """Run a 5-minute countdown timer with millisecond precision"""
    console = Console()
    console.clear()
    
    
    total_seconds = DURATION_MINUTES * 60
    end_time = datetime.now() + timedelta(minutes=DURATION_MINUTES)
    
    with Live(console=console, refresh_per_second=60) as live:  # Increased refresh rate
        while datetime.now() < end_time:
            seconds_left = (end_time - datetime.now()).total_seconds()
            display = create_display(seconds_left, total_seconds)
            live.update(display)
            time.sleep(0.016)  # Approximately 60 FPS refresh rate
        
        # Final display
        final_message = Text("Time HackMatrix Stream", style="bold green")
        live.update(Align(final_message, align="center"))

if __name__ == "__main__":
    try:
        countdown()
    except KeyboardInterrupt:
        Console().print("\n[yellow]Countdown cancelled![/yellow]")

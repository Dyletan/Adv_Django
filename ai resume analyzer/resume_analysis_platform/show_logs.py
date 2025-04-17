import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_analysis_platform.settings')
django.setup()

from analytics.models import LogEntry

def display_logs():
    try:
        logs = LogEntry.objects.using('analytics').all().order_by('timestamp')

        if not logs:
            print("No log entries found.")
            return

        print("\nLog Entries")
        print("-" * 80)
        print(f"{'Timestamp':<25} {'User ID':<20} {'Action':<15} {'Details'}")
        print("-" * 80)

        for log in logs:
            timestamp_str = log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            user_id = log.user_id or 'Anonymous'
            print(f"{timestamp_str:<25} {user_id:<20} {log.action:<15} {log.details}")

    except Exception as e:
        print(f"Error retrieving logs: {e}")

if __name__ == "__main__":
    display_logs()
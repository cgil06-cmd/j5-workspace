#!/usr/bin/env python3
"""Fetch and display upcoming calendar events from iCal URLs."""

import sys
import urllib.request
from datetime import datetime, date, timedelta
from icalendar import Calendar
import pytz

CENTRAL = pytz.timezone("America/Chicago")

CALENDARS = {
    "Personal": "https://calendar.google.com/calendar/ical/cgil06%40gmail.com/private-af629fd2ec26b45e61eda58048c1648d/basic.ics",
    "GCC":      "https://calendar.google.com/calendar/ical/cgilbert%40ourgardencity.com/private-09b86aa6ca8a4f9843b25bfac83ecf22/basic.ics",
}

def fetch_events(days_ahead=2):
    now = datetime.now(CENTRAL)
    cutoff = now + timedelta(days=days_ahead)
    events = []

    for label, url in CALENDARS.items():
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                cal = Calendar.from_ical(resp.read())
            for component in cal.walk():
                if component.name != "VEVENT":
                    continue
                dtstart = component.get("DTSTART")
                if not dtstart:
                    continue
                dt = dtstart.dt
                # Handle all-day events (date only)
                if isinstance(dt, date) and not isinstance(dt, datetime):
                    dt = datetime(dt.year, dt.month, dt.day, 0, 0, tzinfo=CENTRAL)
                elif dt.tzinfo is None:
                    dt = CENTRAL.localize(dt)
                else:
                    dt = dt.astimezone(CENTRAL)
                if now <= dt <= cutoff:
                    summary = str(component.get("SUMMARY", "No title"))
                    events.append((dt, label, summary))
        except Exception as e:
            print(f"  ⚠️ {label}: {e}", file=sys.stderr)

    events.sort(key=lambda x: x[0])
    return events

if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    events = fetch_events(days)
    if not events:
        print("No upcoming events found.")
    else:
        current_day = None
        for dt, label, summary in events:
            day_str = dt.strftime("%A, %b %-d")
            if day_str != current_day:
                print(f"\n📅 {day_str}")
                current_day = day_str
            time_str = dt.strftime("%-I:%M %p") if dt.hour or dt.minute else "All day"
            print(f"  {time_str} — {summary} ({label})")

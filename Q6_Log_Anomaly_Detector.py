"""Q6: Detect failed-login bursts followed by success from a different IP."""
import sys
import re
from collections import defaultdict, deque
from datetime import datetime

LOG_RE = re.compile(r"^(\S+)\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)$", re.I)

def to_minutes(timestamp):
    # Accept HH:MM or ISO-like timestamp whose time portion ends in HH:MM[:SS].
    time_part = timestamp.split("T")[-1]
    match = re.search(r"(\d{2}):(\d{2})(?::\d{2})?$", time_part)
    if not match: raise ValueError(f"Invalid timestamp: {timestamp}")
    hour, minute = map(int, match.groups())
    if hour > 23 or minute > 59: raise ValueError("Invalid time")
    return hour * 60 + minute

def main():
    lines = sys.stdin.read().splitlines()
    try:
        x, window = map(int, lines[0].split())
        n = int(lines[1])
        if x < 1 or window < 1 or len(lines) < n + 2: raise ValueError("Invalid input")
        failures = defaultdict(deque)
        suspicious = {}
        for line in lines[2:n+2]:
            match = LOG_RE.fullmatch(line.strip())
            if not match: continue
            timestamp, user, ip, status = match.groups()
            now = to_minutes(timestamp)
            queue = failures[user]
            while queue and now - queue[0][0] > window:
                queue.popleft()
            if status.upper() == "FAIL":
                queue.append((now, ip, timestamp))
            elif len(queue) >= x and any(old_ip != ip for _, old_ip, _ in queue):
                suspicious.setdefault(user, timestamp)
        for user in sorted(suspicious):
            print(user, suspicious[user])
    except (ValueError, IndexError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()

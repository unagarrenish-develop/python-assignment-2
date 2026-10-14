"""Q1: Extract unique valid .com, .edu and .org email addresses from a text file."""
import re
import sys
from collections import defaultdict

EMAIL_RE = re.compile(r"(?<![A-Za-z0-9._+-])[A-Za-z0-9+._-]+@[A-Za-z0-9.-]+\.(?:com|edu|org)(?![A-Za-z0-9.-])", re.I)

def main():
    if len(sys.argv) != 2:
        print("Usage: python Q1_Email_Intelligence_Extractor.py text_file.txt", file=sys.stderr)
        return
    users = defaultdict(set)
    try:
        with open(sys.argv[1], encoding="utf-8", errors="replace") as handle:
            for line in handle:
                for match in EMAIL_RE.finditer(line):
                    email = match.group(0).lower()
                    # Basic domain-label validation prevents malformed dotted domains.
                    domain = email.split("@", 1)[1]
                    labels = domain.split(".")
                    if any(not label or label.startswith("-") or label.endswith("-") for label in labels):
                        continue
                    users[domain].add(email)
        for domain in sorted(users):
            emails = users[domain]
            print(domain, len(emails), min(emails))
    except OSError as exc:
        print(f"File error: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()

"""Q2: Rank products extracted from saved HTML pages.
Expected markup may contain product-name, price and rating labels/classes.
"""
import re
import sys
from html import unescape
from html.parser import HTMLParser

class ProductParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.products = []
        self.current = None
        self.capture = None
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").lower()
        if any(key in classes for key in ("product", "listing")):
            if self.current:
                self.products.append(self.current)
            self.current = {"name": "", "price_text": "", "rating_text": ""}
        if self.current:
            if "name" in classes or "title" in classes:
                self.capture = "name"
            elif "price" in classes:
                self.capture = "price_text"
            elif "rating" in classes or "stars" in classes:
                self.capture = "rating_text"

    def handle_data(self, data):
        if self.current and self.capture:
            self.current[self.capture] += data.strip()

    def handle_endtag(self, tag):
        if self.capture:
            self.capture = None

    def close(self):
        super().close()
        if self.current:
            self.products.append(self.current)
            self.current = None

def parse_products(path):
    parser = ProductParser()
    with open(path, encoding="utf-8", errors="replace") as handle:
        parser.feed(handle.read())
    found = []
    for item in parser.products:
        name = " ".join(item["name"].split())
        price_match = re.search(r"\d[\d,]*(?:\.\d{1,2})?", item["price_text"])
        rating_match = re.search(r"\d+(?:\.\d+)?", item["rating_text"])
        if not name or not price_match or not rating_match:
            continue
        price = float(price_match.group().replace(",", ""))
        rating = float(rating_match.group())
        if price >= 0 and 0 <= rating <= 5:
            found.append((name, price, rating))
    return found

def main():
    try:
        lines = sys.stdin.read().splitlines()
        p, k = map(int, lines[0].split())
        if not (1 <= p <= 5000 and 1 <= k <= 1000) or len(lines) < p + 1:
            raise ValueError("Invalid p, k, or missing file paths")
        products = {}
        for path in lines[1:p+1]:
            for name, price, rating in parse_products(path.strip()):
                # For duplicate names, keep the best rating then the lower price.
                old = products.get(name.casefold())
                if old is None or (-rating, price, name) < (-old[2], old[1], old[0]):
                    products[name.casefold()] = (name, price, rating)
        ranked = sorted(products.values(), key=lambda x: (-x[2], x[1], x[0]))[:k]
        for name, price, rating in ranked:
            print(name, f"{price:g}", f"{rating:g}")
    except (OSError, ValueError, IndexError) as exc:
        print(f"Error: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()

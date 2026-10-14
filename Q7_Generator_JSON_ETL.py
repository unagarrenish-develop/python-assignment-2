"""Q7: Streaming JSON Lines ETL; corrupted rows are counted per device when identifiable."""
import json
import sys
from collections import defaultdict

def records(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                item = json.loads(line)
                if not isinstance(item, dict): raise ValueError("JSON row must be an object")
                yield item, None
            except (json.JSONDecodeError, ValueError) as exc:
                yield None, str(exc)

def main():
    if len(sys.argv) != 2:
        print("Usage: python Q7_Generator_JSON_ETL.py readings.jsonl", file=sys.stderr)
        return
    stats = defaultdict(lambda: {"count": 0, "min": None, "max": None, "sum": 0.0, "corrupted": 0})
    try:
        for item, error in records(sys.argv[1]):
            device = str(item.get("device_id", "UNKNOWN")) if item else "UNKNOWN"
            if item is None:
                stats[device]["corrupted"] += 1; continue
            try:
                device = str(item["device_id"])
                temp = float(item["temperature_c"])
                humidity = float(item["humidity"])
                if not 0 <= humidity <= 100: raise ValueError("Humidity outside 0..100")
                # Convert Celsius to Fahrenheit for the transformed reading, while summaries use Celsius.
                _temperature_f = temp * 9 / 5 + 32
                s = stats[device]
                s["count"] += 1; s["sum"] += temp
                s["min"] = temp if s["min"] is None else min(s["min"], temp)
                s["max"] = temp if s["max"] is None else max(s["max"], temp)
            except (KeyError, TypeError, ValueError):
                stats[device]["corrupted"] += 1
        for device in sorted(stats):
            s = stats[device]
            if s["count"]:
                print(f"{device} count={s['count']} min={s['min']:g} max={s['max']:g} "
                      f"avg={s['sum']/s['count']:.2f} corrupted={s['corrupted']}")
            else:
                print(f"{device} count=0 min=N/A max=N/A avg=N/A corrupted={s['corrupted']}")
    except OSError as exc:
        print(f"File error: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()

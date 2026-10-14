"""Q10: Clean student marks CSV, create summary CSV and three PNG charts.
Install: pip install matplotlib
CSV should include enrollment, name, and one or more subject columns.
"""
import csv
import os
import sys
import math

def main():
    if len(sys.argv) != 3:
        print("Usage: python Q10_Data_Visualization_Dashboard.py marks.csv output_folder", file=sys.stderr)
        return
    input_path, output_dir = sys.argv[1], sys.argv[2]
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        os.makedirs(output_dir, exist_ok=True)
        with open(input_path, newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or not {"enrollment", "name"}.issubset(reader.fieldnames):
                raise ValueError("CSV requires enrollment and name columns")
            subjects = [c for c in reader.fieldnames if c not in ("enrollment", "name")]
            if not subjects: raise ValueError("At least one subject column is required")
            cleaned, grade_counts = [], {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
            subject_values = {subject: [] for subject in subjects}
            for row in reader:
                clean = {"enrollment": row["enrollment"], "name": row["name"]}
                for subject in subjects:
                    raw = (row.get(subject) or "").strip()
                    try:
                        mark = float(raw)
                        if not 0 <= mark <= 100: raise ValueError
                    except ValueError:
                        mark = None
                    clean[subject] = "" if mark is None else f"{mark:g}"
                    if mark is not None:
                        subject_values[subject].append(mark)
                        grade_counts["A" if mark >= 90 else "B" if mark >= 80 else
                                     "C" if mark >= 70 else "D" if mark >= 60 else "F"] += 1
                cleaned.append(clean)
        with open(os.path.join(output_dir, "cleaned_marks.csv"), "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["enrollment", "name"] + subjects)
            writer.writeheader(); writer.writerows(cleaned)
        with open(os.path.join(output_dir, "summary.csv"), "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle); writer.writerow(["subject", "count", "min", "max", "average"])
            for subject, values in subject_values.items():
                writer.writerow([subject, len(values), min(values) if values else "",
                                 max(values) if values else "", f"{sum(values)/len(values):.2f}" if values else ""])
        plt.figure(figsize=(7, 4)); plt.bar(grade_counts.keys(), grade_counts.values())
        plt.title("Grade Distribution"); plt.xlabel("Grade"); plt.ylabel("Number of marks")
        plt.tight_layout(); plt.savefig(os.path.join(output_dir, "grade_distribution.png")); plt.close()
        averages = [sum(v)/len(v) if v else 0 for v in subject_values.values()]
        plt.figure(figsize=(max(7, len(subjects)*0.7), 4)); plt.bar(subjects, averages)
        plt.title("Subject-wise Average"); plt.ylabel("Average marks"); plt.xticks(rotation=30, ha="right")
        plt.tight_layout(); plt.savefig(os.path.join(output_dir, "subject_average.png")); plt.close()
        totals = []
        for row in cleaned:
            marks = [float(row[s]) for s in subjects if row[s] != ""]
            if marks: totals.append((row["name"], sum(marks)/len(marks)))
        top = sorted(totals, key=lambda x: (-x[1], x[0]))[:10]
        plt.figure(figsize=(max(7, len(top)*0.7), 4)); plt.bar([x[0] for x in top], [x[1] for x in top])
        plt.title("Top Performers"); plt.ylabel("Average marks"); plt.xticks(rotation=30, ha="right")
        plt.tight_layout(); plt.savefig(os.path.join(output_dir, "top_performers.png")); plt.close()
        print("cleaned_marks.csv")
        print("summary.csv")
        print("grade_distribution.png")
        print("subject_average.png")
        print("top_performers.png")
    except (OSError, ValueError, ImportError, csv.Error) as exc:
        print(f"Error: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()

"""Q8: Maximum-score path with right, down, diagonal moves and count of optimal paths."""
import sys

MOD = 1_000_000_007

def solve(matrix):
    n, m = len(matrix), len(matrix[0])
    neg = None
    previous_score = [neg] * m
    previous_count = [0] * m
    for i in range(n):
        current_score, current_count = [neg] * m, [0] * m
        for j in range(m):
            value = matrix[i][j]
            if value is None: continue
            if i == 0 and j == 0:
                current_score[j], current_count[j] = value, 1
                continue
            candidates = []
            if j > 0 and current_score[j-1] is not None:
                candidates.append((current_score[j-1], current_count[j-1]))
            if previous_score[j] is not None:
                candidates.append((previous_score[j], previous_count[j]))
            if j > 0 and previous_score[j-1] is not None:
                candidates.append((previous_score[j-1], previous_count[j-1]))
            if candidates:
                best = max(score for score, _ in candidates)
                current_score[j] = best + value
                current_count[j] = sum(count for score, count in candidates if score == best) % MOD
        previous_score, previous_count = current_score, current_count
    return previous_score[-1], previous_count[-1]

def main():
    try:
        first = sys.stdin.readline().split()
        n, m = map(int, first)
        if n < 1 or m < 1 or n > 2000 or m > 2000: raise ValueError("Invalid matrix dimensions")
        matrix = []
        for _ in range(n):
            tokens = sys.stdin.readline().split()
            if len(tokens) == 1 and len(tokens[0]) == m and "X" in tokens[0]:
                tokens = list(tokens[0])
            if len(tokens) != m: raise ValueError("Each row must contain m cells")
            row = []
            for token in tokens:
                row.append(None if token.upper() == "X" else int(token))
            matrix.append(row)
        score, count = solve(matrix)
        print("IMPOSSIBLE" if score is None else f"{score} {count}")
    except (ValueError, TypeError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()

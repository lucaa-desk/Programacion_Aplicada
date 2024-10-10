from collections import Counter

def most_frequent_count(arr):
    if not arr:
        return 0
    counts = Counter(arr)
    return max(counts.values())

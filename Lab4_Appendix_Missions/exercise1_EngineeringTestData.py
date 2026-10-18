# Exercise 1: Engineering Test Data Organizer

from collections import Counter, defaultdict
from statistics import mean

LAST_NAME = input("Enter your last name: ").strip().upper()
SEED_NUM = int(input("Enter your seed number: "))
FAVORITE_ARTIST = input("Enter your favorite artist: ").strip().upper()

sources = [f"{LAST_NAME}_T{i}" for i in range(1, 6)]
categories = ["TEMPERATURE", "VOLTAGE", "CURRENT", "PRESSURE", "SPEED"]

# Generate values using the seed and artist character positions
artist_values = [ord(char) for char in FAVORITE_ARTIST if char.isalpha()]
if not artist_values:
    artist_values = [1]

records = []

for i, source in enumerate(sources):
    category = categories[i]
    value = (SEED_NUM + artist_values[i % len(artist_values)] + i * 3) % 100 + 1

    records.append({
        "source": source,
        "category": category,
        "value": value
    })

# Add multiple measurements under two categories
records.append({
    "source": sources[0],
    "category": "TEMPERATURE",
    "value": (SEED_NUM + artist_values[0] + 10) % 100 + 1
})
records.append({
    "source": sources[1],
    "category": "VOLTAGE",
    "value": (SEED_NUM + artist_values[0] + 20) % 100 + 1
})

# Include one repeated source/category record
records.append(records[0].copy())

# Organize records by source and category
organized = defaultdict(lambda: defaultdict(list))

for record in records:
    organized[record["source"]][record["category"]].append(
        record["value"]
    )

# Identify repeated and distinct records
record_counts = Counter(
    (r["source"], r["category"], r["value"]) for r in records
)
repeated = [item for item, count in record_counts.items() if count > 1]
distinct = set(
    (r["source"], r["category"], r["value"]) for r in records
)

# Numerical summaries by category
category_values = defaultdict(list)

for record in records:
    category_values[record["category"]].append(record["value"])

print("\n===== GENERATED TEST DATA =====")
for record in records:
    print(record)

print("\n===== ORGANIZED TEST DATA =====")
for source, category_data in organized.items():
    print(source, dict(category_data))

print("\n===== REPEATED AND DISTINCT DATA =====")
print("Repeated records:", repeated)
print("Total records:", len(records))
print("Distinct records:", len(distinct))

print("\n===== NUMERICAL SUMMARIES =====")
for category, values in sorted(category_values.items()):
    print(
        f"{category}: Count={len(values)}, "
        f"Min={min(values)}, Max={max(values)}, "
        f"Average={mean(values):.2f}"
    )

print("\n===== ORDERED RESULTS =====")
ordered_records = sorted(
    records, key=lambda r: (r["category"], r["source"], r["value"])
)
for record in ordered_records:
    print(record)

print("\n===== FINAL SUMMARY =====")
print("Student:", LAST_NAME)
print("Favorite artist:", FAVORITE_ARTIST)
print("Total records:", len(records))
print("Distinct records:", len(distinct))
print("Repeated record combinations:", len(repeated))
print("Categories measured:", len(category_values))
print("Sources tested:", len(sources))
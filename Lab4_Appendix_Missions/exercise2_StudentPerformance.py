# Exercise 2: Student Performance Data Analyzer

from collections import Counter, defaultdict
from statistics import mean

LAST_NAME = input("Enter your last name: ").strip().upper()
SEED_NUM = int(input("Enter your seed number: "))
FAVORITE_ARTIST = input("Enter your favorite artist: ").strip().upper()

students = [f"{LAST_NAME}_S{i}" for i in range(1, 6)]
subjects = [
    "PROGRAMMING", "MATHEMATICS", "ELECTRONICS",
    "PHYSICS", "ENGLISH"
]

artist_values = [ord(c) for c in FAVORITE_ARTIST if c.isalpha()]
if not artist_values:
    artist_values = [1]

records = []

# Generate student-subject scores
for i, student in enumerate(students):
    for j, subject in enumerate(subjects):
        score = (
            SEED_NUM + artist_values[(i + j) % len(artist_values)]
            + i * 7 + j * 5
        ) % 41 + 60

        records.append({
            "student": student,
            "subject": subject,
            "score": score
        })

# Add one repeated student-subject record
records.append(records[0].copy())

# Add one incomplete record
records.append({
    "student": students[0],
    "subject": "PHYSICS",
    "score": None
})

def get_category(score):
    if score is None:
        return "INCOMPLETE"
    elif score >= 90:
        return "EXCELLENT"
    elif score >= 80:
        return "GOOD"
    elif score >= 75:
        return "PASSING"
    else:
        return "FAILING"

# Organize records by student and subject
organized = defaultdict(dict)

for record in records:
    organized[record["student"]][record["subject"]] = record["score"]

# Detect repeated student-subject combinations
pair_counts = Counter(
    (r["student"], r["subject"]) for r in records
)
repeated = [pair for pair, count in pair_counts.items() if count > 1]

incomplete = [r for r in records if r["score"] is None]
valid_records = [r for r in records if r["score"] is not None]

# Add performance categories
for record in records:
    record["category"] = get_category(record["score"])

print("\n===== GENERATED PERFORMANCE RECORDS =====")
for record in records:
    print(record)

print("\n===== ORGANIZED STUDENT DATA =====")
for student, data in sorted(organized.items()):
    print(student, data)

print("\n===== REPEATED AND INCOMPLETE RECORDS =====")
print("Repeated student-subject pairs:", repeated)
print("Incomplete records:", incomplete)

print("\n===== PERFORMANCE CATEGORIES =====")
category_counts = Counter(r["category"] for r in records)
for category, count in sorted(category_counts.items()):
    print(category, ":", count)

print("\n===== STUDENT SUMMARIES =====")
for student in students:
    scores = [
        r["score"] for r in valid_records
        if r["student"] == student
    ]
    print(
        student,
        "Valid scores:", len(scores),
        "Average:", f"{mean(scores):.2f}" if scores else "N/A"
    )

print("\n===== SUBJECT SUMMARIES =====")
for subject in subjects:
    scores = [
        r["score"] for r in valid_records
        if r["subject"] == subject
    ]
    print(
        subject,
        "Valid scores:", len(scores),
        "Average:", f"{mean(scores):.2f}" if scores else "N/A"
    )

print("\n===== ORDERED RESULTS =====")
ordered = sorted(
    records,
    key=lambda r: (
        r["student"], r["subject"],
        -1 if r["score"] is None else r["score"]
    )
)
for record in ordered:
    print(record)

print("\n===== FINAL PERFORMANCE SUMMARY =====")
print("Total records:", len(records))
print("Valid scores:", len(valid_records))
print("Incomplete records:", len(incomplete))
print("Repeated student-subject pairs:", len(repeated))
print("Students:", len(students))
print("Subjects:", len(subjects))
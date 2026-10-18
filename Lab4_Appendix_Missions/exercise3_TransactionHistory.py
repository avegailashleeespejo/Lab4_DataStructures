# Exercise 3: Transaction History Analyzer

from collections import Counter, defaultdict

LAST_NAME = input("Enter your last name: ").strip().upper()
SEED_NUM = int(input("Enter your seed number: "))
FAVORITE_ARTIST = input("Enter your favorite artist: ").strip().upper()

customers = [f"{LAST_NAME}_C{i}" for i in range(1, 6)]

prices = {
    "NOTEBOOK": 35.00,
    "PEN": 10.00,
    "USB": 250.00,
    "HEADPHONES": 350.00,
    "CALCULATOR": 180.00
}

products = list(prices.keys())

artist_values = [ord(c) for c in FAVORITE_ARTIST if c.isalpha()]
if not artist_values:
    artist_values = [1]

transactions = []

# Generate transactions using seed and artist character positions
for i, customer in enumerate(customers):
    for j in range(2):
        product_index = (
            SEED_NUM + artist_values[(i + j) % len(artist_values)]
            + i + j
        ) % len(products)

        product = products[product_index]
        quantity = (
            SEED_NUM + artist_values[(i + j) % len(artist_values)]
            + i + j
        ) % 5 + 1

        transactions.append({
            "customer": customer,
            "product": product,
            "quantity": quantity,
            "price": prices[product],
            "total": quantity * prices[product]
        })

# Add a repeated customer-product purchase
transactions.append(transactions[0].copy())

# Organize data and calculate summaries
customer_totals = defaultdict(float)
customer_counts = Counter()
product_totals = defaultdict(float)
product_quantities = Counter()
purchase_counts = Counter()

for transaction in transactions:
    customer = transaction["customer"]
    product = transaction["product"]
    total = transaction["total"]
    quantity = transaction["quantity"]

    customer_totals[customer] += total
    customer_counts[customer] += 1
    product_totals[product] += total
    product_quantities[product] += quantity
    purchase_counts[(customer, product)] += 1

repeated_purchases = {
    pair: count for pair, count in purchase_counts.items()
    if count > 1
}

print("\n===== GENERATED TRANSACTIONS =====")
for transaction in transactions:
    print(transaction)

print("\n===== REPEATED AND DISTINCT DATA =====")
print("Total transaction records:", len(transactions))
print("Distinct customer-product pairs:", len(purchase_counts))
print("Repeated purchases:", repeated_purchases)
print("Distinct customers:", len(set(t["customer"] for t in transactions)))
print("Distinct products:", len(set(t["product"] for t in transactions)))

print("\n===== TRANSACTION VALUES =====")
for transaction in transactions:
    print(
        transaction["customer"], transaction["product"],
        "Total: PHP", f'{transaction["total"]:.2f}'
    )

print("\n===== CUSTOMER SUMMARIES =====")
for customer in sorted(customer_totals):
    print(
        customer,
        "Transactions:", customer_counts[customer],
        "Total spent: PHP", f"{customer_totals[customer]:.2f}"
    )

print("\n===== PRODUCT SUMMARIES =====")
for product in products:
    print(
        product,
        "Quantity sold:", product_quantities[product],
        "Sales: PHP", f"{product_totals[product]:.2f}"
    )

print("\n===== ORDERED RESULTS =====")
ordered = sorted(
    transactions,
    key=lambda t: (t["customer"], t["product"], t["total"])
)
for transaction in ordered:
    print(transaction)

print("\n===== OVERALL TRANSACTION SUMMARY =====")
print("Total records:", len(transactions))
print(
    "Total sales: PHP",
    f'{sum(t["total"] for t in transactions):.2f}'
)
print("Number of customers:", len(set(t["customer"] for t in transactions)))
print("Number of products:", len(set(t["product"] for t in transactions)))
print("Repeated purchase combinations:", len(repeated_purchases))
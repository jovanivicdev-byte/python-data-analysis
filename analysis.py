
import csv
from collections import defaultdict

sales = [
    {"product": "Laptop", "quantity": 3, "price": 950},
    {"product": "Mouse", "quantity": 12, "price": 25},
    {"product": "Keyboard", "quantity": 8, "price": 60},
    {"product": "Monitor", "quantity": 5, "price": 220},
    {"product": "Laptop", "quantity": 2, "price": 950},
]

revenue_by_product = defaultdict(float)

for item in sales:
    revenue = item["quantity"] * item["price"]
    revenue_by_product[item["product"]] += revenue

total_revenue = sum(revenue_by_product.values())

print("SALES ANALYSIS REPORT")
print("-" * 30)

for product, revenue in sorted(
    revenue_by_product.items(),
    key=lambda item: item[1],
    reverse=True
):
    print(f"{product}: ${revenue:,.2f}")

print("-" * 30)
print(f"Total revenue: ${total_revenue:,.2f}")

with open("sales_report.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Product", "Revenue"])

    for product, revenue in revenue_by_product.items():
        writer.writerow([product, revenue])

print("Report saved to sales_report.csv")
  

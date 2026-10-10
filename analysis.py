
"""Analyze sample product sales and export a report and a chart."""

import csv
from collections import defaultdict
from html import escape
from pathlib import Path

# Example data for this learning project (not real company sales).
SALES = [
    {"product": "Laptop", "quantity": 3, "price": 850.0},
    {"product": "Mouse", "quantity": 12, "price": 25.0},
    {"product": "Keyboard", "quantity": 8, "price": 60.0},
    {"product": "Monitor", "quantity": 5, "price": 220.0},
    {"product": "Laptop", "quantity": 2, "price": 850.0},
]


def analyze_sales(sales):
    """Aggregate units sold and revenue for each product."""
    totals = defaultdict(lambda: {"quantity": 0, "revenue": 0.0})
    for sale in sales:
        item = totals[sale["product"]]
        item["quantity"] += sale["quantity"]
        item["revenue"] += sale["quantity"] * sale["price"]

    rows = [
        {"product": name, "quantity": data["quantity"], "revenue": data["revenue"]}
        for name, data in totals.items()
    ]
    return sorted(rows, key=lambda row: row["revenue"], reverse=True)


def save_csv(rows, filename="sales_report.csv"):
    """Save a reusable CSV report."""
    with Path(filename).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["product", "quantity", "revenue"])
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "revenue": f'{row["revenue"]:.2f}'})


def save_svg_chart(rows, filename="sales_chart.svg"):
    """Create a horizontal bar chart without third-party packages."""
    width = 900
    height = 110 + 64 * len(rows)
    max_revenue = max((row["revenue"] for row in rows), default=1)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="#f8fafc"/>',
        '<text x="30" y="48" font-family="Arial" font-size="26" '
        'font-weight="bold" fill="#0f172a">Revenue by Product (USD)</text>',
    ]
    for index, row in enumerate(rows):
        y = 85 + index * 64
        bar_width = 510 * row["revenue"] / max_revenue
        product = escape(row["product"])
        parts += [
            f'<text x="30" y="{y + 23}" font-family="Arial" font-size="19" '
            f'fill="#334155">{product}</text>',
            f'<rect x="200" y="{y}" width="{bar_width:.1f}" height="34" '
            'rx="5" fill="#0284c7"/>',
            f'<text x="{215 + bar_width:.1f}" y="{y + 23}" '
            'font-family="Arial" font-size="18" fill="#0f172a">'
            f'${row["revenue"]:,.2f}</text>',
        ]
    parts.append("</svg>")
    Path(filename).write_text("\n".join(parts), encoding="utf-8")


def main():
    rows = analyze_sales(SALES)
    print("SALES ANALYSIS REPORT")
    print("-" * 40)
    for row in rows:
        print(f'{row["product"]}: {row["quantity"]} units | ${row["revenue"]:,.2f}')
    print("-" * 40)
    print(f'Total revenue: ${sum(row["revenue"] for row in rows):,.2f}')
    print(f'Total units sold: {sum(row["quantity"] for row in rows)}')
    save_csv(rows)
    save_svg_chart(rows)
    print("Created sales_report.csv and sales_chart.svg")


if __name__ == "__main__":
    main()

import csv


def load_sales(filename):
    sales = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["quantity"] = int(row["quantity"])
            row["price"] = float(row["price"])
            row["revenue"] = row["quantity"] * row["price"]
            sales.append(row)

    return sales


def total_revenue(sales):
    total = 0

    for sale in sales:
        total += sale["revenue"]

    return total


def average_order_value(sales):
    return total_revenue(sales) / len(sales)


def top_product(sales):
    product_revenue = {}

    for sale in sales:
        product = sale["product"]

        if product not in product_revenue:
            product_revenue[product] = 0

        product_revenue[product] += sale["revenue"]

    best_product = max(product_revenue, key=product_revenue.get)
    return best_product, product_revenue[best_product]


def top_category(sales):
    category_revenue = {}

    for sale in sales:
        category = sale["category"]

        if category not in category_revenue:
            category_revenue[category] = 0

        category_revenue[category] += sale["revenue"]

    best_category = max(category_revenue, key=category_revenue.get)
    return best_category, category_revenue[best_category]


def print_recommendation(product, category):
    print()
    print("Business Recommendation:")
    print(
        "The business should focus on promoting",
        product,
        "because it generated the most revenue."
    )
    print(
        "The strongest category was",
        category,
        "so future marketing campaigns could highlight that category."
    )


def main():
    sales = load_sales("sales_data.csv")

    print("SMALL BUSINESS SALES ANALYZER")
    print("-----------------------------")

    total = total_revenue(sales)
    average = average_order_value(sales)
    product, product_revenue = top_product(sales)
    category, category_revenue = top_category(sales)

    print("Total Revenue: $" + str(round(total, 2)))
    print("Average Order Value: $" + str(round(average, 2)))
    print("Top Product:", product)
    print("Top Product Revenue: $" + str(round(product_revenue, 2)))
    print("Top Category:", category)
    print("Top Category Revenue: $" + str(round(category_revenue, 2)))

    print_recommendation(product, category)


if __name__ == "__main__":
    main()

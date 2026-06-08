import csv


def load_csv(filename):
    """
    Reads a CSV file and returns a list of dictionaries.
    Each dictionary represents one row from the file.
    """
    data = []

#opens the CSV files and turns them into a list of dictionaries
    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data.append(row)

    return data

#finds what the product's name is based on the product ID
def find_product_name(products, product_id):
    for product in products:
        if product["product_id"] == product_id:
            return product["product_name"]
#will print this if the product ID is missing or wrong
    return "Unknown Product"

#finds what the product's category is based on the product ID
def find_product_category(products, product_id):
    for product in products:
        if product["product_id"] == product_id:
            return product["category"]

    return "Unknown Category"

#Determines if a customer is new or returning
def find_customer_type(customers, customer_id):
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer["customer_type"]

    return "Unknown Customer Type"


def prepare_sales_data(orders, products, customers):
    """
    Combines orders, products, and customers into one cleaned dataset.
    """
    #creating a new dictionary called "sale"
    sales = []

    for order in orders:
        quantity = int(order["quantity"])
        unit_price = float(order["unit_price"])
        revenue = quantity * unit_price

        product_id = order["product_id"]
        customer_id = order["customer_id"]

        sale = {
            "order_id": order["order_id"],
            "order_date": order["order_date"],
            "customer_id": customer_id,
            "product_id": product_id,
            "product_name": find_product_name(products, product_id),
            "category": find_product_category(products, product_id),
            "customer_type": find_customer_type(customers, customer_id),
            "quantity": quantity,
            "unit_price": unit_price,
            "revenue": revenue
        }

        sales.append(sale)

    return sales


def total_revenue(sales):
    total = 0

    for sale in sales:
        total += sale["revenue"]

    return total


def average_order_value(sales):
    return total_revenue(sales) / len(sales)

#creates a dictionary that tracks revenue of each product
def top_product(sales):
    product_revenue = {}

    for sale in sales:
        product = sale["product_name"]

        if product not in product_revenue:
            product_revenue[product] = 0

        product_revenue[product] += sale["revenue"]
    #finds the product with the highest revenue.
    best_product = max(product_revenue, key=product_revenue.get)
    return best_product, product_revenue[best_product]


def top_category(sales):
    category_revenue = {}

    for sale in sales:
        category = sale["category"]

        if category not in category_revenue:
            category_revenue[category] = 0

        category_revenue[category] += sale["revenue"]
    #finds the category with the most revenue.
    best_category = max(category_revenue, key=category_revenue.get)
    return best_category, category_revenue[best_category]


def customer_type_revenue(sales):
    revenue_by_type = {}

    for sale in sales:
        customer_type = sale["customer_type"]

        if customer_type not in revenue_by_type:
            revenue_by_type[customer_type] = 0
        #finds out who makes the most revenue, new or returning customers
        revenue_by_type[customer_type] += sale["revenue"]

    return revenue_by_type

#taking the dictionary from the previous function and printing it
def print_customer_type_revenue(sales):
    revenue_by_type = customer_type_revenue(sales)

    print()
    print("Revenue by Customer Type:")

    for customer_type in revenue_by_type:
        revenue = revenue_by_type[customer_type]
        print(customer_type + ": $" + str(round(revenue, 2)))


def print_recommendation(best_product, best_category):
    print()
    print("Business Recommendation:")
    print("The business should focus on promoting " + best_product + " because it generated the most revenue.")
    print("The strongest category was " + best_category + ", so future marketing campaigns could highlight that category.")


def main():
    orders = load_csv("orders.csv")
    products = load_csv("products.csv")
    customers = load_csv("customers.csv")

    sales = prepare_sales_data(orders, products, customers)

    total = total_revenue(sales)
    average = average_order_value(sales)
    best_product, product_revenue = top_product(sales)
    best_category, category_revenue = top_category(sales)

    print("SMALL BUSINESS SALES ANALYZER")
    print("-----------------------------")
    print("Total Orders:", len(sales))
    print("Total Revenue: $" + str(round(total, 2)))
    print("Average Order Value: $" + str(round(average, 2)))
    print("Top Product:", best_product)
    print("Top Product Revenue: $" + str(round(product_revenue, 2)))
    print("Top Category:", best_category)
    print("Top Category Revenue: $" + str(round(category_revenue, 2)))

    print_customer_type_revenue(sales)
    print_recommendation(best_product, best_category)


if __name__ == "__main__":
    main()

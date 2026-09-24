TotalUnitsProcessed = 0
failedEntries = 0
run = True





def get_valid_input():
    global failedEntries

    while True:
        product_name = input("Enter product name (or 'quit' to exit): ")

        if product_name == "quit":
            return "quit", 0
        
        stock_quantity = input("Enter quantity: ")

        if stock_quantity.isdigit() and int(stock_quantity) > 0:
            return product_name, stock_quantity
        
        else:
            print("Invalid! Enter ONLY positive numbers.")
            failedEntries += 1

def load_inventory():
    with open('inventory.txt', 'r') as file:
        orders = file.read()

    if orders == "":
        inventory = []

    else:
        inventory = eval(orders)

    print("Current Orders:")

    for order in inventory:
        print(f"{order[0]}, {order[1]}, {order[2]}")

    return inventory


def add_product(inventory, name, amount):

    serial_number = 1001 + len(inventory)


    inventory.append([serial_number, name, amount])

    
    print("New Order Added:")

    print(f"{serial_number}, {name}, {amount}")

    print("Order successfully added to inventory.txt")

    return inventory

def save_inventory(inventory):
    with open("inventory.txt", "w") as file:
        file.write(str(inventory))
    
        
# def calculate_tax(amount):
#     tax = amount * 0.10
#     return tax


def generate_report(total_units, failed_attempts):
    print("\n===== AUDIT REPORT =====")
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


inventory = load_inventory()

while run:
    product_name, stock_quantity = get_valid_input()

    if product_name == "quit":
        save_inventory(inventory)
        load_inventory()
        break

    else:
        add_product(inventory, product_name, stock_quantity)
        

        # inventory = process_delivery(inventory, product_name)
        # TotalUnitsProcessed += product_name

        # tax = calculate_tax(product_name)

        # print("Current inventory:", inventory, "units")
        # print("Tax for this delivery: $", format(tax, ".2f"))
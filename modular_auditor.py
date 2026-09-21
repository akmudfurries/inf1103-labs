TotalUnitsProcessed = 0
failedEntries = 0
inventory = 0
run = True


def get_valid_input():
    global failedEntries

    while True:
        quantity = input("Enter stock quantity (or 'quit' to exit): ")

        if quantity == "quit":
            return quantity

        elif quantity.isdigit() and int(quantity) > 0:
            return int(quantity)

        print("Invalid! Enter ONLY positive numbers.")
        failedEntries += 1


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts):
    print("\n===== AUDIT REPORT =====")
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


while run:
    quantity = get_valid_input()

    if quantity == "quit":
        generate_report(TotalUnitsProcessed, failedEntries)
        break

    elif inventory + quantity > 500:
        print("Total stock limit reached!")
        failedEntries += 1
        generate_report(TotalUnitsProcessed, failedEntries)
        break

    else:
        inventory = process_delivery(inventory, quantity)
        TotalUnitsProcessed += quantity

        tax = calculate_tax(quantity)

        print("Current inventory:", inventory, "units")
        print("Tax for this delivery: $", format(tax, ".2f"))
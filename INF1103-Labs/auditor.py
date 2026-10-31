TotalUnitsProcessed = 0
failedEntries = 0
inventory = 0
run = True

while run == True:
    quantity = 0
    quantity = input("Enter stock quantity (or 'quit' to exit): ")

    if quantity.isdigit():

            quantity = int(quantity)

            if quantity > 0:
                    inventory += quantity
                    if inventory > 500:

                            inventory -= quantity

                            run = False
                            print("Total stock limit reached!")
                            print("Total Units Processed: ", inventory)
                            print("Number of Failed/Rejected Entries: ", failedEntries)
                    
                    else:
                           print("Current inventory: ", inventory, "units")
                           
           
    elif quantity == "quit" :
        run = False

        print("===== AUDIT REPORT =====")
        
        print("Total Units Processed: ", inventory)
        print("Number of Failed/Rejected Entries: ", failedEntries)
        break

    else:
        print("Invalid! Enter ONLY positive numbers.")
        failedEntries += 1    

    
        


        
        

    
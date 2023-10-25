# Modules
import os
import csv

# Set path for files
csvpath = os.path.join("Resources","budget_data.csv")
txtpath = os.path.join("analysis","budget_analysis.txt")

# variables
total_months = 0
total_profit_loss = 0
profit_change = 0
average_change = 0
changes = []
change_max = 0
change_max_date = 0
change_min = 0
change_min_date = 0
total_change = 0
pp = 0

# Open the CSV using the UTF-8 encoding
with open(csvpath, encoding='UTF-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    # read the header row first, (skip this step if there is no header)
    csv_header = next(csvreader)

    # Loop through rows
    for row in csvreader:

        # calculate profit/loss changes from one period to another
        # Use conditional as there is no change if it's the first month of the period
        if total_months != 0:
            profit_change = int(row[1]) - pp

            # append changes to list
            changes.append(profit_change)
        
            # add changes
            total_change = total_change + profit_change

            # determine if that change is bigger or smaller than max and min
            if profit_change > change_max:
                change_max = profit_change
                change_max_date = row[0]
            elif profit_change < change_min:
                change_min = profit_change
                change_min_date = row[0]

        # define previous profit/loss for next period
        pp = int(row[1])

        # add 1 to a month counter
        total_months = total_months + 1

        # add the profit loss to the variable
        total_profit_loss = total_profit_loss + int(row[1])

    #calculate average change
    average_change = round(total_change / (total_months - 1),2)

# Create output using fromatted strings
output = (
    f"Financial Analysis\n"
    f"----------------------------\n"
    f"Total Months: {total_months}\n"
    f"Total: {total_profit_loss}\n"
    f"Average Change: {average_change}\n"
    f"Greatest Increase in Profits: {change_max_date} (${change_max})\n"
    f"Greatest Decrease in Profits: {change_min_date} (${change_min})\n"
)
# print out KPIs
print(output)
with open(txtpath,"w") as txtfile:
    txtfile.write(output)
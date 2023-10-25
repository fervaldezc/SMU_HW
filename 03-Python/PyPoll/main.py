# Modules
import os
import csv

# Set path for files
csvpath = os.path.join("Resources","election_data.csv")
txtpath = os.path.join("analysis","election_analysis.txt")

# variables
total_votes = 0
candidate = ""
candidates = {}
votes = {}
winner = ""
winner_votes = 0

# Open the CSV using the UTF-8 encoding
with open(csvpath, encoding='UTF-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    # read the header row first
    csv_header = next(csvreader)

    # Loop through rows
    for row in csvreader:

        # count votes for each candidate
        # use a dictionary where key = candidate and value = number of votes
        # if the candidate is in the dictionary then add  1 vote to the value, if not, add a new key and a vote

        candidate = row[2]

        if candidate in candidates.keys():
            candidates[candidate] += 1
        else:
            candidates[candidate] = 1
        
        # add 1 to a month counter
        total_votes = total_votes + 1

    for candidate in candidates.keys():
        votes = candidates[candidate]

        if votes > winner_votes:
            winner_votes = votes
            winner = candidate


# Create output using fromatted strings
output = (
    f"Election Results\n"
    f"----------------------------\n"
    f"Total votes: {total_votes}\n"
    f"----------------------------\n")

for candidate in candidates.keys():
    percentage_votes = round(100*candidates[candidate]/total_votes,3)
    newline = f"{candidate}: {percentage_votes}% ({candidates[candidate]})\n"
    output += newline

newline = (
    f"----------------------------\n"
    f"Winner: {winner}\n"
    f"----------------------------\n")
output += newline

# print out KPIs
print(output)
with open(txtpath,"w") as txtfile:
    txtfile.write(output)

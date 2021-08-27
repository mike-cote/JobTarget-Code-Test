# import needed modules for parsing CSV files
# we'll use the default csv module for this exercise
import csv as c

# read the data from the given csv file, with separate lists for columns and rows
columns = []
rows = []
with open('data.csv', 'r') as csvfile:
    csvreader = c.reader(csvfile)
    columns = next(csvreader)  # get column headers
    for row in csvreader:
        rows.append(row)

# ----------------------------------------------------
# First Task: generate a list of 50 counties with highest average cost to acquire customer
# We will use a dictionary of counties (and their state), paired with a 2-length list containing
# the total costs in that county and the number of customers in that county
def high_county_spend():
    print("Generating list of 50 counties with highest average cost to acquire customer")
    counties = {}
    # go through all the rows in the csv file
    # if the county appearing in the row is already in the counties dictionary, update the dictionary
    # otherwise, add the county to the dictionary
    for row in rows:
        if row[6] + ',' + row[7] in counties:
            counties[row[6] + ',' + row[7]] = [(counties[row[6] + ',' + row[7]])[0] + int(row[10][1:]), (counties[row[6] + ',' + row[7]])[1] + 1]
        else:
            counties[row[6] + ',' + row[7]] = [int(row[10][1:]), 1]
    # We now have a dictionary containing all unique counties, their total costs, and their total number of customers
    # We can use this to determine the average cost of acquiring a customers in every county, and store this information
    # in a new list, sort it by cost, and save it to a new csv file

    # create a new list for county average costs
    county_average_costs = []
    # go through the counties dictionary, pulling out needed information, doing necessary calculations, and
    # adding to county average costs list
    for county in counties:
        county_average_costs.append([county, counties[county][0] / counties[county][1]])
    # sort this list based on calculated average cost
    county_average_costs.sort(key = lambda x: x[1], reverse = True)

    # Write the top 50 counties into a properly-named csv file
    # Create column headers for new csv file
    headers = ["County Name and State", "Average Acquirement Cost ($)"]
    # create and write to new file, using previously created headers
    # use a while loop to limit the number of counties saved to the CSV file,
    # also use another value to maintain the last-added value, and continue adding
    # counties with that value even if this brings the total numbers of counties
    # included to above 50 (in other words, in the event of a tie for 50th highest cost county,
    # include all counties in the tie)
    # to not go above the desired amount (in this case, 50)
    with open('high_county_spend.csv', 'w', newline='') as file:
        writer = c.writer(file)
        writer.writerow(headers)
        i = 0       # value to be incremented as counties are added, to limit number of counties added
        cur_value = float("inf")   # value to store current value being added, to be used for adding in tied values
        running = True
        over_50 = False         # Boolean to update if over 50 counties are included due to tied values
        while running:
            if i < 50:      # if there are less than 50 counties, add next county to file
                writer.writerow(county_average_costs[i])
                cur_value = county_average_costs[i][1]
                i += 1
            elif i >= 50 and county_average_costs[i][1] == cur_value:   # if there are greater than or equal to
                writer.writerow(county_average_costs[i])                # 50 counties, but next county has an equal
                cur_value = county_average_costs[i]                     # cost to acquire as previous county,
                i += 1                                                  # add county to file
                over_50 = True                                          # update over_50 to show that over 50 counties
                                                                        # were added
            else:
                running = False                                         # Otherwise, stop adding to file
        # Print short message alerting that over 50 counties are shown in file due to
        # tied average costs to acquire
        if over_50:
            print("""Due to multiple counties being tied for the 50th highest average cost to acquire a customer,
            there are over 50 counties included in the generated file.""")
    print("""List of counties with highest cost to acquire customers 
            generated in file high_county_spend.csv""")
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Second Task: Generate a list of aggregate monthly spending by each state
# We will do this in a similar manner to the way in which task 1 was accomplished
# We will use a dictionary of states that are paired with a running sum of that state's
# monthly spending
def state_revenue():
    print("Generating list of state revenues")
    states = {}
    # go through all the rows in the csv file
    # if the state appearing in the row is already in the states dictionary, update the dictionary
    # otherwise, add the state to the dictionary
    for row in rows:
        if row[7] in states:
            states[row[7]] = states[row[7]] + int(row[9][1:])
        else:
            states[row[7]] = int(row[9][1:])

    # Write the states into a properly-named csv file
    # Create column headers for new csv file
    headers = ["State", "Monthly Spending ($)"]
    # create and write to new file, using previously created headers
    with open('state_revenue.csv ', 'w', newline='') as file:
        writer = c.writer(file)
        writer.writerow(headers)
        for state in states:
            writer.writerow([state, states[state]])
    print("List of state revenues generated in file state_revenue.csv")
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Third Task: Generate a list of the 25 customers that produce the best annual net revenue
# Again, we will do this in a similar manner to the way in which tasks 1 and 2 were accomplished
# We will use a dictionary of customers (companies) that are paired with that customer's annual
# spending (Monthly Spending * 12) minus their Cost to Acquire
def best_customers():
    print("Generating list of best customers")
    customers = {}
    # go through all the rows in the csv file
    # if the customer appearing in the row is not already in the customers dictionary, update the dictionary
    # with their calculated, but throw a print statement to alert that a company appears twice in the data
    # (since we keep track of both the company name and employee name this could happen, not sure if it would mean anything
    # but I figured it would be better to note any cases in which this happened)
    # otherwise, add the company and its annual revenue to the dictionary
    for row in rows:
        if row[3] in customers:
            customers[row[3]] = customers[row[3]] + (12 * int(row[9][1:])) - int(row[10][1:])
            print("The company", + row[3] + " appeared multiple times!")
        else:
            customers[row[3]] = (12 * int(row[9][1:])) - int(row[10][1:])

    # create a new list for companies and the revenues they produce
    customer_revenues = []
    # go through the customers dictionary, pulling out needed information, and
    # adding to customer revenues list
    # calculations are handled in the above dictionary, so they do not need to be done here
    for customer in customers:
        customer_revenues.append([customer, customers[customer]])
    # sort this list based on highest annual net revenue
    customer_revenues.sort(key = lambda x: x[1], reverse = True)

    # Write the Companies into a properly-named csv file
    # Create column headers for new csv file
    headers = ["Company", "Annual Net Revenue ($)"]
    # create and write to new file, using previously created headers
    # use a while loop to limit the number of companies saved to the CSV file
    # to not go above the desired amount (in this case, 25)
    with open('best_customers.csv', 'w', newline='') as file:
        writer = c.writer(file)
        writer.writerow(headers)
        i = 0
        while i < 25:
            writer.writerow(customer_revenues[i])
            i += 1
    print("List of best customers generated in file best_customers.csv")

running = True
while running:
    task_selected = input("""Please choose which data you wish to retrieve:
                          1: Generate a list of the top 50 counties with highest average cost to acquire a customer
                          2: Generate a list of the aggregate spending of all states
                          3: Generate a list of the top 25 customers with the highest annual net revenue
                          0: Quit
                          """)
    if int(task_selected) == 1:
        high_county_spend()
    elif int(task_selected) == 2:
        state_revenue()
    elif int(task_selected) == 3:
        best_customers()
    elif int(task_selected) == 0:
        print("Ending Program")
        running = False
    else:
        print("Please enter a valid input")

# Possible improvements:
# - Create a simplistic GUI rather than using command line interface
# - Allow for file selection, output directory selection, naming of generated file(s)
#   - check loaded files for correct formatting
# - Find more efficient ways of loading / parsing csv files in the event of larger sets of data - perhaps
#   with the pandas library instead of csv?
# - add in ways to allow for task 1 and task 3 to be completed even if the data being used does not have
#   the minimum number of rows needed for these tasks (in other words, handle errors resulting from having data with
#   less than 50 counties or less than 25 customers)
# - Show path to generated files

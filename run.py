import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

#Every Google account has an IAM configuration
#IAM =Identity and Access Management. This configuration specifies what the iser has access to
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ] # scope lists the api's that the program should access in order to run
    # SCOPE is a const in python write them as full captial

    # create another const named creds
CREDS = Credentials.from_service_account_file('creds.json')#To do this, we call the from_service_account_file  method of the Credentials class,and we pass it our creds.json file name.
    
    #Using the  with_scopes method of the creds object,and pass it our scope variable.
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    #finally, we can access our  love_sandwiches sheet, 
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user via the 
    terminal, which must be a string of 6 numbers
    separted bycommas. The loop will repeatedly request data, until it is valid
    """
    while True:
        print("Please enter sales data from the last market: ")
        print("Data should be six numbers, separted by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        #this will get rid of the ","the user entered between values
        sales_data = data_str.split(",")# returns the broken up values as a list e.g['10','11','21']
        validate_data(sales_data)

        if  validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data

# pass it a parameter  of “values” which will be our sales data list.
def validate_data(values):
    """
    Inside the try, converts all string values into intergers.
    Raises valeError if strings cannot be converted into int, or
    if there arent exaclty 6 values.
    """

    try:
        [int(value) for value in values]#for each individual value in the values  list, convert that value into an integer
        if len(values) != 6:
            raise ValueError(
            f"Exactly 6 values required, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True
  
def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """

    print(f"Updating {worksheet} worksheet ...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """

    print("Calculating surplus data...\n")
    # using the worksheet method of the sheet  variable again, we’ll let the sheet know that  
    # we want the data from the “stock” worksheet 
    stock = SHEET.worksheet("stock").get_all_values()#gspread library called get_all_values() to  fetch all of the cells from our stock worksheet.
    stock_row = stock[-1]#The simplest way is to use a slice.In this case stock with square brackets giving it the list index of -1. This will slice the final item from the list and return it to the new stock variable

    surplus_data =[]
   
    for stock,sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    

    return surplus_data

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])# slicing colon because we want to slice multiply values from the list 

    return columns
def calculate_stock_data(data):
    """
    Calculate the average stock for each item type,adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average*1.1 # this add 10% too the average
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,"surplus")
    sales_columns = get_last_5_entries_sales()  
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to love sandwiches Data Automation")

main()

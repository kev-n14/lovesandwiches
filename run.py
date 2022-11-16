import gspread
from google.oauth2.service_account import Credentials


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
    Get sales figures input from the user
    """

    print("Please enter sales data from the last market: ")
    print("Data should be six numbers, separted by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")

get_sales_data()

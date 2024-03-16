from openpyxl import load_workbook
import tabula
import pandas as pd

def read_and_process_table(pdf_path, page_number):
    # Read the PDF into a DataFrame for the specified page
    
    df = tabula.read_pdf(pdf_path, pages=page_number, multiple_tables=True)

    # Check if any tables were found on the specified page
    if df:
        # Assuming you want to use the first table found
        table_df = df[0]

        # Specify the headers for the Excel file
        excel_headers = ['Date', 'Transaction Type','NAV', 'Amount', 'Price', 'Number of Units','Balance of Units']

        # Set the DataFrame headers
        table_df.columns = excel_headers

        # Generate Excel file
        excel_output_path = 'output_table.xlsx'
        
        #Remove NAV column as it is same as Price
        if 'NAV' in table_df.columns:
            table_df = table_df.drop(columns=['NAV'])
        
        #Remove Balancer of Units column as it will be calculated later in excel
        if 'Balance of Units' in table_df.columns:
            table_df = table_df.drop(columns=['Balance of Units'])

        # Remove numbers after decimal point in the 'Amount' column
        table_df['Date'] = pd.to_datetime(table_df['Date']).dt.date
        table_df['Amount'] = table_df['Amount'].str.split('\r').str[0].str.replace(',', '').astype(float)
       
        # Save the modified DataFrame to the same Excel file
        table_df.to_excel(excel_output_path, index=False)

        
        print(f"Excel file '{excel_output_path}' generated successfully.")

    else:
        print(f"No tables found on page {page_number}.")

# Replace 'account.pdf' with the path to your PDF file
# Set page_number to 2 for the second page
read_and_process_table('account.pdf', 2)

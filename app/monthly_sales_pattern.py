import pandas as pd

def load_sales_data(file_path):
    sales_df = pd.read_csv(file_path)
    
    # Assuming you have a date column; if not, you might need to create it based on the existing data
    if 'date' in sales_df.columns:
        sales_df['month'] = pd.to_datetime(sales_df['date']).dt.month
    else:
        # If there is no date column, determine how to create a 'month' column based on your data
        # Here is a dummy example where you might just assign 1 for January (you would adjust as needed)
        sales_df['month'] = 1  # Replace with actual logic to derive month
    
    return sales_df

def analyze_sales_patterns(sales_df):
    # Assuming 'product_name' is the name of your product column
    monthly_sales = sales_df.groupby(['month', 'product_name']).sum().reset_index()  
    return monthly_sales

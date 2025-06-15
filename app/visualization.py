import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px

def load_data(file_path):
    """Load data from a CSV file."""
    return pd.read_csv(file_path)

def process_data(df):
    """Process the sales data to get total sales per product."""
    # Group by product name and count the occurrences
    product_sales = df.groupby('product_name').size().reset_index(name='Total Orders')
    return product_sales


def visualize_sales(product_sales):
    """Visualize total sales of all products with an interactive bar chart."""
    fig = px.bar(
        product_sales.sort_values('Total Orders', ascending=False),
        x='Total Orders',
        y='product_name',
        title='Total Products Sold',
        labels={'Total Orders': 'Total Orders', 'product_name': 'Product Name'},
        height=800
    )
    
    fig.update_layout(
        xaxis_title='Total Orders',
        yaxis_title='Product Name',
        yaxis=dict(autorange="reversed"),  # Reverse the y-axis to show the highest first
        template='plotly_white'
    )
    
    fig.show()

if __name__ == '__main__':
    # Set the correct file path
    data_file_path = r'E:\Design project\data\monthly_sales.csv'  # Change to .csv extension
    print("Data file path:", data_file_path)  # Print for debugging
    sales_data = load_data(data_file_path)

    # Process the sales data
    product_sales = process_data(sales_data)
    
    # Visualize the sales data
    visualize_sales(product_sales)

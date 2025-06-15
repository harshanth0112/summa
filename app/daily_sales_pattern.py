# app/daily_sales_pattern.py
import pandas as pd
import matplotlib.pyplot as plt

def load_sales_data(file_path):
    """
    Loads the daily sales data from the specified CSV file.
    Assumes columns: ['date', 'product', 'sales'].
    """
    sales_df = pd.read_csv(file_path, parse_dates=['date'])
    sales_df['day_of_week'] = sales_df['date'].dt.day_name()  # Add day of the week
    sales_df['week'] = sales_df['date'].dt.isocalendar().week  # Add week number
    return sales_df

def analyze_daily_patterns(sales_df):
    """
    Analyzes daily sales patterns across weeks and products.
    """
    # Group sales by day of the week and product, summing sales
    daily_sales = sales_df.groupby(['week', 'day_of_week', 'product']).sum().reset_index()
    
    # Pivot table to have products as columns and days of the week as rows
    pivot_table = daily_sales.pivot_table(index=['week', 'day_of_week'], columns='product', values='sales', aggfunc='sum')
    
    # Plot sales trends for each day of the week
    pivot_table.plot(kind='line', figsize=(12, 6), title='Daily Sales Patterns by Week')
    plt.xlabel('Week and Day of the Week')
    plt.ylabel('Sales')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()
    
    return pivot_table

def recommend_daily_supply(pivot_table):
    """
    Provides daily demand and supply recommendations based on sales patterns.
    """
    recommendations = {}

    # Example: Increase supply for products with high demand on specific days
    for product in pivot_table.columns:
        high_demand_days = pivot_table[product][pivot_table[product] > pivot_table[product].mean()].index
        recommendations[product] = f"Increase supply on: {', '.join([f'{day[1]} (Week {day[0]})' for day in high_demand_days])}"
    
    return recommendations

if __name__ == "__main__":
    # Load daily sales data and analyze patterns
    sales_df = load_sales_data(r'C:\Users\h6411\Desktop\Design project (2)\Design project\data\monthly_sales.csv')  # Replace with actual daily sales data path
    pivot_table = analyze_daily_patterns(sales_df)
    
    # Provide daily supply recommendations
    recommendations = recommend_daily_supply(pivot_table)
    
    print("Daily Supply Recommendations:")
    for product, recommendation in recommendations.items():
        print(f"{product}: {recommendation}")

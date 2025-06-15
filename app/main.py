# app/main.py
import pandas as pd
from flask import Blueprint, render_template
from mlxtend.frequent_patterns import apriori
from scipy import sparse

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    print(f"Looking for index.html in: {bp.template_folder}")
    return render_template('index.html')


@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/visualize')
def visualize():
    # Load and process sales data
    data_file_path = r'E:\Design project\data\monthly_sales.csv'
    sales_data = pd.read_csv(data_file_path)  # Example of loading CSV
    product_sales = sales_data.groupby('product_name').size().reset_index(name='Total Orders')
    return render_template('visualization.html', product_sales=product_sales)

# Load the dataset
def load_order_data(file_path):
    return pd.read_csv(file_path).sample(frac=0.1, random_state=1)

# Prepare data for Apriori
def preprocess_for_apriori(orders_df):
    basket = orders_df.pivot_table(index='order_id', columns='product_name', aggfunc='size', fill_value=0)
    basket_sparse = sparse.csr_matrix(basket.values > 0)
    return basket_sparse, basket.columns.tolist()

# Find frequent itemsets using Apriori
def find_frequent_itemsets(basket_sparse, product_names, min_support=0.01):
    basket_df = pd.DataFrame(basket_sparse.toarray(), columns=product_names)
    frequent_itemsets = apriori(basket_df, min_support=min_support, use_colnames=True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    return frequent_itemsets

# Display top N frequent itemsets
def display_top_frequent_itemsets(frequent_itemsets, top_n=5):
    pair_itemsets = frequent_itemsets[frequent_itemsets['length'] == 2].sort_values(by='support', ascending=False).head(top_n)
    all_top_itemsets = frequent_itemsets.sort_values(by='support', ascending=False).head(top_n)

    print(f"Top {top_n} Most Frequent Pairs (2-item combinations):")
    print(pair_itemsets[['itemsets', 'support']])
    
    print(f"\nTop {top_n} Most Frequent Itemsets:")
    print(all_top_itemsets[['itemsets', 'support']])

# New function for combo offers
def apriori_combo_offer(basket_sparse, product_names, min_support=0.01):
    frequent_itemsets = find_frequent_itemsets(basket_sparse, product_names, min_support)
    return frequent_itemsets

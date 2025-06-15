import pandas as pd
import xml.etree.ElementTree as ET

def load_xml_data(file_path):
    """Load data from an XML file."""
    try:
        tree = ET.parse(file_path)
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

    root = tree.getroot()
    
    # Extract data into a list of dictionaries
    data = []
    for order in root.findall('order'):
        order_id = order.get('order_id')
        user_id = order.get('user_id')
        for product in order.find('products').findall('product'):
            product_id = product.get('product_id')
            product_name = product.get('product_name')
            quantity = product.get('quantity')
            data.append({
                'order_id': order_id,
                'user_id': user_id,
                'product_id': product_id,
                'product_name': product_name,
                'quantity': int(quantity)  # Convert quantity to integer
            })

    # Create a DataFrame from the extracted data
    sales_data_df = pd.DataFrame(data)
    return sales_data_df

def main():
    # Set the path to your XML file
    xml_file_path = r'E:\Design project\data\monthly_sales.csv'  # Change this to your actual XML file path

    # Read and print the contents of the XML file for debugging
    try:
        with open(xml_file_path, 'r') as file:
            xml_content = file.read()
            print("XML Content:")
            print(xml_content)  # Print the raw content of the XML file
    except Exception as e:
        print(f"Error reading XML file: {e}")
        return

    # Load and process the XML data
    sales_data_df = load_xml_data(xml_file_path)

    # Display the DataFrame
    print("Loaded Sales Data:")
    print(sales_data_df.head())  # Display the first few rows for verification

if __name__ == '__main__':
    main()

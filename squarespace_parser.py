import csv
from product_classes import SquarespaceProduct, SquarespaceVariant

def _parse_float_safe(value_str, default=None):
    """Safely parses a string to a float, returning a default if parsing fails."""
    if value_str is None or value_str == '':
        return default
    try:
        return float(value_str)
    except ValueError:
        return default

def _parse_int_safe(value_str, default=None):
    """Safely parses a string to an int, returning a default if parsing fails."""
    if value_str is None or value_str == '':
        return default
    try:
        return int(value_str)
    except ValueError:
        return default

def _split_string_to_list(value_str, delimiter=',', strip_whitespace=True):
    """Splits a string by a delimiter and optionally strips whitespace from items."""
    if not value_str:
        return []
    items = value_str.split(delimiter)
    if strip_whitespace:
        return [item.strip() for item in items if item.strip()]
    return items

def parse_squarespace_csv(csv_filepath):
    """
    Parses a Squarespace CSV file and returns a list of SquarespaceProduct objects.

    Args:
        csv_filepath (str): The path to the Squarespace CSV file.

    Returns:
        list: A list of SquarespaceProduct objects.
    """
    products = []
    current_product = None

    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product_id = row.get('Product ID [Non Editable]')

                if product_id:  # This row represents a new product
                    # Parse product fields
                    categories_str = row.get('Categories', '')
                    tags_str = row.get('Tags', '')
                    hosted_images_str = row.get('Hosted Image URLs', '')

                    current_product = SquarespaceProduct(
                        product_id=product_id,
                        product_type=row.get('Product Type'),
                        product_page=row.get('Product Page'),
                        product_url=row.get('Product URL'),
                        title=row.get('Title'),
                        description=row.get('Description'),
                        sku=row.get('SKU'), # Main product SKU
                        option_name_1=row.get('Option Name 1'), # Main product option
                        option_value_1=row.get('Option Value 1'), # Main product option value
                        price=_parse_float_safe(row.get('Price')),
                        sale_price=_parse_float_safe(row.get('Sale Price')),
                        on_sale=row.get('On Sale', '').lower() == 'true',
                        stock=_parse_int_safe(row.get('Stock')), # Main product stock
                        categories=_split_string_to_list(categories_str, delimiter=','),
                        tags=_split_string_to_list(tags_str, delimiter=','),
                        weight=_parse_float_safe(row.get('Weight')),
                        length=_parse_float_safe(row.get('Length')),
                        width=_parse_float_safe(row.get('Width')),
                        height=_parse_float_safe(row.get('Height')),
                        visible=row.get('Visible', '').lower() == 'yes' or row.get('Visible', '').lower() == 'true',
                        hosted_image_urls=_split_string_to_list(hosted_images_str, delimiter=' ')
                    )
                    products.append(current_product)

                # Check for variant information in any row, even if it's a product row (for single-variant products)
                # A row is a variant if 'Variant ID [Non Editable]' exists OR if it's a product row with variant-like options
                # but we only add it as a variant if it's NOT the main product row itself (already processed)
                variant_id = row.get('Variant ID [Non Editable]')

                # If it's not a product row (product_id is empty) OR if it is a product row BUT has a distinct variant ID
                # This logic is to capture variants listed under a product.
                # The primary way to identify a variant is by the absence of 'Product ID [Non Editable]'
                # OR the presence of 'Variant ID [Non Editable]' that might be different from a combined product/variant row.

                # A simpler distinction: if product_id was found, we've made a product.
                # Now, if there's variant-specific info (like Variant ID or option names different from main product), it's a variant.
                # The prompt implies: if no "Product ID", it's a variant of the *previous* product.

                if not product_id: # This row is definitely a variant of the current_product
                    if current_product:
                        variant = SquarespaceVariant(
                            variant_id=row.get('Variant ID [Non Editable]'), # This should exist for variant rows
                            sku=row.get('SKU'), # Variant SKU
                            option_name_1=row.get('Option Name 1'),
                            option_value_1=row.get('Option Value 1'),
                            option_name_2=row.get('Option Name 2'),
                            option_value_2=row.get('Option Value 2'),
                            option_name_3=row.get('Option Name 3'),
                            option_value_3=row.get('Option Value 3'),
                            price=_parse_float_safe(row.get('Price')), # Variant price
                            sale_price=_parse_float_safe(row.get('Sale Price')), # Variant sale price
                            on_sale=row.get('On Sale', '').lower() == 'true', # Variant on_sale
                            stock=_parse_int_safe(row.get('Stock')), # Variant stock
                            weight=_parse_float_safe(row.get('Weight')), # Variant weight
                            length=_parse_float_safe(row.get('Length')), # Variant length
                            width=_parse_float_safe(row.get('Width')),   # Variant width
                            height=_parse_float_safe(row.get('Height'))  # Variant height
                        )
                        current_product.variants.append(variant)
                    else:
                        # This case should ideally not happen in a well-formed CSV: a variant row before any product.
                        # Handle error or log warning if necessary. For now, skipping.
                        print(f"Warning: Found variant-like row without a current product: {row}")
                        pass

    except FileNotFoundError:
        print(f"Error: The file {csv_filepath} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while parsing the CSV file: {e}")
        return []

    return products

if __name__ == '__main__':
    # Example Usage (assuming you have a dummy.csv or a real Squarespace CSV)
    # Create a dummy CSV for testing
    dummy_csv_content = """Product ID [Non Editable],Product Type,Product Page,Product URL,Title,Description,SKU,Option Name 1,Option Value 1,Option Name 2,Option Value 2,Price,Sale Price,On Sale,Stock,Categories,Tags,Weight,Length,Width,Height,Visible,Hosted Image URLs,Variant ID [Non Editable]
p1,PHYSICAL,/shop/p1,http://example.com/p1,Product 1,Desc 1,SKU1,Color,Red,,50,40,TRUE,10,"Cat1, Cat2","Tag1, Tag2",1,2,3,4,Yes,"img1.jpg img2.jpg",v1_p1
,,,,Variant for P1 SKU1-Red,SKU1-Red,Color,Red,,50,40,TRUE,10,,,,,,,,
,,,,Variant for P1 SKU1-Blue,SKU1-Blue,Color,Blue,,55,45,FALSE,5,,,,,,,,v2_p1
p2,SERVICE,/shop/p2,http://example.com/p2,Product 2,Desc 2,SKU2,,,,60,,FALSE,100,"Cat3","Tag3",0.5,1,1,1,Yes,"img3.jpg",
"""
    dummy_csv_filepath = 'dummy_squarespace.csv'
    with open(dummy_csv_filepath, 'w', newline='', encoding='utf-8') as f:
        f.write(dummy_csv_content)

    print(f"Attempting to parse '{dummy_csv_filepath}'...")
    parsed_products = parse_squarespace_csv(dummy_csv_filepath)

    if parsed_products:
        for product in parsed_products:
            print(f"Product: {product.title} (ID: {product.product_id}), SKU: {product.sku}, Price: {product.price}")
            print(f"  Description: {product.description}")
            print(f"  Categories: {product.categories}")
            print(f"  Tags: {product.tags}")
            print(f"  Images: {product.hosted_image_urls}")
            print(f"  Visible: {product.visible}")
            print(f"  Stock: {product.stock}")
            if hasattr(product, 'option_name_1') and product.option_name_1: # Check if main product has options
                 print(f"  Main Product Option: {product.option_name_1} - {product.option_value_1}")


            if product.variants:
                print("  Variants:")
                for variant in product.variants:
                    print(f"    Variant ID: {variant.variant_id}, SKU: {variant.sku}, Price: {variant.price}, Stock: {variant.stock}")
                    options = []
                    if variant.option_name_1 and variant.option_value_1:
                        options.append(f"{variant.option_name_1}: {variant.option_value_1}")
                    if variant.option_name_2 and variant.option_value_2:
                        options.append(f"{variant.option_name_2}: {variant.option_value_2}")
                    if variant.option_name_3 and variant.option_value_3:
                        options.append(f"{variant.option_name_3}: {variant.option_value_3}")
                    if options:
                        print(f"      Options: {', '.join(options)}")
            print("-" * 20)
    else:
        print("No products parsed or an error occurred.")

    # Clean up dummy file
    import os
    os.remove(dummy_csv_filepath)
    print(f"Cleaned up '{dummy_csv_filepath}'.")
</tbody>

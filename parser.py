import csv
from product_classes import Product, Variant

def get_option_names(row_dict):
    names = []
    for i in range(1, 7): # Option Name 1 to Option Name 6
        name = row_dict.get(f"Option Name {i}")
        if name:
            names.append(name)
        else:
            break # Stop if an option name is not found
    return names

def get_option_values(row_dict, num_options):
    values = []
    for i in range(1, num_options + 1):
        value = row_dict.get(f"Option Value {i}", "") # Default to empty string if not found
        values.append(value)
    return values

def parse_bool(value_str):
    if value_str:
        return value_str.lower() == 'yes'
    return False

def parse_float(value_str):
    try:
        return float(value_str)
    except (ValueError, TypeError):
        return 0.0

def parse_int(value_str):
    try:
        return int(value_str)
    except (ValueError, TypeError):
        return 0

def split_list_field(value_str, delimiter=','):
    if not value_str:
        return []
    return [item.strip() for item in value_str.split(delimiter)]

def split_space_separated_list(value_str):
    if not value_str:
        return []
    return value_str.split(' ')

def parse_products_csv(filepath):
    products = []
    current_product_object = None
    # These are the exact column names from the CSV
    PRODUCT_ID_COL = "Product ID [Non Editable]"
    VARIANT_ID_COL = "Variant ID [Non Editable]"
    PRODUCT_TYPE_COL = "Product Type [Non Editable]"
    PRODUCT_PAGE_COL = "Product Page"
    PRODUCT_URL_COL = "Product URL"
    TITLE_COL = "Title"
    DESCRIPTION_COL = "Description"
    SKU_COL = "SKU"
    PRICE_COL = "Price"
    SALE_PRICE_COL = "Sale Price"
    ON_SALE_COL = "On Sale"
    STOCK_COL = "Stock"
    CATEGORIES_COL = "Categories"
    TAGS_COL = "Tags"
    WEIGHT_COL = "Weight"
    LENGTH_COL = "Length"
    WIDTH_COL = "Width"
    HEIGHT_COL = "Height"
    VISIBLE_COL = "Visible"
    HOSTED_IMAGE_URLS_COL = "Hosted Image URLs"

    try:
        with open(filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product_id_val = row.get(PRODUCT_ID_COL)

                if product_id_val and product_id_val.strip(): # This row is a new product
                    if current_product_object:
                        products.append(current_product_object)

                    option_names_list = get_option_names(row)

                    current_product_object = Product(
                        product_id=product_id_val,
                        product_type=row.get(PRODUCT_TYPE_COL),
                        product_page=row.get(PRODUCT_PAGE_COL),
                        product_url=row.get(PRODUCT_URL_COL),
                        title=row.get(TITLE_COL),
                        description=row.get(DESCRIPTION_COL),
                        categories=split_list_field(row.get(CATEGORIES_COL)),
                        tags=split_list_field(row.get(TAGS_COL)),
                        visible=parse_bool(row.get(VISIBLE_COL)),
                        hosted_image_urls=split_space_separated_list(row.get(HOSTED_IMAGE_URLS_COL)),
                        option_names=option_names_list
                        # variants list is initialized empty in Product class
                    )

                if not current_product_object:
                    # Or log a warning: print(f"Skipping row, no current product: {row}")
                    continue

                # Every row (product or variant-only) defines a variant
                variant_option_values = get_option_values(row, len(current_product_object.option_names))

                variant_obj = Variant(
                    variant_id=row.get(VARIANT_ID_COL),
                    sku=row.get(SKU_COL),
                    option_values=variant_option_values,
                    price=parse_float(row.get(PRICE_COL)),
                    sale_price=parse_float(row.get(SALE_PRICE_COL)),
                    on_sale=parse_bool(row.get(ON_SALE_COL)),
                    stock=parse_int(row.get(STOCK_COL)),
                    weight=parse_float(row.get(WEIGHT_COL)),
                    length=parse_float(row.get(LENGTH_COL)),
                    width=parse_float(row.get(WIDTH_COL)),
                    height=parse_float(row.get(HEIGHT_COL)),
                    # Variant specific image URLs or product's if variant's is empty
                    hosted_image_urls=split_space_separated_list(row.get(HOSTED_IMAGE_URLS_COL)) if row.get(HOSTED_IMAGE_URLS_COL) and row.get(HOSTED_IMAGE_URLS_COL).strip() else current_product_object.hosted_image_urls
                )
                current_product_object.variants.append(variant_obj)

            if current_product_object: # Add the last product
                products.append(current_product_object)

    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    return products

if __name__ == "__main__":
    csv_file = "products_squarespace.csv"
    parsed_products = parse_products_csv(csv_file)

    if parsed_products:
        print(f"\nSuccessfully parsed {len(parsed_products)} product(s) from '{csv_file}':")
        for product in parsed_products:
            print("\n--- Product ---")
            print(f"Title: {product.title}")
            print(f"ID: {product.product_id}")
            print(f"Type: {product.product_type}")
            print(f"Page: {product.product_page}")
            print(f"URL: {product.product_url}")
            print(f"Description: {product.description[:100]}...") # Print first 100 chars of description
            print(f"Categories: {product.categories}")
            print(f"Tags: {product.tags}")
            print(f"Visible: {product.visible}")
            print(f"Option Names: {product.option_names}")
            print(f"Hosted Image URLs: {product.hosted_image_urls}")
            print(f"Number of Variants: {len(product.variants)}")

            if product.variants:
                print("  --- Variants ---")
                for variant in product.variants:
                    print(f"    Variant ID: {variant.variant_id}")
                    print(f"    SKU: {variant.sku}")
                    print(f"    Option Values: {variant.option_values}")
                    print(f"    Price: {variant.price}")
                    print(f"    Sale Price: {variant.sale_price}")
                    print(f"    On Sale: {variant.on_sale}")
                    print(f"    Stock: {variant.stock}")
                    print(f"    Weight: {variant.weight}")
                    print(f"    Length: {variant.length}")
                    print(f"    Width: {variant.width}")
                    print(f"    Height: {variant.height}")
                    print(f"    Hosted Image URLs: {variant.hosted_image_urls}")
                    print("    -----")
    else:
        print(f"No products parsed from '{csv_file}' or file not found.")

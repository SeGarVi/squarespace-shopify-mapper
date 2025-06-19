import csv
from product_classes import ShopifyProduct # Assuming ShopifyProduct is in product_classes.py

SHOPIFY_HEADERS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value",
    "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty",
    "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price",
    "Variant Compare At Price", "Variant Requires Shipping", "Variant Taxable", "Variant Barcode",
    "Image Src", "Image Position", "Image Alt Text", "Gift Card", "SEO Title", "SEO Description",
    "Google Shopping / Google Product Category", "Google Shopping / Gender",
    "Google Shopping / Age Group", "Google Shopping / MPN", "Google Shopping / Condition",
    "Google Shopping / Custom Product", "Google Shopping / Custom Label 0",
    "Google Shopping / Custom Label 1", "Google Shopping / Custom Label 2",
    "Google Shopping / Custom Label 3", "Google Shopping / Custom Label 4",
    "Variant Image", "Variant Weight Unit", "Variant Tax Code", "Cost per item", "Status"
    # Removed deprecated/example-specific metafields as they are not in ShopifyProduct class
    # "Option1 Linked To", "Option2 Linked To", "Option3 Linked To" - also seem specific/not general
]

# A more complete header list based on common Shopify CSVs if needed,
# but sticking to the provided one and what ShopifyProduct/Variant classes can populate.
# The provided list in the prompt is quite extensive.
# Let's ensure all keys from the prompt are in the `SHOPIFY_HEADERS` for DictWriter.
# I've adjusted the list above to match the prompt's original request closely.
# The prompt's list was missing a few from the example like "Option1 Linked To", but also included many Google Shopping fields.
# For this implementation, I will use the exact list from the prompt.

SHOPIFY_HEADERS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value", "Option1 Linked To", "Option2 Name", "Option2 Value", "Option2 Linked To",
    "Option3 Name", "Option3 Value", "Option3 Linked To", "Variant SKU", "Variant Grams",
    "Variant Inventory Tracker", "Variant Inventory Qty", "Variant Inventory Policy",
    "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price",
    "Variant Requires Shipping", "Variant Taxable", "Variant Barcode", "Image Src",
    "Image Position", "Image Alt Text", "Gift Card", "SEO Title", "SEO Description",
    "Google Shopping / Google Product Category", "Google Shopping / Gender",
    "Google Shopping / Age Group", "Google Shopping / MPN", "Google Shopping / Condition",
    "Google Shopping / Custom Product", "Google Shopping / Custom Label 0",
    "Google Shopping / Custom Label 1", "Google Shopping / Custom Label 2",
    "Google Shopping / Custom Label 3", "Google Shopping / Custom Label 4",
    "Color (product.metafields.shopify.color-pattern)", # Example Metafield
    "Grupo de edad del perro (product.metafields.shopify.dog-age-group)", # Example Metafield
    "Sabor de comida para mascotas (product.metafields.shopify.pet-food-flavor)", # Example Metafield
    "Forma de la comida para mascotas (product.metafields.shopify.pet-food-form)", # Example Metafield
    "Variant Image", "Variant Weight Unit", "Variant Tax Code", "Cost per item", "Status"
]


def write_shopify_csv(shopify_products: list[ShopifyProduct], csv_filepath: str):
    """
    Writes a list of ShopifyProduct objects to a CSV file in Shopify's format.

    Args:
        shopify_products (list[ShopifyProduct]): List of products to write.
        csv_filepath (str): Path to the output CSV file.
    """
    with open(csv_filepath, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=SHOPIFY_HEADERS)
        writer.writeheader()

        for product in shopify_products:
            image_position = 1

            for variant_index, variant in enumerate(product.variants):
                # Initialize row_data with all headers to ensure all columns are present
                row_data = {header: "" for header in SHOPIFY_HEADERS}

                row_data["Handle"] = product.handle

                # Fields for the first variant / main product line
                if variant_index == 0:
                    row_data["Title"] = product.title
                    row_data["Body (HTML)"] = product.body_html
                    row_data["Vendor"] = product.vendor
                    row_data["Product Category"] = product.product_category
                    row_data["Type"] = product.type
                    row_data["Tags"] = product.tags # Already a string
                    row_data["Published"] = str(product.published).lower() if isinstance(product.published, bool) else "true" # default to true

                    row_data["Image Src"] = product.image_src if product.image_src else ""
                    if product.image_src:
                        row_data["Image Position"] = image_position
                        image_position += 1

                    row_data["Image Alt Text"] = product.title # Default alt text
                    row_data["Status"] = "active" # Default status

                    # Option names from the product level (set by mapper)
                    row_data["Option1 Name"] = product.option1_name
                    row_data["Option2 Name"] = getattr(product, 'option2_name', None) or "" # Use getattr for safety
                    row_data["Option3 Name"] = getattr(product, 'option3_name', None) or "" # Use getattr for safety

                # Common variant fields (apply to all variant rows including the first)
                row_data["Option1 Value"] = variant.option1_value
                if hasattr(variant, 'option2_value') and variant.option2_value is not None : # Check if product has option2_name
                    row_data["Option2 Value"] = variant.option2_value
                if hasattr(variant, 'option3_value') and variant.option3_value is not None: # Check if product has option3_name
                    row_data["Option3 Value"] = variant.option3_value

                row_data["Variant SKU"] = variant.sku
                row_data["Variant Grams"] = str(variant.grams) if variant.grams is not None else ""
                row_data["Variant Inventory Tracker"] = variant.inventory_tracker
                row_data["Variant Inventory Qty"] = str(variant.inventory_qty) if variant.inventory_qty is not None else ""
                row_data["Variant Inventory Policy"] = variant.inventory_policy
                row_data["Variant Fulfillment Service"] = variant.fulfillment_service
                row_data["Variant Price"] = str(variant.price) if variant.price is not None else ""
                row_data["Variant Compare At Price"] = str(variant.compare_at_price) if variant.compare_at_price is not None else ""

                row_data["Variant Requires Shipping"] = str(variant.requires_shipping).lower() if isinstance(variant.requires_shipping, bool) else "true"
                row_data["Variant Taxable"] = str(variant.taxable).lower() if isinstance(variant.taxable, bool) else "true"
                row_data["Variant Barcode"] = variant.barcode if variant.barcode else ""

                row_data["Variant Image"] = variant.image_src if variant.image_src else ""
                row_data["Variant Weight Unit"] = "kg" # As per example, or make dynamic if needed

                # Gift Card is usually False for non-gift card products
                row_data["Gift Card"] = "false"

                # Default SEO fields if not specifically mapped
                if variant_index == 0: # SEO Title/Desc usually for main product
                    row_data["SEO Title"] = product.title
                    row_data["SEO Description"] = product.body_html[:320] if product.body_html else "" # Shopify limit

                writer.writerow(row_data)

            # Additional Image Rows
            for additional_image_url in product.additional_images:
                image_row_data = {header: "" for header in SHOPIFY_HEADERS}
                image_row_data["Handle"] = product.handle
                image_row_data["Image Src"] = additional_image_url
                image_row_data["Image Position"] = image_position
                image_row_data["Image Alt Text"] = product.title # Default alt text
                # Only write if there's an image_src to prevent blank image rows if logic error somewhere
                if additional_image_url:
                    writer.writerow(image_row_data)
                    image_position += 1

if __name__ == '__main__':
    from product_classes import ShopifyVariant # For local testing

    # Create dummy ShopifyProduct instances for testing
    # Product 1: With variants
    sp1_v1 = ShopifyVariant(title='Red', sku='TSHIRT-RED', option1_name='Color', option1_value='Red', price=25.0, inventory_qty=10, grams=150, requires_shipping=True, taxable=True)
    sp1_v2 = ShopifyVariant(title='Blue', sku='TSHIRT-BLUE', option1_name='Color', option1_value='Blue', price=25.0, inventory_qty=5, grams=150, compare_at_price=30.0, requires_shipping=True, taxable=True)

    sp1 = ShopifyProduct(
        handle='awesome-t-shirt', title='Awesome T-Shirt', body_html='A really cool t-shirt.', vendor='Mi tienda',
        product_category='Apparel', type='Shirts', tags='Clothing, Fashion', published=True,
        image_src='http://example.com/tshirt-main.jpg',
        option1_name='Color' # Set by mapper
    )
    sp1.variants.extend([sp1_v1, sp1_v2])
    sp1.additional_images = ['http://example.com/tshirt-angle2.jpg', 'http://example.com/tshirt-angle3.jpg']
    # Manually set variant fields on product for testing (mapper would do this)
    sp1.variant_sku = sp1_v1.sku
    sp1.variant_price = sp1_v1.price
    sp1.variant_inventory_qty = sp1_v1.inventory_qty
    sp1.option1_value = sp1_v1.option1_value


    # Product 2: Simple product (one default variant)
    sp2_v_default = ShopifyVariant(
        title='Default Title', sku='MUG-COOL', option1_name='Title', option1_value='Default Title',
        price=15.0, inventory_qty=50, grams=300, requires_shipping=True, taxable=True
    )
    sp2 = ShopifyProduct(
        handle='cool-mug', title='Cool Mug', body_html='A very cool mug.', vendor='Mi tienda',
        product_category='Home Goods', type='Mugs', tags='Kitchen, Drinkware', published=True,
        image_src='http://example.com/mug.jpg',
        option1_name='Title' # Set by mapper
    )
    sp2.variants.append(sp2_v_default)
    # Manually set variant fields on product for testing
    sp2.variant_sku = sp2_v_default.sku
    sp2.variant_price = sp2_v_default.price
    sp2.variant_inventory_qty = sp2_v_default.inventory_qty
    sp2.option1_value = sp2_v_default.option1_value


    test_products = [sp1, sp2]
    output_csv_file = 'test_shopify_output.csv'

    print(f"Writing Shopify products to '{output_csv_file}'...")
    write_shopify_csv(test_products, output_csv_file)
    print(f"Successfully wrote to '{output_csv_file}'.")

    # You can open 'test_shopify_output.csv' to verify its structure.
    # Example: print content to console
    # with open(output_csv_file, 'r', encoding='utf-8') as f:
    #     print("\n--- CSV Content ---")
    #     print(f.read())
    #     print("--- End of CSV Content ---")

    # Clean up dummy file
    import os
    # os.remove(output_csv_file) # Comment out if you want to inspect the file
    # print(f"Cleaned up '{output_csv_file}'.")

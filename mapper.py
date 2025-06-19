import re
from urllib.parse import urlparse
from product_classes import ShopifyProduct, ShopifyVariant, SquarespaceProduct, SquarespaceVariant

def _generate_handle(product_url: str, title: str) -> str:
    """
    Generates a Shopify handle from a product URL or title.
    """
    handle = ""
    if product_url:
        try:
            path = urlparse(product_url).path
            # Extract the last part of the path, ignore if it's a common suffix like .html
            if path:
                name = path.strip('/').split('/')[-1]
                if '.' in name: # Avoid using file extensions as handles
                    name_part = name.rsplit('.', 1)[0]
                    if name_part: # Ensure it's not just ".html"
                        handle = name_part
                else:
                    handle = name
        except Exception:
            pass # Fallback to title if URL parsing fails

    if not handle and title:
        handle = title.lower()
        handle = re.sub(r'\s+', '-', handle)  # Replace spaces with hyphens
        handle = re.sub(r'[^\w\-]+', '', handle)  # Remove non-alphanumeric except hyphens
        handle = re.sub(r'--+', '-', handle)  # Replace multiple hyphens with single
        handle = handle.strip('-')

    return handle if handle else "default-product-handle"


def map_squarespace_to_shopify(squarespace_products: list[SquarespaceProduct]) -> list[ShopifyProduct]:
    """
    Maps a list of SquarespaceProduct objects to a list of ShopifyProduct objects.
    """
    shopify_products = []

    for sq_product in squarespace_products:
        handle = _generate_handle(sq_product.product_url, sq_product.title)

        main_image_src = sq_product.hosted_image_urls[0] if sq_product.hosted_image_urls else None
        additional_images_src = sq_product.hosted_image_urls[1:] if len(sq_product.hosted_image_urls) > 1 else []

        # Determine Product Category
        product_category = "Uncategorized"
        if sq_product.categories:
            product_category = sq_product.categories[0]

        # Determine Type
        product_type = sq_product.product_type
        if not product_type and sq_product.categories:
            product_type = sq_product.categories[0] # Fallback to first category for type

        shopify_product = ShopifyProduct(
            handle=handle,
            title=sq_product.title,
            body_html=sq_product.description,
            vendor="Mi tienda", # Default vendor
            product_category=product_category,
            type=product_type,
            tags=", ".join(sq_product.tags) if sq_product.tags else "",
            published=True, # Default to published
            image_src=main_image_src
        )
        shopify_product.additional_images = additional_images_src

        if sq_product.variants:
            # Set Shopify product option names from the first Squarespace variant
            # Assumes all variants of a product share the same option name structure
            first_sq_variant = sq_product.variants[0]
            if first_sq_variant.option_name_1:
                shopify_product.option1_name = first_sq_variant.option_name_1
            if first_sq_variant.option_name_2:
                shopify_product.option2_name = first_sq_variant.option_name_2 # Will be set if exists
            if first_sq_variant.option_name_3:
                shopify_product.option3_name = first_sq_variant.option_name_3 # Will be set if exists

            for sq_variant in sq_product.variants:
                # Construct variant title for Shopify (e.g., "Value1 / Value2")
                variant_title_parts = []
                if sq_variant.option_value_1:
                    variant_title_parts.append(sq_variant.option_value_1)
                if sq_variant.option_value_2:
                    variant_title_parts.append(sq_variant.option_value_2)
                if sq_variant.option_value_3:
                    variant_title_parts.append(sq_variant.option_value_3)

                shopify_variant_title = " / ".join(variant_title_parts) if variant_title_parts else sq_product.title # Fallback for safety

                shopify_variant = ShopifyVariant(
                    title=shopify_variant_title,
                    sku=sq_variant.sku,
                    grams=sq_variant.weight, # Assuming weight is in grams or needs conversion later
                    inventory_tracker="shopify",
                    inventory_qty=sq_variant.stock,
                    inventory_policy="deny",
                    fulfillment_service="manual",
                    price=sq_variant.price,
                    compare_at_price=sq_variant.sale_price if sq_variant.on_sale else None,
                    requires_shipping=True, # Assuming physical products
                    taxable=True, # Default
                    barcode=None, # No barcode info from Squarespace structure
                    image_src=None, # No direct variant image mapping from Squarespace structure
                    option1_name=sq_variant.option_name_1,
                    option1_value=sq_variant.option_value_1,
                    option2_name=sq_variant.option_name_2,
                    option2_value=sq_variant.option_value_2,
                    option3_name=sq_variant.option_name_3,
                    option_value_3=sq_variant.option_value_3 # Corrected attribute name
                )
                shopify_product.variants.append(shopify_variant)
        else:
            # No Squarespace variants, create a default Shopify variant
            shopify_product.option1_name = "Title"
            # shopify_product.option1_value = "Default Title" # This will be set later from the variant itself

            default_variant = ShopifyVariant(
                title="Default Title",
                sku=sq_product.sku, # SKU from main product
                grams=sq_product.weight, # Weight from main product
                inventory_tracker="shopify",
                inventory_qty=sq_product.stock, # Stock from main product
                inventory_policy="deny",
                fulfillment_service="manual",
                price=sq_product.price, # Price from main product
                compare_at_price=sq_product.sale_price if sq_product.on_sale else None,
                requires_shipping=True,
                taxable=True,
                option1_name="Title",
                option1_value="Default Title"
            )
            shopify_product.variants.append(default_variant)

        # Populate ShopifyProduct's main variant fields from the first variant in the list
        if shopify_product.variants:
            first_shopify_variant = shopify_product.variants[0]
            shopify_product.variant_sku = first_shopify_variant.sku
            shopify_product.variant_price = first_shopify_variant.price
            shopify_product.variant_inventory_qty = first_shopify_variant.inventory_qty

            # Set main product's option values from the first variant
            # Option names were already set (either from sq_variant or "Title")
            if shopify_product.option1_name: # Check if option1_name is set
                 shopify_product.option1_value = first_shopify_variant.option1_value
            if hasattr(shopify_product, 'option2_name') and shopify_product.option2_name: # Check if option2_name is set
                 shopify_product.option2_value = first_shopify_variant.option2_value
            if hasattr(shopify_product, 'option3_name') and shopify_product.option3_name: # Check if option3_name is set
                 shopify_product.option3_value = first_shopify_variant.option3_value


        shopify_products.append(shopify_product)

    return shopify_products

if __name__ == '__main__':
    # Create dummy SquarespaceProduct instances for testing
    # Product 1: With variants
    sq_p1_v1 = SquarespaceVariant(variant_id='v1', sku='SKU1-RED', option_name_1='Color', option_value_1='Red', price=50.0, stock=10, weight=100)
    sq_p1_v2 = SquarespaceVariant(variant_id='v2', sku='SKU1-BLUE', option_name_1='Color', option_value_1='Blue', price=52.0, stock=5, weight=100)
    sq_product1 = SquarespaceProduct(
        product_id='p1', title='Awesome T-Shirt', description='A really cool t-shirt', product_url='/shop/awesome-t-shirt',
        tags=['Clothing', 'Fashion'], categories=['Apparel'], product_type='PHYSICAL',
        hosted_image_urls=['http://example.com/img1.jpg', 'http://example.com/img2.jpg']
    )
    sq_product1.variants.extend([sq_p1_v1, sq_p1_v2])

    # Product 2: No variants (uses main product fields for default variant)
    sq_product2 = SquarespaceProduct(
        product_id='p2', title='Cool Mug', description='A very cool mug', product_url='/shop/cool-mug',
        sku='SKU-MUG', price=15.0, stock=20, weight=300,
        tags=['Home', 'Kitchen'], categories=['Homewares'], product_type='PHYSICAL',
        hosted_image_urls=['http://example.com/mug.jpg']
    )

    # Product 3: Minimal data, no URL
    sq_product3 = SquarespaceProduct(
        product_id='p3', title='Sticker Pack', description='Fun stickers', product_url=None,
        sku='SKU-STICKER', price=5.0, stock=100, weight=10
    )


    squarespace_items = [sq_product1, sq_product2, sq_product3]

    print("Mapping Squarespace products to Shopify products...")
    shopify_items = map_squarespace_to_shopify(squarespace_items)

    for sp in shopify_items:
        print(f"\nShopify Product: {sp.title} (Handle: {sp.handle})")
        print(f"  Body HTML: {sp.body_html}")
        print(f"  Vendor: {sp.vendor}, Category: {sp.product_category}, Type: {sp.type}")
        print(f"  Tags: {sp.tags}, Published: {sp.published}")
        print(f"  Image Src: {sp.image_src}")
        print(f"  Additional Images: {sp.additional_images}")
        print(f"  Option1 Name: {sp.option1_name}, Value: {sp.option1_value}")
        if hasattr(sp, 'option2_name') and sp.option2_name:
            print(f"  Option2 Name: {sp.option2_name}, Value: {sp.option2_value}")
        print(f"  Variant SKU (main): {sp.variant_sku}, Price: {sp.variant_price}, Qty: {sp.variant_inventory_qty}")

        print("  Variants:")
        for i, v in enumerate(sp.variants):
            print(f"    Variant {i+1}:")
            print(f"      Title: {v.title}")
            print(f"      SKU: {v.sku}, Price: {v.price}, Qty: {v.inventory_qty}, Grams: {v.grams}")
            print(f"      Option1: {v.option1_name} = {v.option1_value}")
            if v.option2_name:
                 print(f"      Option2: {v.option2_name} = {v.option2_value}")
            if v.option3_name:
                 print(f"      Option3: {v.option3_name} = {v.option3_value}") # Corrected attribute name
            print(f"      Compare@Price: {v.compare_at_price}")

    print("\nMapping complete.")

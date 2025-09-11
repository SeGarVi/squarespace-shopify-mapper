import string_utils
import re
from shopify_product import ShopifyProductBuilder

#TODO fill columns status (column BB)
#     fill columns Fulfillment service (column W, justo antes de variant price) 
#     fill columns Inventory policy (column V, justo antes de Fulfillment service)

class SquarespaceToShopifyProductMapper:
    def __init__(self, squarespace_product):
        self.squarespace_product = squarespace_product

    def map(self):
        if not self.squarespace_product.variants:
            if len(self.squarespace_product.hosted_image_urls) > 1:
                return self.map_with_many_images()
            else:
                return self.map_without_variants()
        else:
            if len(self.squarespace_product.variants) >= len(self.squarespace_product.hosted_image_urls):
                # If there are more variants than images, we can't map images to variants properly
                return self.map_with_more_variants_than_images()
            else:
                # If there are more images than variants, we can map images to variants properly
                return self.map_with_more_images_than_variants()

    def map_without_variants(self):
        shopify_products = []
        shopify_product_type = self.map_type()
        shopify_product = ShopifyProductBuilder() \
            .with_handle(self.map_handle()) \
            .with_title(self.map_title()) \
            .with_body(self.map_body()) \
            .with_type(shopify_product_type) \
            .with_tags(shopify_product_type) \
            .with_published(self.map_published()) \
            .with_option_1_name(self.map_option_name_1()) \
            .with_option_1_value(self.map_option_value_1()) \
            .with_option_1_value(self.map_option_value_1()) \
            .with_variant_grams(self.map_variant_grams()) \
            .with_variant_inventory_tracker("shopify") \
            .with_variant_inventory_qty(self.map_variant_inventory_qty()) \
            .with_variant_inventory_policy("deny") \
            .with_variant_fulfillment_service("manual") \
            .with_variant_price(self.map_variant_price()) \
            .with_image_src(self.squarespace_product.hosted_image_urls[0]) \
            .with_image_position(1) \
            .with_product_category(self.calculate_category(shopify_product_type)) \
            .with_status("active") \
            .build()

        shopify_products.append(shopify_product)
        return shopify_products
    
    def map_with_many_images(self):
        shopify_products = []
        shopify_products.append(self.map_first_image())
        position = 2
        for image_url in self.squarespace_product.hosted_image_urls[1:]:
            shopify_product = self.map_additional_image(position)
            shopify_products.append(shopify_product)
            position += 1
        return shopify_products

    def map_first_image(self):
        shopify_product_type = self.map_type()
        shopify_product = ShopifyProductBuilder() \
            .with_handle(self.map_handle()) \
            .with_title(self.map_title()) \
            .with_body(self.map_body()) \
            .with_type(shopify_product_type) \
            .with_tags(shopify_product_type) \
            .with_published(self.map_published()) \
            .with_option_1_name(self.map_option_name_1()) \
            .with_option_1_value(self.map_option_value_1()) \
            .with_variant_grams(self.map_variant_grams()) \
            .with_variant_inventory_tracker("shopify") \
            .with_variant_inventory_qty(self.map_variant_inventory_qty()) \
            .with_variant_inventory_policy("deny") \
            .with_variant_fulfillment_service("manual") \
            .with_variant_price(self.map_variant_price()) \
            .with_image_src(self.squarespace_product.hosted_image_urls[0]) \
            .with_image_position(1) \
            .with_product_category(self.calculate_category(shopify_product_type)) \
            .with_status("active") \
            .build()
        return shopify_product

    def map_additional_image(self, position):
        shopify_product = ShopifyProductBuilder() \
            .with_handle(self.map_handle()) \
            .with_image_src(self.squarespace_product.hosted_image_urls[position-1]) \
            .with_image_position(position) \
            .build()
        return shopify_product

    def map_with_more_variants_than_images(self):
        shopify_products = []
        shopify_products.append(self.map_first_variant())
        position = 2
        for variant in self.squarespace_product.variants[1:]:
            shopify_product = self.map_variant(variant, position)
            shopify_products.append(shopify_product)
            position += 1
        return shopify_products

    def map_with_more_images_than_variants(self):
        shopify_products = []
        shopify_products.append(self.map_first_variant())
        for position in range(1, len(self.squarespace_product.hosted_image_urls)):
            if position < len(self.squarespace_product.variants):
                shopify_product = self.map_variant(self.squarespace_product.variants[position], position+1)
            else:
                shopify_product = self.map_just_image(position+1)
            shopify_products.append(shopify_product)
        return shopify_products

    def map_first_variant(self):
        shopify_product_type = self.map_type()
        shopify_product = ShopifyProductBuilder() \
            .with_handle(self.map_handle()) \
            .with_title(self.map_title()) \
            .with_body(self.map_body()) \
            .with_type(shopify_product_type) \
            .with_tags(shopify_product_type) \
            .with_published(self.map_published()) \
            .with_option_1_name(self.map_option_name_1(self.squarespace_product.variants[0])) \
            .with_option_1_value(self.map_option_value_1(self.squarespace_product.variants[0])) \
            .with_variant_grams(self.map_variant_grams(self.squarespace_product.variants[0])) \
            .with_variant_inventory_tracker("shopify") \
            .with_variant_inventory_qty(self.map_variant_inventory_qty(self.squarespace_product.variants[0])) \
            .with_variant_inventory_policy("deny") \
            .with_variant_fulfillment_service("manual") \
            .with_variant_price(self.map_variant_price(self.squarespace_product.variants[0])) \
            .with_image_src(self.squarespace_product.hosted_image_urls[0]) \
            .with_image_position(1) \
            .with_product_category(self.calculate_category(shopify_product_type)) \
            .with_status("active") \
            .build()
        return shopify_product

    def map_variant(self, variant, position):
        shopify_product = ShopifyProductBuilder() \
            .with_handle(self.map_handle()) \
            .with_option_1_value(self.map_option_value_1(variant)) \
            .with_variant_grams(self.map_variant_grams(variant)) \
            .with_variant_inventory_tracker("shopify") \
            .with_variant_inventory_qty(self.map_variant_inventory_qty(variant)) \
            .with_variant_inventory_policy("deny") \
            .with_variant_fulfillment_service("manual") \
            .with_variant_price(self.map_variant_price(variant)) \
            .with_image_src(self.squarespace_product.hosted_image_urls[position-1] if position-1 < len(self.squarespace_product.hosted_image_urls) else None) \
            .with_image_position(position) \
            .build()
        return shopify_product
    
    def map_just_image(self, position):
        shopify_product = ShopifyProductBuilder() \
            .with_handle(self.map_handle()) \
            .with_image_src(self.squarespace_product.hosted_image_urls[position-1] if position-1 < len(self.squarespace_product.hosted_image_urls) else None) \
            .with_image_position(position) \
            .build()
        return shopify_product

    def map_variant_grams(self, variant=None):
        return re.match(r"^(\d+)\s*(g|gr|gr\.)$", str(self.map_option_value_1(variant)).strip(), re.IGNORECASE).group(1) + ".0" \
            if re.match(r"^(\d+)\s*(g|gr|gr\.)$", str(self.map_option_value_1(variant)).strip(), re.IGNORECASE) \
            else ""

    def map_variant_price(self, variant=None):
        if variant:
            return variant.price
        return self.squarespace_product.price

    def map_variant_inventory_qty(self, variant=None):
        if variant:
            return variant.stock
        else:
            return self.squarespace_product.stock

    def map_option_value_1(self, variant=None):
        if variant:
            return variant.option_value_1
        return "Default Title"

    def map_option_name_1(self, variant=None):
        if variant:
            return variant.option_name_1
        return "Title"

    def map_published(self):
        is_visible = self.squarespace_product.visible
        return "true" if is_visible == "Yes" else "false" if is_visible == "No" else ""

    def map_handle(self):
        return string_utils.remove_accents(self.squarespace_product.title).replace(" ", "-").lower()

    def map_title(self):
        return self.squarespace_product.title

    def map_body(self):
        return self.squarespace_product.description

    def calculate_category(self, tags):
        tags = tags or ""
        tags_lower = tags.lower()

        def contains(*words):
            return all(word.lower() in tags_lower for word in words)

        if contains("Hmeda", "Perro") or contains("Comida-Deshidratada", "Perro"):
            return "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Food > Non-Prescription Dog Food"
        if contains("Collar", "Desparasitante"):
            return "Animals & Pet Supplies > Pet Supplies > Pet Collars & Harnesses > Flea Collars"
        if contains("Masticacin", "Perro"):
            return "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Treats"
        if contains("Premio-Rpido", "Perro"):
            return "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Treats"
        if contains("Juego", "Perro"):
            return "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Toys"
        if contains("Cama", "Perro", "Refrescante"):
            return "Animals & Pet Supplies > Pet Supplies > Pet Beds > Cooling Beds"
        if contains("Cama", "Perro"):
            return "Animals & Pet Supplies > Pet Supplies > Pet Beds > Bolster Beds"
        if contains("Bebedero", "Plegable"):
            return "Animals & Pet Supplies > Pet Supplies > Pet Bowls, Feeders & Waterers > Travel Bowls"
        if contains("Bolsita", "Snacks"):
            return "Animals & Pet Supplies > Pet Supplies > Pet Waste Bag Dispensers & Holders > Standard Dispensers & Holders"
        if "champú".lower() in tags_lower:
            return "Animals & Pet Supplies > Pet Supplies > Pet Grooming Supplies > Pet Shampoo & Conditioner > Shampoos"
        if "correa".lower() in tags_lower:
            return "Animals & Pet Supplies > Pet Supplies > Pet Leashes > Standard Leashes"
        if "collar".lower() in tags_lower:
            return "Animals & Pet Supplies > Pet Supplies > Pet Collars & Harnesses > Standard Collars"
        if "toalla".lower() in tags_lower:
            return "Animals & Pet Supplies > Pet Supplies > Pet Grooming Supplies"
        if "bandana".lower() in tags_lower:
            return "Animals & Pet Supplies > Pet Supplies > Pet Apparel > Pet Bandanas"
        if "toallita".lower() in tags_lower:
            return "Animals & Pet Supplies > Pet Supplies > Pet Grooming Supplies > Pet Wipes > Grooming Wipes"
        if "suplemento".lower() in tags_lower:
            return "Animals & Pet Supplies > Pet Supplies > Pet Vitamins & Supplements"
        if contains("Limpiador", "Ojos"):
            return "Animals & Pet Supplies > Pet Supplies > Pet Eye Drops & Lubricants > Eye Cleaners"
        if contains("Hmeda", "Gato"):
            return "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Food > Non-Prescription Cat Food"
        if contains("Snacks-Gato", "Gato"):
            return "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Treats"
        if contains("Juego", "Gato"):
            return "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Toys"
        return ""

    def map_type(self):
        categories = self.squarespace_product.categories
        tags = self.squarespace_product.tags

        # Remove accents
        categories_clean = string_utils.remove_accents(categories)
        tags_clean = string_utils.remove_accents(tags)

        # Replace " /" or "/ " with ""
        categories_clean = categories_clean.replace('/', ', ')

        categories_proper = string_utils.proper_case(categories_clean)
        tags_proper = string_utils.proper_case(tags_clean)

        # Concatenate and split by comma
        combined = categories_proper + ',' + tags_proper
        items = [item.strip() for item in combined.split(',') if item.strip()]

        # Unique and sorted
        unique_sorted = sorted(set(items))

        # Join with ", "
        return ', '.join(unique_sorted)

    def map_variants(self):
        variants = []
        for variant in self.squarespace_product.variants:
            mapped_variant = {
                "option1": variant.name,
                "price": variant.price,
                "sku": variant.sku,
                "inventory_quantity": variant.inventory_quantity
            }
            variants.append(mapped_variant)
        return variants

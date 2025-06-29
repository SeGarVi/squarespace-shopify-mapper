import csv
from squarespace_product import SquarespaceProductBuilder
from squarespace_product import SquarespaceVariantBuilder

class SquarespaceParser:
    def __init__(self, path):
        self.path = path
        self.products = []
        self.image_urls = []

    def create_product(self, row, image_urls=None):
        squarespace_product_builder = SquarespaceProductBuilder() \
                        .with_title(row['Title']) \
                        .with_description(row['Description']) \
                        .with_price(row['Price']) \
                        .with_stock(row['Stock']) \
                        .with_tags(row['Tags']) \
                        .with_visible(row['Visible'])
        return squarespace_product_builder.build()

    def parse(self):
        with open(self.path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            last_product = None
            last_product_image_urls = None
            for row in reader:
                if self.is_product(row):
                    self.set_product_image_urls(last_product_image_urls)
                    if self.is_variant(row):
                        # If the row has options, we create a product with variants
                        last_product = self.create_product_with_variant(row)
                    else:
                        last_product = self.create_product(row)
                    last_product_image_urls = row['Hosted Image URLs'].split()
                    self.products.append(last_product)
                
                if row['Option Name 1'] and row['Option Value 1']:
                    if last_product:
                        last_product.add_variant(self.create_variant(row))
            self.set_product_image_urls(last_product_image_urls)
            return self.products
    
    def set_product_image_urls(self, image_urls):
        product = self.products[-1] if self.products else None
        if product:
            number_of_images = len(image_urls)
            number_of_variants = len(product.variants) if product.variants else 0
            if number_of_images > 0:
                if number_of_variants == 0 or number_of_images < number_of_variants:
                    product.hosted_image_urls = image_urls
                elif number_of_images == number_of_variants + 1:
                    product.hosted_image_urls.append(image_urls[0])
                    for i, variant in enumerate(product.variants):
                        variant.hosted_image_urls.append(image_urls[i + 1])
                elif number_of_images == number_of_variants:
                    for i, variant in enumerate(product.variants):
                        variant.hosted_image_urls.append(image_urls[i])
                elif number_of_images > number_of_variants + 1:
                    variant_image_start_index = number_of_images - number_of_variants - 1
                    if variant_image_start_index > 1:
                        product.hosted_image_urls = image_urls[:variant_image_start_index]
                    else:
                        product.hosted_image_urls.append(image_urls[0])
                    for i, variant in enumerate(product.variants):
                        variant.hosted_image_urls.append(image_urls[variant_image_start_index + i])

    def create_product_with_variant(self, row):
        squarespace_product_builder = SquarespaceProductBuilder() \
                        .with_title(row['Title']) \
                        .with_description(row['Description']) \
                        .with_tags(row['Tags']) \
                        .with_visible(row['Visible'])
        return squarespace_product_builder.build()

    def create_variant(self, row):
        squarspace_varant_builder = SquarespaceVariantBuilder() \
                        .with_option_name_1(row['Option Name 1']) \
                        .with_option_value_1(row['Option Value 1']) \
                        .with_price(row['Price']) \
                        .with_stock(row['Stock'])
        return squarspace_varant_builder.build()

    def is_variant(self, row):
        return row['Option Name 1'] and row['Option Value 1']

    def is_product(self, row):
        return row['Product ID [Non Editable]']

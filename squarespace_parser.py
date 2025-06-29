import csv
from squarespace_product import SquarespaceProductBuilder
from squarespace_product import SquarespaceVariantBuilder

class SquarespaceParser:
    def __init__(self, path):
        self.path = path
        self.products = []

    def create_product(self, row):
        squarespace_product_builder = SquarespaceProductBuilder() \
                        .with_title(row['Title']) \
                        .with_description(row['Description']) \
                        .with_price(row['Price']) \
                        .with_stock(row['Stock']) \
                        .with_tags(row['Tags']) \
                        .with_visible(row['Visible']) \
                        .with_hosted_image_urls(row['Hosted Image URLs'])
        return squarespace_product_builder.build()

    def parse(self):
        with open(self.path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            last_product = None
            for row in reader:
                if self.is_product(row):
                    if self.is_variant(row):
                        # If the row has options, we create a product with variants
                        last_product = self.create_product_with_variant(row)
                    else:
                        last_product = self.create_product(row)
                    self.products.append(last_product)
                
                if row['Option Name 1'] and row['Option Value 1']:
                    if last_product:
                        last_product.add_variant(self.create_variant(row))
            return self.products
        
    def create_product_with_variant(self, row):
        squarespace_product_builder = SquarespaceProductBuilder() \
                        .with_title(row['Title']) \
                        .with_description(row['Description']) \
                        .with_tags(row['Tags']) \
                        .with_visible(row['Visible']) \
                        .with_hosted_image_urls(row['Hosted Image URLs'])
        return squarespace_product_builder.build()

    def create_variant(self, row):
        squarspace_varant_builder = SquarespaceVariantBuilder() \
                        .with_option_name_1(row['Option Name 1']) \
                        .with_option_value_1(row['Option Value 1']) \
                        .with_price(row['Price']) \
                        .with_stock(row['Stock']) \
                        .with_hosted_image_urls(row['Hosted Image URLs'])
        return squarspace_varant_builder.build()

    def is_variant(self, row):
        return row['Option Name 1'] and row['Option Value 1']

    def is_product(self, row):
        return row['Product ID [Non Editable]']

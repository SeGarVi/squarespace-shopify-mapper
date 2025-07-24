import argparse
from squarespace_parser import SquarespaceParser
from squarespace_to_shopify_product_mapper import SquarespaceToShopifyProductMapper
from shopify_product_writer import ShopifyProductListWriter

def main():
    print("test")
    parser = argparse.ArgumentParser(description="Convert Squarespace site to Shopify.")
    parser.add_argument("squarespace_products_file_path", help="Path to the Squarespace products CSV file")
    parser.add_argument("output_file", help="URL of the Shopify store to import into")

    args = parser.parse_args()
    squarespace_parser = SquarespaceParser(args.squarespace_products_file_path)
    products = squarespace_parser.parse()
    shopify_products = []
    for product in products:
        shopify_product_mapper = SquarespaceToShopifyProductMapper(product)
        shopify_products.extend(shopify_product_mapper.map())
    
    writer = ShopifyProductListWriter(shopify_products, args.output_file)
    writer.write()

if __name__ == "__main__":
    main()
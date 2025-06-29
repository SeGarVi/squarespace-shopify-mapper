import argparse
from squarespace_parser import SquarespaceParser

def main():
    print("test")
    parser = argparse.ArgumentParser(description="Convert Squarespace site to Shopify.")
    parser.add_argument("squarespace_products_file_path", help="Path to the Squarespace products CSV file")
    parser.add_argument("output_file", help="URL of the Shopify store to import into")

    args = parser.parse_args()
    squarespace_parser = SquarespaceParser(args.squarespace_products_file_path)
    products = squarespace_parser.parse()
    print(str(products))

if __name__ == "__main__":
    main()
import unittest
import os
import csv
import filecmp # Kept for potential alternative, but primary is dict comparison

from squarespace_parser import parse_squarespace_csv
from mapper import map_squarespace_to_shopify
from shopify_writer import write_shopify_csv, SHOPIFY_HEADERS # Import headers for consistency if needed

class TestProductMigration(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        self.squarespace_input_csv = "products_squarespace.csv"
        self.expected_shopify_output_csv = "products_shopify.csv" # Ground truth
        self.generated_shopify_output_csv = "test_generated_shopify_output.csv"

        # Ensure dummy input files exist for the test to run.
        # If these are not provided with the problem, the test will naturally fail,
        # which is fine. For a self-contained test, we might create them here.
        # For this exercise, we assume they are provided externally.
        if not os.path.exists(self.squarespace_input_csv):
            print(f"Warning: Input file {self.squarespace_input_csv} not found. Test may fail.")
            # Create a minimal dummy Squarespace CSV if it doesn't exist, so parser can run
            with open(self.squarespace_input_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Product ID [Non Editable]', 'Title', 'Hosted Image URLs', 'Tags', 'Categories', 'Product Type', 'SKU', 'Price', 'Stock'])
                writer.writerow(['p1', 'Test Product 1', 'img1.jpg img2.jpg', 'TagA,TagB', 'CatX', 'PHYSICAL', 'SKU1', '10.99', '5'])
            print(f"Created dummy {self.squarespace_input_csv} for test run.")

        if not os.path.exists(self.expected_shopify_output_csv):
            print(f"Warning: Expected output file {self.expected_shopify_output_csv} not found. Test may fail comparison.")
            # Create a minimal dummy Shopify CSV if it doesn't exist.
            # This would ideally be the true expected output.
            with open(self.expected_shopify_output_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=SHOPIFY_HEADERS)
                writer.writeheader()
                # Add a row corresponding to the dummy Squarespace input
                row = {h: "" for h in SHOPIFY_HEADERS}
                row.update({
                    "Handle": "test-product-1", "Title": "Test Product 1", "Vendor": "Mi tienda",
                    "Product Category": "CatX", "Type": "CatX", "Tags": "TagA, TagB", "Published": "true",
                    "Option1 Name": "Title", "Option1 Value": "Default Title",
                    "Variant SKU": "SKU1", "Variant Price": "10.99", "Variant Inventory Qty": "5",
                    "Variant Grams": "", "Variant Inventory Tracker": "shopify", "Variant Inventory Policy": "deny",
                    "Variant Fulfillment Service": "manual", "Variant Requires Shipping": "true", "Variant Taxable": "true",
                    "Image Src": "img1.jpg", "Image Position": "1", "Image Alt Text": "Test Product 1",
                    "Gift Card": "false", "Status": "active", "SEO Title": "Test Product 1", "SEO Description": "",
                    "Variant Weight Unit": "kg"
                })
                writer.writerow(row)
                row2 = {h: "" for h in SHOPIFY_HEADERS}
                row2.update({
                    "Handle": "test-product-1",
                    "Image Src": "img2.jpg", "Image Position": "2", "Image Alt Text": "Test Product 1"
                })
                writer.writerow(row2)

            print(f"Created dummy {self.expected_shopify_output_csv} for test run.")


    def tearDown(self):
        """Tear down test fixtures, if any."""
        if os.path.exists(self.generated_shopify_output_csv):
            os.remove(self.generated_shopify_output_csv)

    def _read_csv_to_list_of_dicts(self, filepath):
        """Helper function to read a CSV file into a list of dictionaries."""
        if not os.path.exists(filepath):
            self.fail(f"CSV file not found: {filepath}")
        with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Filter out rows that are completely empty (all values are empty strings)
            # This can happen if there are blank lines in the CSV that DictReader might process
            # depending on how the CSV is formatted.
            data = [row for row in reader if any(value.strip() for value in row.values())]
        return data

    def test_full_migration_produces_correct_shopify_csv(self):
        """
        Test the full migration process: parse -> map -> write, then compare output CSVs.
        """
        # Step 1: Parse Squarespace CSV
        self.assertTrue(os.path.exists(self.squarespace_input_csv),
                        f"Input Squarespace CSV not found: {self.squarespace_input_csv}")
        squarespace_products = parse_squarespace_csv(self.squarespace_input_csv)
        self.assertTrue(squarespace_products, "Parsing Squarespace CSV returned no products.")

        # Step 2: Map to Shopify Objects
        shopify_products = map_squarespace_to_shopify(squarespace_products)
        self.assertTrue(shopify_products, "Mapping to Shopify objects returned no products.")

        # Step 3: Write Shopify CSV
        write_shopify_csv(shopify_products, self.generated_shopify_output_csv)
        self.assertTrue(os.path.exists(self.generated_shopify_output_csv),
                        f"Generated Shopify CSV was not created: {self.generated_shopify_output_csv}")

        # Step 4: Compare CSV Files (content-wise)
        generated_data = self._read_csv_to_list_of_dicts(self.generated_shopify_output_csv)
        expected_data = self._read_csv_to_list_of_dicts(self.expected_shopify_output_csv)

        self.assertTrue(generated_data, "Generated Shopify CSV data is empty after reading.")
        self.assertTrue(expected_data, f"Expected Shopify CSV data is empty after reading ({self.expected_shopify_output_csv}).")

        self.assertEqual(len(generated_data), len(expected_data),
                         f"Row count mismatch. Generated: {len(generated_data)}, Expected: {len(expected_data)}\n"
                         f"Generated file: {self.generated_shopify_output_csv}\n"
                         f"Expected file: {self.expected_shopify_output_csv}")

        # Compare row by row, dictionary by dictionary
        for i, (gen_row, exp_row) in enumerate(zip(generated_data, expected_data)):
            # Ensure all keys from expected_data are in generated_data and vice-versa for a fair comparison
            # This is important because DictReader might not include keys for totally empty optional columns
            # if they weren't in the header of a malformed CSV, but our writer *always* writes all headers.
            # However, DictReader uses fieldnames from the header row, so keys should match if CSVs are well-formed.

            # Normalize rows: ensure all SHOPIFY_HEADERS are present with default "" if missing
            # This helps if one CSV might omit empty trailing columns that were still in headers.
            # However, DictReader should handle this by assigning None or empty string.
            # The primary concern is that both dicts should have the same set of keys derived from their headers.
            # Our _read_csv_to_list_of_dicts uses DictReader, so keys come from CSV's own header.

            self.assertDictEqual(gen_row, exp_row, f"Mismatch in row {i + 1} (1-indexed). \n"
                                                  f"Generated Row: {gen_row}\n"
                                                  f"Expected Row : {exp_row}")

if __name__ == '__main__':
    unittest.main()

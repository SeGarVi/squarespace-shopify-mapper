import unittest
import os
import csv
from product_classes import Product, Variant
from parser import (
    parse_products_csv,
    get_option_names,
    get_option_values,
    parse_bool,
    parse_float,
    parse_int,
    split_list_field,
    split_space_separated_list
)

class TestHelperFunctions(unittest.TestCase):
    def test_parse_bool(self):
        self.assertTrue(parse_bool("Yes"))
        self.assertTrue(parse_bool("yes"))
        self.assertFalse(parse_bool("No"))
        self.assertFalse(parse_bool("no"))
        self.assertFalse(parse_bool(""))
        self.assertFalse(parse_bool("random"))

    def test_parse_float(self):
        self.assertEqual(parse_float("12.34"), 12.34)
        self.assertEqual(parse_float("0"), 0.0)
        self.assertEqual(parse_float(""), 0.0)
        self.assertEqual(parse_float("abc"), 0.0)
        self.assertEqual(parse_float(None), 0.0)

    def test_parse_int(self):
        self.assertEqual(parse_int("123"), 123)
        self.assertEqual(parse_int("0"), 0)
        self.assertEqual(parse_int(""), 0)
        self.assertEqual(parse_int("abc"), 0)
        self.assertEqual(parse_int(None), 0)

    def test_split_list_field(self):
        self.assertEqual(split_list_field("a, b, c"), ["a", "b", "c"])
        self.assertEqual(split_list_field("a"), ["a"])
        self.assertEqual(split_list_field(""), [])
        self.assertEqual(split_list_field(None), [])
        self.assertEqual(split_list_field("x; y; z", delimiter=';'), ["x", "y", "z"])

    def test_split_space_separated_list(self):
        self.assertEqual(split_space_separated_list("url1 url2"), ["url1", "url2"])
        self.assertEqual(split_space_separated_list("url1"), ["url1"])
        self.assertEqual(split_space_separated_list(""), [])
        self.assertEqual(split_space_separated_list(None), [])

    def test_get_option_names(self):
        row_dict = {"Option Name 1": "Color", "Option Name 2": "Size", "Option Value 1": "Red"}
        self.assertEqual(get_option_names(row_dict), ["Color", "Size"])
        row_dict_empty = {"Option Value 1": "Red"}
        self.assertEqual(get_option_names(row_dict_empty), [])
        row_dict_gap = {"Option Name 1": "Color", "Option Name 3": "Material"} # Stops at gap
        self.assertEqual(get_option_names(row_dict_gap), ["Color"])


    def test_get_option_values(self):
        row_dict = {"Option Value 1": "Red", "Option Value 2": "Large", "Option Name 1": "Color"}
        self.assertEqual(get_option_values(row_dict, 2), ["Red", "Large"])
        self.assertEqual(get_option_values(row_dict, 1), ["Red"])
        self.assertEqual(get_option_values(row_dict, 3), ["Red", "Large", ""]) # Asks for more than available
        row_dict_empty = {"Option Name 1": "Color"}
        self.assertEqual(get_option_values(row_dict_empty, 1), [""])

class TestProductVariantClasses(unittest.TestCase):
    def test_product_creation(self):
        p = Product(product_id="p1", product_type="PHYSICAL", product_page="pp",
                    product_url="pu", title="T", description="D",
                    categories=["C1"], tags=["T1"], visible=True,
                    hosted_image_urls=["url1"], option_names=["Color"])
        self.assertEqual(p.product_id, "p1")
        self.assertEqual(p.title, "T")
        self.assertEqual(p.option_names, ["Color"])
        self.assertEqual(p.variants, [])

    def test_variant_creation(self):
        v = Variant(variant_id="v1", sku="SKU1", option_values=["Red"],
                    price=10.0, sale_price=8.0, on_sale=True, stock=5,
                    weight=0.5, length=1.0, width=2.0, height=3.0,
                    hosted_image_urls=["img1"])
        self.assertEqual(v.variant_id, "v1")
        self.assertEqual(v.sku, "SKU1")
        self.assertEqual(v.option_values, ["Red"])
        self.assertEqual(v.price, 10.0)
        self.assertTrue(v.on_sale)
        self.assertEqual(v.stock, 5)

class TestParseProductsCSV(unittest.TestCase):
    def setUp(self):
        self.csv_file_path = "products_squarespace.csv" # Assumes this file exists from previous step
        self.test_temp_products_csv = "test_temp_products.csv"

        # Headers needed for a minimal valid CSV for the parser
        self.minimal_header = [
            "Product ID [Non Editable]", "Variant ID [Non Editable]", "Product Type [Non Editable]",
            "Product Page", "Product URL", "Title", "Description", "SKU",
            "Option Name 1", "Option Value 1", "Option Name 2", "Option Value 2",
            "Option Name 3", "Option Value 3", "Option Name 4", "Option Value 4",
            "Option Name 5", "Option Value 5", "Option Name 6", "Option Value 6",
            "Price", "Sale Price", "On Sale", "Stock", "Categories", "Tags",
            "Weight", "Length", "Width", "Height", "Visible", "Hosted Image URLs"
        ]


    def tearDown(self):
        if os.path.exists(self.test_temp_products_csv):
            os.remove(self.test_temp_products_csv)

    def test_parse_full_csv(self):
        products = parse_products_csv(self.csv_file_path)
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 2)

        # Product 1: Alfombra de Lamido Navideña
        p1 = products[0]
        self.assertEqual(p1.product_id, "671d17a5bd32d801cc4b7e18")
        self.assertEqual(p1.title, "Alfombra de Lamido Navideña")
        self.assertEqual(len(p1.variants), 4)
        self.assertEqual(p1.option_names, ["Color"])
        self.assertEqual(p1.categories, ["/perro/juegos/juegos-interactivos"])
        self.assertEqual(p1.tags, ["Juego", "Alfombra", "Navidad", "Navideño", "Lamido"])
        expected_p1_images = [
            "https://images.squarespace-cdn.com/content/v1/607ec7700a233a470e2449aa/c7320585-3eb4-4014-9090-6c2cf32312c6/verde111.jpg",
            "https://images.squarespace-cdn.com/content/v1/607ec7700a233a470e2449aa/04172ffa-cdce-4e34-b1bd-869637f9b4a2/amarillo1.jpg",
            "https://images.squarespace-cdn.com/content/v1/607ec7700a233a470e2449aa/c37d9438-d18c-48fb-a897-44e2244f448a/rojo333.jpg",
            "https://images.squarespace-cdn.com/content/v1/607ec7700a233a470e2449aa/4c5522c8-d7c2-4695-a68d-980af6b7d205/marron.jpg"
        ]
        self.assertEqual(p1.hosted_image_urls, expected_p1_images)

        # Variant 1.1 (Verde)
        v1_1 = p1.variants[0]
        self.assertEqual(v1_1.variant_id, "d1911417-9b5e-40d3-aeb2-24c8c854ba04")
        self.assertEqual(v1_1.sku, "SQ3770213")
        self.assertEqual(v1_1.option_values, ["Verde"])
        self.assertEqual(v1_1.price, 8.90)
        self.assertEqual(v1_1.stock, 0)
        self.assertEqual(v1_1.hosted_image_urls, expected_p1_images) # Inherited

        # Variant 1.2 (Amarillo)
        v1_2 = p1.variants[1]
        self.assertEqual(v1_2.sku, "SQ4864940")
        self.assertEqual(v1_2.option_values, ["Amarillo"])
        self.assertEqual(v1_2.stock, 5)
        self.assertEqual(v1_2.hosted_image_urls, expected_p1_images) # Inherited

        # Product 2: Limpiador de Ojos
        p2 = products[1]
        self.assertEqual(p2.product_id, "6792a557268ad1226ad28b8f")
        self.assertEqual(p2.title, "Limpiador de Ojos")
        self.assertEqual(len(p2.variants), 1)
        self.assertEqual(p2.option_names, []) # No option names for this product

        v2_1 = p2.variants[0]
        self.assertEqual(v2_1.sku, "SQ5571153")
        self.assertEqual(v2_1.price, 7.40)
        self.assertEqual(v2_1.stock, 3)
        self.assertEqual(v2_1.option_values, [])
        self.assertEqual(v2_1.hosted_image_urls, ["https://images.squarespace-cdn.com/content/v1/607ec7700a233a470e2449aa/b422e725-d968-4f93-aa8f-19ed7c1dca40/limpiador+ojos.jpg"])


    def test_empty_csv(self):
        with open(self.test_temp_products_csv, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.minimal_header) # Write only header
        products = parse_products_csv(self.test_temp_products_csv)
        self.assertEqual(products, [])

        os.remove(self.test_temp_products_csv) # Clean up before next part of test

        with open(self.test_temp_products_csv, mode='w', encoding='utf-8') as f:
            pass # Completely empty file
        products = parse_products_csv(self.test_temp_products_csv)
        self.assertEqual(products, [])


    def test_file_not_found(self):
        products = parse_products_csv("non_existent_file.csv")
        # The parser prints an error message to console, which is acceptable for this test.
        # We just care that it returns an empty list as designed.
        self.assertEqual(products, [])

    def test_product_without_variants_after_it(self):
        # Create a CSV with only the "Limpiador de Ojos" product data
        # This product row itself is also its only variant
        limpiador_data = [
            "6792a557268ad1226ad28b8f", "1829cf88-cc16-4856-b0e6-05d170ebf350", "PHYSICAL", "shop",
            "limpiador-de-ojos", "Limpiador de Ojos", "<p>Desc</p>", "SQ5571153",
            "", "", "", "", "", "", "", "", "", "", "", "", # No options
            "7.40", "0.00", "No", "3", "/gatos/higiene-gato, /perro/higiene/biogance",
            "Biogance, Ojo", "0.0", "0.0", "0.0", "0.0", "Yes",
            "https://images.squarespace-cdn.com/content/v1/607ec7700a233a470e2449aa/b422e725-d968-4f93-aa8f-19ed7c1dca40/limpiador+ojos.jpg"
        ]
        with open(self.test_temp_products_csv, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.minimal_header)
            writer.writerow(limpiador_data)

        products = parse_products_csv(self.test_temp_products_csv)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].title, "Limpiador de Ojos")
        self.assertEqual(len(products[0].variants), 1)
        self.assertEqual(products[0].variants[0].sku, "SQ5571153")

    def test_variant_specific_image_url(self):
        # Test if variant uses its own image URL when provided,
        # and product's when variant's is empty or missing.
        test_data = [
            self.minimal_header,
            [ # Product P1, Variant V1 (has product images)
                "P1", "V1_ID", "PHYSICAL", "page", "url", "Product P1", "Desc P1", "SKU_P1V1",
                "Color", "Red", "", "", "", "", "", "", "", "", "", "",
                "10.00", "0.00", "No", "10", "Cat1", "Tag1", "0.1", "1", "1", "1", "Yes", "prod_img1.jpg prod_img2.jpg"
            ],
            [ # Variant V2 for P1 (has its own image)
                "", "V2_ID", "", "", "", "", "", "SKU_P1V2", # Product ID is blank, indicating it's a variant of P1
                "Color", "Blue", "", "", "", "", "", "", "", "", "", "",
                "12.00", "0.00", "No", "5", "", "", "0.1", "1", "1", "1", "", "var_img1.jpg" # Note: Categories, Tags, Visible for variant row usually ignored by parser
            ],
            [ # Variant V3 for P1 (image URL is blank, should inherit from P1)
                "", "V3_ID", "", "", "", "", "", "SKU_P1V3",
                "Color", "Green", "", "", "", "", "", "", "", "", "", "",
                "11.00", "0.00", "No", "8", "", "", "0.1", "1", "1", "1", "", "" # Empty image URL
            ]
        ]
        with open(self.test_temp_products_csv, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(test_data)

        products = parse_products_csv(self.test_temp_products_csv)
        self.assertEqual(len(products), 1)
        p1 = products[0]
        self.assertEqual(len(p1.variants), 3)

        self.assertEqual(p1.variants[0].sku, "SKU_P1V1") # This is the first variant, which is also the product row
        self.assertEqual(p1.variants[0].hosted_image_urls, ["prod_img1.jpg", "prod_img2.jpg"])

        self.assertEqual(p1.variants[1].sku, "SKU_P1V2")
        self.assertEqual(p1.variants[1].hosted_image_urls, ["var_img1.jpg"]) # Specific variant image

        self.assertEqual(p1.variants[2].sku, "SKU_P1V3")
        self.assertEqual(p1.variants[2].hosted_image_urls, ["prod_img1.jpg", "prod_img2.jpg"]) # Inherited from product P1


if __name__ == '__main__':
    unittest.main()

import csv

class ShopifyProductListWriter:
    def __init__(self, products, output_file=None):
        self.products = products
        self.output_file = output_file

    def write(self):
        data = []
        data.append(ShopifyProductRow.HEADER)
        for product in self.products:
            data.append(self.create_product_row(product).get_row())

        with open(self.output_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def create_product_row(self, product):
        builder = ShopifyProductRowBuilder()
        return builder.with_handle(product.handle) \
            .with_title(product.title) \
            .with_body(product.body) \
            .with_product_category(product.product_category) \
            .with_type(product.type) \
            .with_tags(product.tags) \
            .with_published(product.published) \
            .with_option_1_name(product.option_1_name) \
            .with_option_1_value(product.option_1_value) \
            .with_variant_inventory_qty(product.variant_inventory_qty) \
            .with_variant_inventory_policy(product.variant_inventory_policy) \
            .with_variant_fulfillment_service(product.variant_fulfillment_service) \
            .with_variant_price(product.variant_price) \
            .with_image_src(product.image_src) \
            .with_image_position(product.image_position) \
            .with_status(product.status) \
            .build()

class ShopifyProductRowBuilder:
    def __init__(self):
        self._fields = {
            'handle': None,
            'title': None,
            'body': None,
            'product_category': None,
            'type': None,
            'tags': None,
            'published': None,
            'option_1_name': None,
            'option_1_value': None,
            'variant_inventory_qty': None,
            'variant_inventory_policy': None,
            'variant_fulfillment_service': None,
            'variant_price': None,
            'image_src': None,
            'image_position': None,
            'status': None
        }

    def with_handle(self, value):
        self._fields['handle'] = value
        return self

    def with_title(self, value):
        self._fields['title'] = value
        return self

    def with_body(self, value):
        self._fields['body'] = value
        return self

    def with_product_category(self, value):
        self._fields['product_category'] = value
        return self

    def with_type(self, value):
        self._fields['type'] = value
        return self

    def with_tags(self, value):
        self._fields['tags'] = value
        return self

    def with_published(self, value):
        self._fields['published'] = value
        return self

    def with_option_1_name(self, value):
        self._fields['option_1_name'] = value
        return self

    def with_option_1_value(self, value):
        self._fields['option_1_value'] = value
        return self

    def with_variant_inventory_qty(self, value):
        self._fields['variant_inventory_qty'] = value
        return self
    
    def with_variant_inventory_policy(self, value):
        self._fields['variant_inventory_policy'] = value
        return self
    
    def with_variant_fulfillment_service(self, value):
        self._fields['variant_fulfillment_service'] = value
        return self

    def with_variant_price(self, value):
        self._fields['variant_price'] = value
        return self

    def with_image_src(self, value):
        self._fields['image_src'] = value
        return self

    def with_image_position(self, value):
        self._fields['image_position'] = value
        return self
    
    def with_status(self, value):
        self._fields['status'] = value
        return self

    def build(self):
        return ShopifyProductRow(**self._fields)

class ShopifyProductRow:
    HEADER = [
        "Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published",
        "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value",
        "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty",
        "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price",
        "Variant Requires Shipping", "Variant Taxable", "Variant Barcode", "Image Src", "Image Position",
        "Image Alt Text", "Gift Card", "SEO Title", "SEO Description", "Google Shopping / Google Product Category",
        "Google Shopping / Gender", "Google Shopping / Age Group", "Google Shopping / MPN",
        "Google Shopping / AdWords Grouping", "Google Shopping / AdWords Labels", "Google Shopping / Condition",
        "Google Shopping / Custom Product", "Google Shopping / Custom Label 0", "Google Shopping / Custom Label 1",
        "Google Shopping / Custom Label 2", "Google Shopping / Custom Label 3", "Google Shopping / Custom Label 4",
        "Variant Weight Unit", "Variant Tax Code", "Cost per item", "Price / International",
        "Compare At Price / International", "Status"
    ]

    def __init__(self,
            handle,
            title,
            body,
            product_category,
            type,
            tags,
            published,
            option_1_name,
            option_1_value,
            variant_inventory_qty,
            variant_inventory_policy,
            variant_fulfillment_service,
            variant_price,
            image_src,
            image_position,
            status):
        self.row = [""] * self.HEADER.__len__()
        self.row[0]= handle
        self.row[1] = title
        self.row[2] = body
        self.row[4] = product_category
        self.row[5] = type
        self.row[6] = tags
        self.row[7] = published
        self.row[8] = option_1_name
        self.row[9] = option_1_value
        self.row[17] = variant_inventory_qty
        self.row[18] = variant_inventory_policy
        self.row[19] = variant_fulfillment_service
        self.row[20] = variant_price
        self.row[25] = image_src
        self.row[26] = image_position
        self.row[49] = status
    
    def get_header(self):
        return self.HEADER
    
    def get_row(self):
        return self.row
class SquarespaceVariant:
    def __init__(self, variant_id=None, sku=None, option_name_1=None, option_value_1=None,
                 option_name_2=None, option_value_2=None, option_name_3=None, option_value_3=None,
                 price=None, sale_price=None, on_sale=None, stock=None, weight=None,
                 length=None, width=None, height=None):
        self.variant_id = variant_id
        self.sku = sku
        self.option_name_1 = option_name_1
        self.option_value_1 = option_value_1
        self.option_name_2 = option_name_2
        self.option_value_2 = option_value_2
        self.option_name_3 = option_name_3
        self.option_value_3 = option_value_3
        self.price = price
        self.sale_price = sale_price
        self.on_sale = on_sale
        self.stock = stock
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height

class SquarespaceProduct:
    def __init__(self, product_id=None, product_type=None, product_page=None, product_url=None,
                 title=None, description=None, sku=None, option_name_1=None, option_value_1=None,
                 price=None, sale_price=None, on_sale=None, stock=None,
                 categories=None, tags=None, weight=None, length=None, width=None, height=None,
                 visible=None, hosted_image_urls=None):
        self.product_id = product_id
        self.product_type = product_type
        self.product_page = product_page
        self.product_url = product_url
        self.title = title
        self.description = description
        self.sku = sku
        self.option_name_1 = option_name_1
        self.option_value_1 = option_value_1
        self.price = price
        self.sale_price = sale_price
        self.on_sale = on_sale
        self.stock = stock
        self.categories = categories if categories is not None else []
        self.tags = tags if tags is not None else []
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.visible = visible
        self.hosted_image_urls = hosted_image_urls if hosted_image_urls is not None else []
        self.variants = []

class ShopifyVariant:
    def __init__(self, title=None, sku=None, grams=None, inventory_tracker=None,
                 inventory_qty=None, inventory_policy=None, fulfillment_service=None,
                 price=None, compare_at_price=None, requires_shipping=True, taxable=True,
                 barcode=None, image_src=None, option1_name=None, option1_value=None,
                 option2_name=None, option2_value=None, option3_name=None, option_value_3=None):
        self.title = title
        self.sku = sku
        self.grams = grams
        self.inventory_tracker = inventory_tracker
        self.inventory_qty = inventory_qty
        self.inventory_policy = inventory_policy
        self.fulfillment_service = fulfillment_service
        self.price = price
        self.compare_at_price = compare_at_price
        self.requires_shipping = requires_shipping
        self.taxable = taxable
        self.barcode = barcode
        self.image_src = image_src
        self.option1_name = option1_name
        self.option1_value = option1_value
        self.option2_name = option2_name
        self.option2_value = option2_value
        self.option3_name = option3_name
        self.option3_value = option_value_3

class ShopifyProduct:
    def __init__(self, handle=None, title=None, body_html=None, vendor=None, product_category=None,
                 type=None, tags=None, published=True, option1_name=None, option1_value=None,
                 variant_sku=None, variant_price=None, variant_inventory_qty=None, image_src=None):
        self.handle = handle
        self.title = title
        self.body_html = body_html
        self.vendor = vendor
        self.product_category = product_category
        self.type = type
        self.tags = tags if tags is not None else ""
        self.published = published
        self.option1_name = option1_name
        self.option1_value = option1_value
        self.variant_sku = variant_sku
        self.variant_price = variant_price
        self.variant_inventory_qty = variant_inventory_qty
        self.image_src = image_src
        self.variants = []
        self.additional_images = []

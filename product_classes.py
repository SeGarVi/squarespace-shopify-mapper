class Product:
    def __init__(self, product_id: str, product_type: str, product_page: str,
                 product_url: str, title: str, description: str,
                 categories: list[str], tags: list[str], visible: bool,
                 hosted_image_urls: list[str], option_names: list[str],
                 variants: list = None):
        self.product_id = product_id
        self.product_type = product_type
        self.product_page = product_page
        self.product_url = product_url
        self.title = title
        self.description = description
        self.categories = categories
        self.tags = tags
        self.visible = visible
        self.hosted_image_urls = hosted_image_urls
        self.option_names = option_names
        self.variants = variants if variants is not None else []

class Variant:
    def __init__(self, variant_id: str, sku: str, option_values: list[str],
                 price: float, sale_price: float, on_sale: bool, stock: int,
                 weight: float, length: float, width: float, height: float,
                 hosted_image_urls: list[str]):
        self.variant_id = variant_id
        self.sku = sku
        self.option_values = option_values
        self.price = price
        self.sale_price = sale_price
        self.on_sale = on_sale
        self.stock = stock
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.hosted_image_urls = hosted_image_urls

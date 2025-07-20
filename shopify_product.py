class ShopifyProduct:
    def __init__(
            self,
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
            variant_price,
            image_src,
            image_position
    ):
        self.handle = handle
        self.title = title
        self.body = body
        self.product_category = product_category
        self.type = type
        self.tags = tags
        self.published = published
        self.option_1_name = option_1_name
        self.option_1_value = option_1_value
        self.variant_inventory_qty = variant_inventory_qty
        self.variant_price = variant_price
        self.image_src = image_src
        self.image_position = image_position

    def __repr__(self):
        return f"ShopifyProduct(handle={self.handle}, title={self.title}, variant_price={self.variant_price})"
    
class ShopifyProductBuilder:
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
            'variant_price': None,
            'image_src': None,
            'image_position': None
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

    def with_variant_price(self, value):
        self._fields['variant_price'] = value
        return self

    def with_image_src(self, value):
        self._fields['image_src'] = value
        return self

    def with_image_position(self, value):
        self._fields['image_position'] = value
        return self

    def build(self):
        return ShopifyProduct(**self._fields)
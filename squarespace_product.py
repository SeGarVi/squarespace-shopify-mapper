class SquarespaceProduct:
    def __init__(
        self,
        title,
        description,
        price,
        stock,
        tags,
        visible,
        hosted_image_urls
    ):
        self.title = title
        self.description = description
        self.price = price
        self.stock = stock
        self.tags = tags
        self.visible = visible
        self.hosted_image_urls = hosted_image_urls
        self.variants = []

    def add_variant(self, variant):
        if isinstance(variant, SquarespaceProductVariant):
            self.variants.append(variant)
        else:
            raise TypeError("Variant must be an instance of SquarespaceProductVariant")

    def __repr__(self):
        return f"ProductRow({self.__dict__})"

class SquarespaceProductBuilder:
    def __init__(self):
        self._fields = {
            'title': None,
            'description': None,
            'price': None,
            'stock': None,
            'tags': None,
            'visible': None,
            'hosted_image_urls': None
        }

    def with_title(self, value):
        self._fields['title'] = value
        return self

    def with_description(self, value):
        self._fields['description'] = value
        return self

    def with_price(self, value):
        self._fields['price'] = value
        return self

    def with_stock(self, value):
        self._fields['stock'] = value
        return self

    def with_tags(self, value):
        self._fields['tags'] = value
        return self

    def with_visible(self, value):
        self._fields['visible'] = value
        return self

    def with_hosted_image_urls(self, value):
        self._fields['hosted_image_urls'] = value
        return self

    def build(self):
        return SquarespaceProduct(**self._fields)

class SquarespaceProductVariant:
    def __init__(self,
        option_name_1,
        option_value_1,
        price,
        stock,
        hosted_image_urls
    ):
        self.option_name_1 = option_name_1
        self.option_value_1 = option_value_1
        self.price = price
        self.stock = stock
        self.hosted_image_urls = hosted_image_urls

class SquarespaceVariantBuilder:
    def __init__(self):
        self._fields = {
            'option_name_1': None,
            'option_value_1': None,
            'price': None,
            'stock': None,
            'hosted_image_urls': None
        }

    def with_option_name_1(self, value):
        self._fields['option_name_1'] = value
        return self

    def with_option_value_1(self, value):
        self._fields['option_value_1'] = value
        return self

    def with_price(self, value):
        self._fields['price'] = value
        return self

    def with_stock(self, value):
        self._fields['stock'] = value
        return self

    def with_hosted_image_urls(self, value):
        self._fields['hosted_image_urls'] = value
        return self

    def build(self):
        return SquarespaceProductVariant(**self._fields)

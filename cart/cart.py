from product.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product.inventory > 0:

            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
            else:
                if self.cart[product_id]['quantity'] < product.inventory:
                    self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def get_post_price(self):
        weight = sum(item['weight'] * item['quantity'] for item in self.cart.values())
        if weight == 0:
            return 0
        elif weight < 1000:
            return 7000
        elif 1000 <= weight <= 1500:
            return 30000
        elif weight >= 2000:
            return 50000
        else:
            return 60000

    def get_total_price(self):
        price = sum(item['price'] * item['quantity'] for item in self.cart.values())
        return price

    def get_final_price(self):
        return self.get_total_price() + self.get_post_price()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_dict = self.cart.copy()
        for product in products:
            cart_dict[str(product.id)]['product_id'] = product.id
            cart_dict[str(product.id)]['product_images_last_file_url'] = str(product.images.last().file.url)
            cart_dict[str(product.id)]['product_name'] = product.name
            cart_dict[str(product.id)]['product_new_price'] = product.new_price
            cart_dict[str(product.id)]['product_get_absolute_url'] = product.get_absolute_url()

        for item in cart_dict.values():
            item['total'] = item['quantity'] * item['price']
            yield item

    def save(self):
        self.session.modified = True

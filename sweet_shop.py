class Sweet:
    def __init__(self, id, name, category, price, quantity):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity 

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['name'], data['category'], data['price'], data['quantity'])

class SweetShopManagementSystem:
    def __init__(self):
        self.sweets = []

    def add_sweet(self, name, category, price, quantity):
        if not self.sweets:
            sweet_id = 1001
        else:
            sweet_id = max(s.id for s in self.sweets) + 1
        sweet = Sweet(sweet_id, name, category, price, quantity)
        self.sweets.append(sweet)
        return sweet

    def delete_sweet(self, id):
        initial_len = len(self.sweets)
        self.sweets = [s for s in self.sweets if s.id != id]
        if len(self.sweets) == initial_len:
            raise ValueError('Sweet not found')

    def view_all(self):
        return self.sweets

    def search_by_name(self, name):
        return [s for s in self.sweets if name.lower() in s.name.lower()]

    def search_by_category(self, category):
        return [s for s in self.sweets if category.lower() in s.category.lower()]

    def search_by_price_range(self, min_price, max_price):
        return [s for s in self.sweets if min_price <= s.price <= max_price]

    def purchase(self, id, qty):
        for s in self.sweets:
            if s.id == id:
                if s.quantity >= qty:
                    s.quantity -= qty
                    return
                else:
                    raise ValueError('Insufficient stock')
        raise ValueError('Sweet not found')

    def restock(self, id, qty):
        for s in self.sweets:
            if s.id == id:
                s.quantity += qty
                return
        raise ValueError('Sweet not found') 
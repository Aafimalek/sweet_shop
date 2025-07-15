import unittest
from sweet_shop import Sweet, SweetShopManagementSystem

class TestSweetShop(unittest.TestCase):
    def setUp(self):
        self.system = SweetShopManagementSystem()

    def test_add_sweet_first(self):
        sweet = self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        self.assertEqual(sweet.id, 1001)
        self.assertEqual(len(self.system.view_all()), 1)

    def test_add_sweet_sequential(self):
        self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        sweet2 = self.system.add_sweet('Gajar Halwa', 'Vegetable-Based', 30, 15)
        self.assertEqual(sweet2.id, 1002)

    def test_add_after_delete_max(self):
        s1 = self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        s2 = self.system.add_sweet('Gajar Halwa', 'Vegetable-Based', 30, 15)
        self.system.delete_sweet(s2.id)
        s3 = self.system.add_sweet('Gulab Jamun', 'Milk-Based', 10, 50)
        self.assertEqual(s3.id, 1002)

    def test_add_after_delete_non_max(self):
        s1 = self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        s2 = self.system.add_sweet('Gajar Halwa', 'Vegetable-Based', 30, 15)
        self.system.delete_sweet(s1.id)
        s3 = self.system.add_sweet('Gulab Jamun', 'Milk-Based', 10, 50)
        self.assertEqual(s3.id, 1003)

    def test_delete_sweet(self):
        sweet = self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        self.system.delete_sweet(sweet.id)
        self.assertEqual(len(self.system.view_all()), 0)

    def test_view_all(self):
        self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        self.system.add_sweet('Gajar Halwa', 'Vegetable-Based', 30, 15)
        sweets = self.system.view_all()
        self.assertEqual(len(sweets), 2)

    def test_view_all_empty(self):
        sweets = self.system.view_all()
        self.assertEqual(len(sweets), 0)

    def test_search_by_name(self):
        self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        results = self.system.search_by_name('kaju')
        self.assertEqual(len(results), 1)

    def test_search_by_name_no_match(self):
        self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        results = self.system.search_by_name('missing')
        self.assertEqual(len(results), 0)

    def test_search_by_category(self):
        self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        results = self.system.search_by_category('nut')
        self.assertEqual(len(results), 1)

    def test_search_by_category_no_match(self):
        self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        results = self.system.search_by_category('chocolate')
        self.assertEqual(len(results), 0)

    def test_search_by_price_range(self):
        self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        self.system.add_sweet('Gajar Halwa', 'Vegetable-Based', 30, 15)
        results = self.system.search_by_price_range(20, 40)
        self.assertEqual(len(results), 1)

    def test_search_by_price_range_no_match(self):
        self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        results = self.system.search_by_price_range(60, 70)
        self.assertEqual(len(results), 0)

    def test_purchase_success(self):
        sweet = self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        self.system.purchase(sweet.id, 5)
        self.assertEqual(sweet.quantity, 15)
        self.assertEqual(len(self.system.view_all()), 1)

    def test_purchase_to_zero_keeps(self):
        sweet = self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 5)
        self.system.purchase(sweet.id, 5)
        self.assertEqual(sweet.quantity, 0)
        self.assertEqual(len(self.system.view_all()), 1)

    def test_purchase_insufficient_stock(self):
        sweet = self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        with self.assertRaises(ValueError) as cm:
            self.system.purchase(sweet.id, 25)
        self.assertEqual(str(cm.exception), 'Insufficient stock')
        self.assertEqual(sweet.quantity, 20)

    def test_purchase_not_found(self):
        with self.assertRaises(ValueError) as cm:
            self.system.purchase(999, 5)
        self.assertEqual(str(cm.exception), 'Sweet not found')

    def test_restock(self):
        sweet = self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 20)
        self.system.restock(sweet.id, 10)
        self.assertEqual(sweet.quantity, 30)

    def test_restock_not_found(self):
        with self.assertRaises(ValueError) as cm:
            self.system.restock(999, 10)
        self.assertEqual(str(cm.exception), 'Sweet not found')

    def test_add_with_zero_quantity(self):
        sweet = self.system.add_sweet('Kaju Katli', 'Nut-Based', 50, 0)
        self.assertEqual(sweet.quantity, 0)
        self.assertEqual(len(self.system.view_all()), 1)  # Does not auto-delete on add

    def test_delete_not_found(self):
        with self.assertRaises(ValueError) as cm:
            self.system.delete_sweet(999)
        self.assertEqual(str(cm.exception), 'Sweet not found')

if __name__ == '__main__':
    unittest.main() 
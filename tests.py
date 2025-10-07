# test_main.py
import unittest
from unittest.mock import Mock, patch, MagicMock
from main import custom_split, add_handler, show_handler, remove_handler, quit_handler
from database import Product
import argparse

class TestMain(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()
        self.mock_product = Mock(spec=Product)
        self.mock_product.id = 1
        self.mock_product.name = "Test Product"
        self.mock_product.category = "Test Category"
        self.mock_product.date = "2023-01-01"
        self.mock_product.price = 100

    def test_custom_split_with_quoted_spaces(self):
        input_str = '"product name" category "2023-01-01"'
        result = custom_split(input_str)
        self.assertEqual(result, ['product name', 'category', '2023-01-01'])

    @patch('main.Product')
    def test_add_handler_success(self, MockProduct):
        args = argparse.Namespace(name="Test", category="Category", date="2023-01-01", price=100)
        MockProduct.return_value = self.mock_product
        result = add_handler(args, self.mock_session)
        self.mock_session.add.assert_called_once_with(self.mock_product)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(self.mock_product)
        self.assertTrue(result)

    def test_add_handler_negative_price(self):
        args = argparse.Namespace(name="Test", category="Category", date="2023-01-01", price=-100)
        result = add_handler(args, self.mock_session)
        self.mock_session.add.assert_not_called()
        self.assertTrue(result)

    def test_show_handler_no_filters(self):
        args = argparse.Namespace(category=None, date=None)
        self.mock_session.query.return_value.all.return_value = [self.mock_product]
        result = show_handler(args, self.mock_session)
        self.mock_session.query.assert_called_with(Product)
        self.assertTrue(result)

    def test_show_handler_with_category_filter(self):
        args = argparse.Namespace(category=['Electronics'], date=None)
        mock_query = Mock()
        self.mock_session.query.return_value = mock_query
        mock_query.filter.return_value.all.return_value = [self.mock_product]
        result = show_handler(args, self.mock_session)
        mock_query.filter.assert_called_once()
        self.assertTrue(result)

    def test_remove_handler_existing_product(self):
        args = argparse.Namespace(id=1)
        self.mock_session.get.return_value = self.mock_product
        result = remove_handler(args, self.mock_session)
        self.mock_session.delete.assert_called_with(self.mock_product)
        self.mock_session.commit.assert_called_once()
        self.assertTrue(result)

    def test_remove_handler_nonexistent_product(self):
        args = argparse.Namespace(id=999)
        self.mock_session.get.return_value = None
        result = remove_handler(args, self.mock_session)
        self.mock_session.delete.assert_not_called()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
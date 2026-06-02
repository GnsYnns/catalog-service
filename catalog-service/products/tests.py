from rest_framework.test import APITestCase
from .models import Product


class ProductAPITests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Casque XYZ', price_cents=8990, stock=10,
            category='electronics')
        self.low_stock_product = Product.objects.create(
            name='Clavier ABC', price_cents=4999, stock=2,
            category='electronics')

    def test_list_products(self):
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        data = {'name': 'Souris', 'price': '29.99', 'stock': 50}
        response = self.client.post('/api/v1/products/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['price_cents'], 2999)

    def test_get_nonexistent_returns_404(self):
        response = self.client.get('/api/v1/products/99999/')
        self.assertEqual(response.status_code, 404)

    def test_filter_products_by_category(self):
        response = self.client.get('/api/v1/products/?category=electronics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_negative_price_returns_400(self):
        data = {'name': 'Produit invalide', 'price': '-1.00', 'stock': 1}
        response = self.client.post('/api/v1/products/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_low_stock_action(self):
        response = self.client.get('/api/v1/products/low-stock/?threshold=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_update_product_price_updates_cents(self):
        response = self.client.patch(
            f'/api/v1/products/{self.product.id}/',
            {'price': '99.99'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price_cents, 9999)

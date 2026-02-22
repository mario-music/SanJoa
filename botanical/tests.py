from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Product, UserProfile, Order, Review, Wishlist


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Plant',
            scientific_name='Testus plantus',
            price=Decimal('25.00'),
            description='A test plant',
            category='Plants',
            stock_quantity=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Plant')
        self.assertEqual(self.product.price, Decimal('25.00'))
        self.assertTrue(self.product.is_active)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Plant')


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            membership_tier='Silver'
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.membership_tier, 'Silver')

    def test_discount_percentage(self):
        self.assertEqual(self.profile.discount_percentage, 10)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(user=self.user)

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'botanical/home.html')

    def test_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'botanical/login.html')

    def test_login_success(self):
        response = self.client.post('/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_protected_page_requires_login(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)  # Redirects to login

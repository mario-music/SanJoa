from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from botanical.models import Product, UserProfile, MembershipPlan

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database with sample data...')

        # Create sample products
        products_data = [
            {
                'name': 'Monstera Deliciosa',
                'scientific_name': 'Monstera deliciosa',
                'price': 45.00,
                'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=800&q=80',
                'description': 'Famous for its natural leaf-holes, it is a statement plant for any room.',
                'category': 'Plants',
                'tags': ['indoor', 'tropical', 'large-leaf'],
                'stock_quantity': 15,
                'featured': True
            },
            {
                'name': 'Snake Plant',
                'scientific_name': 'Dracaena trifasciata',
                'price': 25.00,
                'image_url': 'https://images.unsplash.com/photo-1593482892290-f54927ae1b30?w=800&q=80',
                'description': 'One of the toughest plants you can find. Perfect for beginners.',
                'category': 'Plants',
                'tags': ['indoor', 'low-light', 'beginner-friendly'],
                'stock_quantity': 25,
                'featured': True
            },
            {
                'name': 'Lavender Seeds',
                'price': 5.00,
                'image_url': 'https://images.unsplash.com/photo-1595181852980-0447ba9ca4d2?w=800&q=80',
                'description': 'High-quality English Lavender seeds for aromatic garden borders.',
                'category': 'Seeds',
                'tags': ['outdoor', 'fragrant', 'pollinator-friendly'],
                'stock_quantity': 100,
                'featured': False
            },
            {
                'name': 'Organic Seaweed Fertilizer',
                'price': 18.00,
                'image_url': 'https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?w=800&q=80',
                'description': 'Boost plant growth and root health with 100% organic seaweed extract.',
                'category': 'Fertilizer',
                'tags': ['organic', 'growth-booster'],
                'stock_quantity': 50,
                'featured': True
            },
            {
                'name': 'Terracotta Pot Set',
                'price': 35.00,
                'image_url': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&q=80',
                'description': 'Breathable clay pots perfect for succulents and moisture-sensitive plants.',
                'category': 'Accessories',
                'tags': ['pottery', 'classic'],
                'stock_quantity': 30,
                'featured': False
            },
            {
                'name': 'Peace Lily',
                'scientific_name': 'Spathiphyllum',
                'price': 32.00,
                'image_url': 'https://images.unsplash.com/photo-1593482892290-f54927ae1b30?w=800&q=80',
                'description': 'Elegant white blooms and air-purifying qualities make this a favorite.',
                'category': 'Plants',
                'tags': ['indoor', 'low-light', 'air-purifying'],
                'stock_quantity': 20,
                'featured': True
            },
            {
                'name': 'Tomato Seeds',
                'scientific_name': 'Solanum lycopersicum',
                'price': 4.50,
                'image_url': 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=800&q=80',
                'description': 'Heirloom tomato seeds for a bountiful harvest.',
                'category': 'Seeds',
                'tags': ['outdoor', 'edible', 'summer'],
                'stock_quantity': 150,
                'featured': False
            },
            {
                'name': 'Pothos',
                'scientific_name': 'Epipremnum aureum',
                'price': 22.00,
                'image_url': 'https://images.unsplash.com/photo-1614594895304-fe7116ac7f4a?w=800&q=80',
                'description': 'Easy-care trailing plant perfect for hanging baskets or shelves.',
                'category': 'Plants',
                'tags': ['indoor', 'trailing', 'beginner-friendly'],
                'stock_quantity': 35,
                'featured': True
            },
            {
                'name': 'Organic Compost',
                'price': 15.00,
                'image_url': 'https://images.unsplash.com/photo-1585779034823-7e9ac8faec70?w=800&q=80',
                'description': 'Rich, nutrient-dense compost for healthy soil.',
                'category': 'Fertilizer',
                'tags': ['organic', 'soil-amendment'],
                'stock_quantity': 60,
                'featured': False
            },
            {
                'name': 'Watering Can',
                'price': 28.00,
                'image_url': 'https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=800&q=80',
                'description': 'Classic copper watering can with long spout for precision watering.',
                'category': 'Accessories',
                'tags': ['tools', 'copper'],
                'stock_quantity': 25,
                'featured': False
            },
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))

        # Create default membership plans if they don't exist
        plans = [
            {
                'tier': 'Bronze',
                'price_monthly': 5.00,
                'price_yearly': 50.00,
                'discount_percentage': 5,
                'benefits': ['5% off all orders'],
                'description': 'Basic membership with small discounts.'
            },
            {
                'tier': 'Silver',
                'price_monthly': 15.00,
                'price_yearly': 150.00,
                'discount_percentage': 10,
                'benefits': ['10% off all orders', 'Priority support'],
                'description': 'Popular plan with better discounts and perks.'
            },
            {
                'tier': 'Gold',
                'price_monthly': 30.00,
                'price_yearly': 300.00,
                'discount_percentage': 15,
                'benefits': ['15% off all orders', 'Free shipping'],
                'description': 'All-inclusive membership with maximum benefits.'
            },
        ]

        for p in plans:
            plan_obj, created = MembershipPlan.objects.get_or_create(
                tier=p['tier'],
                defaults={
                    'price_monthly': p['price_monthly'],
                    'price_yearly': p['price_yearly'],
                    'discount_percentage': p['discount_percentage'],
                    'benefits': p['benefits'],
                    'description': p['description'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created membership plan: {plan_obj.tier}'))

        # Create admin user if doesn't exist
        admin_user, admin_created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@sanjoaearthcare.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if admin_created:
            admin_user.set_password('admin123')
            admin_user.save()
        
        admin_profile, admin_profile_created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={'membership_tier': 'Gold'}
        )
        if admin_created or admin_profile_created:
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin123)'))

        # Create sample user if doesn't exist
        demo_user, demo_created = User.objects.get_or_create(
            username='demo@example.com',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        if demo_created:
            demo_user.set_password('demo123')
            demo_user.save()
        
        demo_profile, demo_profile_created = UserProfile.objects.get_or_create(
            user=demo_user,
            defaults={'membership_tier': 'Silver'}
        )
        if demo_created or demo_profile_created:
            self.stdout.write(self.style.SUCCESS('Created demo user (username: demo@example.com, password: demo123)'))

        self.stdout.write(self.style.SUCCESS('Database population completed!'))

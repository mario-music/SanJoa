# SanJoa Earth Care - Django Application

**"Save Your Waste To Make Best"**

A premium botanical marketplace and sustainable earth care solutions platform built with Django.

## Features

- 🌱 **Product Marketplace** - Browse and purchase plants, seeds, fertilizers, and accessories
- 🤖 **AI Plant Doctor** - Upload plant photos for AI-powered diagnosis and care recommendations
- 👤 **User Accounts** - Complete user profile management with membership tiers
- 📦 **Order Management** - Track orders with detailed status updates
- ❤️ **Wishlist** - Save favorite products for later
- 🎨 **Beautiful UI** - Modern, responsive design with Tailwind CSS
- 🔐 **Admin Dashboard** - Comprehensive Django admin interface for managing the platform

## Tech Stack

- **Backend**: Django 5.0
- **Database**: SQLite (default) / PostgreSQL (production)
- **Frontend**: Django Templates + Tailwind CSS
- **AI Integration**: Google Gemini API (for Plant Doctor)
- **Image Handling**: Pillow

## Installation

### Prerequisites
- Python 3.10 or higher
- pip
- virtualenv (recommended)

### Setup Steps

1. **Clone or extract the project**
   ```bash
   cd sanjoa_earthcare
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows (Command Prompt)
   venv\Scripts\activate.bat
   
   # On Windows (PowerShell) - if you get execution policy error, run first:

   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

   .\venv\Scripts\Activate.ps1
   python manage.py runserver
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example env file
   # On Windows (Command Prompt)
   copy .env.example .env
   
   # On macOS/Linux
   cp .env.example .env
   
   # Edit .env and add your settings:
   # - SECRET_KEY (generate a new one for production)
   # - GEMINI_API_KEY (get from Google AI Studio)
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Populate database with sample data**
   ```bash
   python manage.py populate_db
   ```
   
   This creates:
   - Admin user: `admin` / `admin123`
   - Demo user: `demo@example.com` / `demo123`
   - 10 sample products

7. **Create a superuser (optional - if not using populate_db)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
sanjoa_earthcare/
├── config/                 # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── botanical/              # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin configuration
│   ├── apps.py
│   ├── templates/         # HTML templates
│   │   └── botanical/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── plant_doctor.html
│   │       ├── product_detail.html
│   │       ├── orders.html
│   │       ├── account.html
│   │       ├── about_us.html
│   │       ├── join_us.html
│   │       └── sales.html
│   ├── static/            # Static files (CSS, JS, images)
│   └── management/
│       └── commands/
│           └── populate_db.py
├── media/                 # Uploaded files
├── staticfiles/           # Collected static files
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Django Admin Features

The admin panel provides comprehensive management tools:

### User Profiles
- View and edit user profiles
- Manage membership tiers (None, Bronze, Silver, Gold)
- View profile pictures and contact information

### Products
- Full CRUD operations for products
- Bulk actions (activate/deactivate, mark as featured)
- Image preview
- Stock management
- View average ratings and review counts

### Orders
- Order tracking and status management
- Bulk status updates (mark as shipped/delivered)
- View order items and totals
- Shipping information management

### Reviews
- Moderate product reviews
- View ratings and comments

### Wishlists
- View user wishlists
- Track popular products

### Plant Diagnoses
- View AI-generated plant diagnoses
- Access uploaded plant images

### Newsletter
- Manage email subscriptions
- Bulk activate/deactivate subscriptions

## Key Models

### UserProfile
- Extended user model with membership tiers
- Profile pictures and contact information
- Discount percentages based on membership

### Product
- Products with categories (Plants, Seeds, Fertilizer, Accessories)
- Image support (upload or URL)
- Tags for categorization
- Stock management
- Featured products

### Order
- Order tracking with status (Processing, Confirmed, Shipped, Delivered, Cancelled)
- Auto-generated order numbers
- Shipping details

### Review
- Product reviews with 1-5 star ratings
- One review per user per product

### Wishlist
- User wishlists
- Many-to-many relationship between users and products

### PlantDiagnosis
- AI-powered plant diagnoses
- Image storage
- Diagnosis and recommendations

## API Endpoints

The application includes several API endpoints for AJAX functionality:

- `POST /api/products/` - Get products (with category filter)
- `POST /api/wishlist/toggle/` - Toggle wishlist items
- `POST /api/cart/add/` - Add items to cart
- `POST /api/diagnose-plant/` - AI plant diagnosis
- `POST /api/newsletter/subscribe/` - Newsletter subscription
- `POST /api/profile/update/` - Update user profile

## Membership Tiers

- **None**: No membership benefits
- **Bronze**: 5% discount on all orders
- **Silver**: 10% discount on all orders  
- **Gold**: 15% discount on all orders

## Development

### Running Tests
```bash
python manage.py test
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

### Making Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Production Deployment

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up proper SECRET_KEY
5. Configure static files serving
6. Use gunicorn or uwsgi
7. Set up nginx as reverse proxy
8. Configure SSL/HTTPS

Example with gunicorn:
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Environment Variables

Key environment variables (set in `.env`):

- `SECRET_KEY` - Django secret key (required)
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `GEMINI_API_KEY` - Google Gemini API key for AI features

## License

© 2024 SanJoa Earth Care. All rights reserved.

## Support

For support, email: hello@sanjoaearthcare.com

## Contributing

This is a proprietary project. Please contact the maintainers for contribution guidelines.

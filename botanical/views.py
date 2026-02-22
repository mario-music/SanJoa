from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
import json
import os

from .models import (
    Product, UserProfile, Order, OrderItem, 
    Review, Wishlist, PlantDiagnosis, Newsletter,
    MembershipPlan, MembershipPurchase
)


# ============= PAGE VIEWS =============

def home(request):
    """Homepage with product listing"""
    # Get filter parameters
    category = request.GET.get('category', 'All')
    search_query = request.GET.get('search', '')
    
    # Filter products
    products = Product.objects.filter(is_active=True)

    if category != 'All':
        products = products.filter(category=category)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(scientific_name__icontains=search_query)
        )

    # Get featured products
    featured_products = Product.objects.filter(is_active=True, featured=True)[:6]
    # Get user wishlist
    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(request.user.wishlist_items.values_list('product_id', flat=True))
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'featured_products': featured_products,
        'categories': Product.CATEGORY_CHOICES,
        'current_category': category,
        'search_query': search_query,
        'wishlist_ids': wishlist_ids,
    }
    return render(request, 'botanical/home.html', context)


def product_detail(request, pk):
    """Individual product detail page"""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    reviews = product.reviews.all()[:10]
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=pk)[:4]
    
    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'botanical/product_detail.html', context)


def login_view(request):
    """User login page"""
    if request.user.is_authenticated:
        return redirect('botanical:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('botanical:home')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'botanical/login.html')


def register_view(request):
    """User registration page"""
    if request.user.is_authenticated:
        return redirect('botanical:home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'botanical/register.html')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'botanical/register.html')
        
        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        
        # Ensure profile exists (signals may already create it)
        UserProfile.objects.get_or_create(user=user)
        
        # Auto login
        login(request, user)
        messages.success(request, f'Welcome to SanJoa Earth Care, {name}!')
        return redirect('botanical:home')
    
    return render(request, 'botanical/register.html')


@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('botanical:home')


def plant_doctor(request):
    """AI Plant Doctor page"""
    return render(request, 'botanical/plant_doctor.html')


def join_us(request):
    """Join community page"""
    return render(request, 'botanical/join_us.html')


def membership(request):
    """Browse and purchase membership plans"""
    plans = MembershipPlan.objects.filter(is_active=True).order_by('tier')
    
    current_membership = None
    active_purchase = None
    
    if request.user.is_authenticated:
        from django.utils import timezone
        today = timezone.now().date()
        
        # Get the most recent active membership purchase
        active_purchase = MembershipPurchase.objects.filter(
            user=request.user,
            status='Active',
            start_date__lte=today,
            end_date__gte=today
        ).first()
        
        if active_purchase:
            current_membership = active_purchase.plan.tier
    
    context = {
        'plans': plans,
        'current_membership': current_membership,
        'active_purchase': active_purchase,
    }
    return render(request, 'botanical/membership.html', context)


@login_required
def upgrade_membership(request, plan_id):
    """Handle membership upgrade"""
    plan = get_object_or_404(MembershipPlan, pk=plan_id, is_active=True)
    
    if request.method == 'POST':
        billing_cycle = request.POST.get('billing_cycle', 'Monthly')
        
        if billing_cycle not in ['Monthly', 'Yearly']:
            messages.error(request, 'Invalid billing cycle.')
            return redirect('botanical:membership')
        
        # Calculate pricing and dates
        price_paid = plan.price_monthly if billing_cycle == 'Monthly' else plan.price_yearly
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=30) if billing_cycle == 'Monthly' else start_date + timedelta(days=365)
        
        # Cancel any existing active memberships
        from django.utils import timezone
        today = timezone.now().date()
        existing_purchases = MembershipPurchase.objects.filter(
            user=request.user,
            status='Active',
            end_date__gte=today
        )
        for purchase in existing_purchases:
            purchase.status = 'Cancelled'
            purchase.save()
        
        # Create new membership purchase
        purchase = MembershipPurchase.objects.create(
            user=request.user,
            plan=plan,
            billing_cycle=billing_cycle,
            status='Active',
            price_paid=price_paid,
            start_date=start_date,
            end_date=end_date,
            transaction_id=f"TXN-{request.user.id}-{start_date.timestamp()}"
        )
        
        # Update user profile
        request.user.profile.membership_tier = plan.tier
        request.user.profile.save()
        
        messages.success(request, f'Successfully upgraded to {plan.tier} membership!')
        return redirect('botanical:membership')
    
    context = {
        'plan': plan,
    }
    return render(request, 'botanical/upgrade_membership.html', context)

def about_us(request):
    """About us page"""
    return render(request, 'botanical/about_us.html')


@login_required
def orders(request):
    """User orders page"""
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': user_orders,
    }
    return render(request, 'botanical/orders.html', context)


@login_required
def sales(request):
    """Sales dashboard for sellers"""
    # This is a placeholder - you can extend it based on your needs
    context = {}
    return render(request, 'botanical/sales.html', context)


@login_required
def account(request):
    """User account page"""
    profile = request.user.profile
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # Update profile
        request.user.first_name = request.POST.get('name', request.user.first_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        
        profile.phone_number = request.POST.get('phone', profile.phone_number)
        profile.address = request.POST.get('address', profile.address)
        profile.city = request.POST.get('city', profile.city)
        profile.state = request.POST.get('state', profile.state)
        profile.zip_code = request.POST.get('zip_code', profile.zip_code)
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('botanical:account')
    
    context = {
        'profile': profile,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'botanical/account.html', context)


# ============= API ENDPOINTS =============

@csrf_exempt
def api_products(request):
    """API endpoint to get products"""
    category = request.GET.get('category', 'All')
    
    products = Product.objects.filter(is_active=True)
    if category != 'All':
        products = products.filter(category=category)
    
    data = [{
        'id': p.id,
        'name': p.name,
        'scientificName': p.scientific_name,
        'price': float(p.price),
        'image': p.get_image_url,
        'description': p.description,
        'category': p.category,
        'tags': p.tags,
        'rating': p.average_rating,
        'reviews': p.review_count,
    } for p in products]
    
    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required
def api_wishlist_toggle(request):
    """API endpoint to toggle wishlist"""
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = get_object_or_404(Product, pk=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if not created:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
        
        return JsonResponse({'status': 'added'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@login_required
def api_cart_add(request):
    """API endpoint to add to cart (placeholder)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        # This is a simplified version
        # You would typically store cart in session or database
        
        return JsonResponse({'status': 'added', 'quantity': quantity})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def api_diagnose_plant(request):
    """API endpoint for plant diagnosis using Gemini AI"""
    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)
        
        image = request.FILES['image']
        
        # Save diagnosis record
        diagnosis = PlantDiagnosis.objects.create(
            user=request.user if request.user.is_authenticated else None,
            image=image,
            diagnosis='Analyzing plant health...',
            recommendations='Please wait while we analyze the image.'
        )
        
        # Here you would integrate with Gemini API
        # For now, returning a placeholder response
        
        response_data = {
            'diagnosis': 'Your plant appears to be healthy with some minor issues.',
            'recommendations': 'Ensure adequate watering and sunlight. Consider using organic fertilizer.',
        }
        
        # Update the diagnosis
        diagnosis.diagnosis = response_data['diagnosis']
        diagnosis.recommendations = response_data['recommendations']
        diagnosis.save()
        
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def api_newsletter_subscribe(request):
    """API endpoint for newsletter subscription"""
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        name = data.get('name', '')
        
        if not email:
            return JsonResponse({'error': 'Email required'}, status=400)
        
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults={'name': name}
        )
        
        if created:
            return JsonResponse({'status': 'subscribed', 'message': 'Thank you for subscribing!'})
        else:
            return JsonResponse({'status': 'exists', 'message': 'You are already subscribed!'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@login_required
def api_profile_update(request):
    """API endpoint to update user profile"""
    if request.method == 'POST':
        data = json.loads(request.body)
        
        if 'name' in data:
            request.user.first_name = data['name']
        if 'email' in data:
            request.user.email = data['email']
        request.user.save()
        
        profile = request.user.profile
        if 'membership' in data:
            profile.membership_tier = data['membership']
        if 'phone' in data:
            profile.phone_number = data['phone']
        profile.save()
        
        return JsonResponse({
            'id': request.user.id,
            'name': request.user.first_name,
            'email': request.user.email,
            'membership': profile.membership_tier,
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

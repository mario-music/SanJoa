from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg, Sum
from .models import (
    UserProfile, Product, Review, Wishlist, 
    Order, OrderItem, PlantDiagnosis, Newsletter
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for User Profiles"""
    list_display = ['user', 'membership_tier', 'phone_number', 'city', 'created_at', 'profile_image_preview']
    list_filter = ['membership_tier', 'created_at', 'state']
    search_fields = ['user__username', 'user__email', 'phone_number', 'city']
    readonly_fields = ['created_at', 'updated_at', 'profile_image_preview']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'membership_tier', 'profile_picture', 'profile_image_preview')
        }),
        ('Contact Details', {
            'fields': ('phone_number', 'address', 'city', 'state', 'zip_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def profile_image_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.profile_picture.url)
        return "No Image"
    profile_image_preview.short_description = 'Profile Picture'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Products"""
    list_display = ['name', 'category', 'price', 'stock_quantity', 'featured', 'is_active', 'average_rating', 'review_count', 'product_image_preview']
    list_filter = ['category', 'is_active', 'featured', 'created_at']
    search_fields = ['name', 'scientific_name', 'description']
    list_editable = ['price', 'stock_quantity', 'featured', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'product_image_preview', 'average_rating', 'review_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'scientific_name', 'category', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Media', {
            'fields': ('image', 'image_url', 'product_image_preview')
        }),
        ('Settings', {
            'fields': ('tags', 'is_active', 'featured')
        }),
        ('Statistics', {
            'fields': ('average_rating', 'review_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def product_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />', obj.image_url)
        return "No Image"
    product_image_preview.short_description = 'Product Image'
    
    actions = ['mark_as_featured', 'mark_as_not_featured', 'activate_products', 'deactivate_products']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(featured=True)
        self.message_user(request, f"{queryset.count()} products marked as featured.")
    mark_as_featured.short_description = "Mark selected as featured"
    
    def mark_as_not_featured(self, request, queryset):
        queryset.update(featured=False)
        self.message_user(request, f"{queryset.count()} products unmarked as featured.")
    mark_as_not_featured.short_description = "Unmark selected as featured"
    
    def activate_products(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} products activated.")
    activate_products.short_description = "Activate selected products"
    
    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} products deactivated.")
    deactivate_products.short_description = "Deactivate selected products"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Product Reviews"""
    list_display = ['user', 'product', 'rating', 'comment_preview', 'created_at']
    list_filter = ['rating', 'created_at', 'product__category']
    search_fields = ['user__username', 'product__name', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'product', 'rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Comment'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Admin interface for Wishlist"""
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at', 'product__category']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['added_at']


class OrderItemInline(admin.TabularInline):
    """Inline admin for Order Items"""
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']
    fields = ['product', 'quantity', 'price', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Orders"""
    list_display = ['order_number', 'user', 'status', 'final_total', 'created_at', 'status_badge']
    list_filter = ['status', 'created_at', 'shipping_state']
    search_fields = ['order_number', 'user__username', 'user__email', 'tracking_number']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Pricing', {
            'fields': ('total', 'discount', 'final_total')
        }),
        ('Shipping Details', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip')
        }),
        ('Tracking', {
            'fields': ('tracking_number', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'Processing': '#fbbf24',
            'Confirmed': '#60a5fa',
            'Shipped': '#a78bfa',
            'Delivered': '#34d399',
            'Cancelled': '#f87171',
        }
        color = colors.get(obj.status, '#9ca3af')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{}</span>',
            color, obj.status
        )
    status_badge.short_description = 'Status'
    
    actions = ['mark_as_shipped', 'mark_as_delivered']
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='Shipped')
        self.message_user(request, f"{queryset.count()} orders marked as shipped.")
    mark_as_shipped.short_description = "Mark selected as shipped"
    
    def mark_as_delivered(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='Delivered', delivered_at=timezone.now())
        self.message_user(request, f"{queryset.count()} orders marked as delivered.")
    mark_as_delivered.short_description = "Mark selected as delivered"


@admin.register(PlantDiagnosis)
class PlantDiagnosisAdmin(admin.ModelAdmin):
    """Admin interface for Plant Diagnoses"""
    list_display = ['user_display', 'diagnosis_preview', 'created_at', 'diagnosis_image_preview']
    list_filter = ['created_at']
    search_fields = ['user__username', 'diagnosis', 'recommendations']
    readonly_fields = ['created_at', 'diagnosis_image_preview']
    
    fieldsets = (
        ('Diagnosis Information', {
            'fields': ('user', 'image', 'diagnosis_image_preview', 'diagnosis', 'recommendations')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
        }),
    )
    
    def user_display(self, obj):
        return obj.user.username if obj.user else 'Anonymous'
    user_display.short_description = 'User'
    
    def diagnosis_preview(self, obj):
        return obj.diagnosis[:60] + '...' if len(obj.diagnosis) > 60 else obj.diagnosis
    diagnosis_preview.short_description = 'Diagnosis'
    
    def diagnosis_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.image.url)
        return "No Image"
    diagnosis_image_preview.short_description = 'Plant Image'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin interface for Newsletter Subscriptions"""
    list_display = ['email', 'name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at']
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} subscriptions activated.")
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} subscriptions deactivated.")
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"


# Customize admin site
admin.site.site_header = "SanJoa Earth Care Administration"
admin.site.site_title = "SanJoa Admin"
admin.site.index_title = "Dashboard"

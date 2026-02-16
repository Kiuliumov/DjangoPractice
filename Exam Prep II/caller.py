import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from main_app.models import Profile, Order, Product
from django.db.models import Q, Count


def populate_db():
    # 1. Create Profiles
    p1 = Profile.objects.create(
        full_name="John Doe",
        email="john@example.com",
        phone_number="123456789",
        is_active=True
    )
    p2 = Profile.objects.create(
        full_name="Jane Smith",
        email="jane@example.com",
        phone_number="987654321",
        is_active=True
    )

    # 2. Create Products
    prod1 = Product.objects.create(
        name="Laptop",
        price=1200.00,
        in_stock=10,
        is_available=True
    )
    prod2 = Product.objects.create(
        name="Smartphone",
        price=800.00,
        in_stock=5,
        is_available=True
    )

    # 3. Create Orders
    Order.objects.create(
        profile=p1,
        total_price=1200.00,
        is_completed=True
    )
    Order.objects.create(
        profile=p2,
        total_price=800.00,
        is_completed=False
    )




def get_profiles(search_string=None):
    if search_string is None:
        return ""

    # Case-insensitive partial match across three fields
    query = (
            Q(full_name__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_number__icontains=search_string)
    )

    profiles = Profile.objects.filter(query).annotate(
        num_of_orders=Count('orders')
    ).order_by('full_name')

    if not profiles.exists():
        return ""

    result = []
    for p in profiles:
        result.append(
            f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.num_of_orders}")

    return "\n".join(result)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles.exists():
        return ""

    result = [f"Profile: {p.full_name}, orders: {p.orders_count}" for p in profiles]
    return "\n".join(result)


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if not last_order:
        return ""

    product_names = last_order.products.order_by('name').values_list('name', flat=True)

    if not product_names:
        return ""

    return f"Last sold products: {', '.join(product_names)}"

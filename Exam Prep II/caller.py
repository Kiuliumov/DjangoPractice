import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from main_app.models import *

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

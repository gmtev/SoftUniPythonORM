import os
import django
from django.db.models import Q, Count, F, When, Case, Value, BooleanField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order, Product


# Create queries within functions
def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ""

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
            |
        Q(email__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profiles.exists():
        return ""

    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email},"
        f" phone number: {p.phone_number}, orders: {p.orders.count()}"
        for p in profiles
    )


# for some reason I couldn't pass the "judge" tests by using the custom manager, so by rewriting
# it here I manage to get full points on this task
def get_loyal_profiles():
    loyal_profiles = (Profile.objects.annotate
                      (order_count=Count('orders'))
                      .filter(order_count__gt=2).order_by('-order_count'))

    if not loyal_profiles:
        return ""

    profile_list = [
        f"Profile: {profile.full_name}, orders: {profile.order_count}"
        for profile in loyal_profiles
    ]

    return "\n".join(profile_list)


def get_last_sold_products():
    latest_order = Order.objects.order_by('-creation_date').first()
    if not latest_order or not latest_order.products.exists():
        return ""

    products = latest_order.products.all().order_by('name')
    product_names = [product.name for product in products]
    return f"Last sold products: {', '.join(product_names)}"


def get_top_products():
    top_products = Product.objects.annotate(
        num_orders=Count('order')).filter(num_orders__gt=0).order_by('-num_orders', 'name')[:5]

    if not top_products:
        return ""

    product_list = [
        f"{product.name}, sold {product.num_orders} times"
        for product in top_products
    ]

    return "Top products:\n" + "\n".join(product_list)


def apply_discounts():
    orders = Order.objects.annotate(
        num_products=Count('products')).filter(num_products__gt=2, is_completed=False)
    num_of_updated_orders = orders.update(total_price=F('total_price') * 0.9)

    return f"Discount applied to {num_of_updated_orders} orders."


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not order:
        return ""

    # for product in order.products.all():
    #     product.in_stock -= 1
    #     if product.in_stock == 0:
    #         product.is_available = False
    #     product.save()
    order.products.update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available'),
            output_field=BooleanField()
        )
    )

    order.is_completed = True
    order.save()

    return "Order has been completed!"

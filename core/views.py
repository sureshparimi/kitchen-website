from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LogoutView
from django.template.response import TemplateResponse
from .models import MenuItem, Category, Order, OrderItem, Testimonial
from .forms import CustomUserCreationForm, OrderForm, UserChangeForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import json
from datetime import datetime, timedelta
import random
from django.views.decorators.http import require_POST
from decimal import Decimal

def get_cart_count(request):
    cart = request.session.get('cart', {})
    return sum(cart.values()) if cart else 0

class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'
    next_page = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, self.get_farewell_message())
        response = super().dispatch(request, *args, **kwargs)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.get_farewell_message()
        return context
    
    def get_farewell_message(self):
        quotes = [
            "Thank you for dining with us! Your presence made our day special. ",
            "We hope you enjoyed your culinary journey. Come back soon! ",
            "Your satisfaction is our greatest joy. See you again! ",
            "Thank you for choosing us. We can't wait to serve you again! ",
            "Every guest is family here. Come back home soon! ",
            "Your taste in food is as excellent as your company. Visit us again! ",
            "Thanks for being part of our story. Your next amazing meal awaits! ",
            "We'll miss you until your next visit. Take care! "
        ]
        return random.choice(quotes)

def home(request):
    # Get cart count
    cart_count = get_cart_count(request)
    
    # Create default category if it doesn't exist
    category, created = Category.objects.get_or_create(
        name="South Indian Specials",
        defaults={
            'description': "Authentic South Indian delicacies prepared with traditional recipes and fresh ingredients."
        }
    )
    
    # Create categories
    breakfast_category, created = Category.objects.get_or_create(
        name="Andhra Breakfast Specials",
        defaults={
            'description': "Start your day with authentic Andhra breakfast delicacies."
        }
    )

    lunch_category, created = Category.objects.get_or_create(
        name="Lunch Specialties",
        defaults={
            'description': "Experience the rich flavors of traditional Andhra lunch items."
        }
    )

    dinner_category, created = Category.objects.get_or_create(
        name="Dinner Delights",
        defaults={
            'description': "End your day with our carefully crafted dinner selections."
        }
    )

    # Breakfast Items
    menu_items = [
        {
            'name': 'Pesarattu',
            'description': 'A nutritious green gram dosa served with ginger chutney. Made with organic green gram and served piping hot.',
            'price': 7.99,
            'image': 'https://cdn.pixabay.com/photo/2017/06/30/04/58/dosa-2457236_1280.jpg',
            'category': breakfast_category,
            'preparation_time': 15,
            'is_available': True
        },
        {
            'name': 'Upma',
            'description': 'Savory semolina breakfast dish with vegetables and ghee, garnished with curry leaves and cashews.',
            'price': 6.99,
            'image': 'https://cdn.pixabay.com/photo/2020/03/06/12/27/upma-4907510_1280.jpg',
            'category': breakfast_category,
            'preparation_time': 20,
            'is_available': True
        },
        {
            'name': 'Idli with Podi',
            'description': 'Steamed rice cakes served with spicy gunpowder and ghee. Perfect healthy breakfast option.',
            'price': 7.99,
            'image': 'https://cdn.pixabay.com/photo/2017/06/30/05/00/idli-2457238_1280.jpg',
            'category': breakfast_category,
            'preparation_time': 25,
            'is_available': True
        },
        {
            'name': 'Punugulu',
            'description': 'Deep-fried rice and urad dal batter balls with chutney. Crispy outside, soft inside.',
            'price': 5.99,
            'image': 'https://cdn.pixabay.com/photo/2020/09/06/14/07/indian-food-5549071_1280.jpg',
            'category': breakfast_category,
            'preparation_time': 15,
            'is_available': True
        }
    ]

    # Lunch Items
    lunch_items = [
        {
            'name': 'Andhra Thali',
            'description': 'Complete meal with rice, dal, curries, rasam, and accompaniments',
            'price': 14.99,
            'image': 'https://cdn.pixabay.com/photo/2016/11/23/18/42/indian-food-1854245_1280.jpg',
            'category': lunch_category,
            'preparation_time': 30,
            'is_available': True
        },
        {
            'name': 'Pulihora',
            'description': 'Traditional tamarind rice with peanuts and spices',
            'price': 9.99,
            'image': 'https://cdn.pixabay.com/photo/2020/03/06/12/27/rice-4907509_1280.jpg',
            'category': lunch_category,
            'preparation_time': 25,
            'is_available': True
        },
        {
            'name': 'Gongura Chicken',
            'description': 'Spicy chicken curry made with sorrel leaves',
            'price': 12.99,
            'image': 'https://cdn.pixabay.com/photo/2019/09/15/08/06/food-4477676_1280.jpg',
            'category': lunch_category,
            'preparation_time': 35,
            'is_available': True
        }
    ]

    # Dinner Items
    dinner_items = [
        {
            'name': 'Andhra Biryani',
            'description': 'Aromatic rice dish with spices and choice of vegetables or meat',
            'price': 15.99,
            'image': 'https://cdn.pixabay.com/photo/2019/11/15/11/33/biryani-4628019_1280.jpg',
            'category': dinner_category,
            'preparation_time': 45,
            'is_available': True
        },
        {
            'name': 'Ragi Sangati',
            'description': 'Traditional finger millet balls served with spicy curry',
            'price': 10.99,
            'image': 'https://cdn.pixabay.com/photo/2015/11/07/11/12/food-1030947_1280.jpg',
            'category': dinner_category,
            'preparation_time': 30,
            'is_available': True
        },
        {
            'name': 'Pesarattu Dosa',
            'description': 'Green gram dosa served with upma and chutney',
            'price': 11.99,
            'image': 'https://cdn.pixabay.com/photo/2017/06/30/04/58/dosa-2457236_1280.jpg',
            'category': dinner_category,
            'preparation_time': 20,
            'is_available': True
        }
    ]

    # Add all menu items
    all_items = menu_items + lunch_items + dinner_items
    for item_data in all_items:
        MenuItem.objects.get_or_create(
            name=item_data['name'],
            defaults={
                'description': item_data['description'],
                'price': item_data['price'],
                'image': item_data['image'],
                'category': item_data['category'],
                'preparation_time': item_data['preparation_time'],
                'is_available': item_data['is_available']
            }
        )
    
    categories = Category.objects.all()
    featured_items = MenuItem.objects.filter(is_available=True)[:6]
    
    # Create a sample testimonial if none exist
    if not Testimonial.objects.exists():
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if User.objects.filter(username='admin').exists():
            admin_user = User.objects.get(username='admin')
            Testimonial.objects.create(
                user=admin_user,
                content="The dosa batter from Parimi's Kitchen is simply outstanding! The fermentation is perfect, and the dosas turn out crispy every time. Highly recommended!",
                rating=5,
                is_approved=True
            )
    
    context = {
        'cart_count': cart_count,
        'categories': categories,
        'featured_items': featured_items,
    }
    return render(request, 'core/home.html', context)

def menu(request):
    cart_count = get_cart_count(request)
    categories = Category.objects.all()
    menu_items = MenuItem.objects.filter(is_available=True)
    
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'cart_count': cart_count,
    }
    return render(request, 'core/menu.html', context)

def register(request):
    cart_count = get_cart_count(request)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form, 'cart_count': cart_count})

@login_required
def cart(request):
    """Display cart contents"""
    items, total = get_cart_items(request)
    return render(request, 'core/cart.html', {
        'items': items,
        'total': total
    })

@login_required
@require_POST
def update_cart(request):
    """Handle cart updates (increase, decrease, remove items)"""
    try:
        data = json.loads(request.body)
        item_id = str(data.get('item_id'))  # Convert to string as session keys must be strings
        action = data.get('action')
        
        if not item_id or not action:
            return JsonResponse({'status': 'error', 'message': 'Missing required data'})
        
        # Get the menu item to validate it exists
        menu_item = get_object_or_404(MenuItem, id=item_id)
        
        # Get or initialize cart
        cart = request.session.get('cart', {})
        
        # Update cart based on action
        if action == 'increase':
            cart[item_id] = cart.get(item_id, 0) + 1
        elif action == 'decrease':
            if cart.get(item_id, 0) > 1:
                cart[item_id] = cart[item_id] - 1
            else:
                cart.pop(item_id, None)
        elif action == 'remove':
            cart.pop(item_id, None)
        
        # Save updated cart
        request.session['cart'] = cart
        request.session.modified = True
        
        # Calculate new totals
        quantity = cart.get(item_id, 0)
        subtotal = menu_item.price * Decimal(str(quantity)) if quantity > 0 else Decimal('0.00')
        
        # Calculate new cart total
        total = sum(
            MenuItem.objects.get(id=item_id).price * Decimal(str(qty))
            for item_id, qty in cart.items()
        )
        
        return JsonResponse({
            'status': 'success',
            'quantity': quantity,
            'subtotal': float(subtotal),
            'total': float(total),
            'cart_count': sum(cart.values())
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def get_cart_items(request):
    """Helper function to get cart items with their details"""
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    
    for item_id, quantity in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            subtotal = menu_item.price * Decimal(str(quantity))
            total += subtotal
            items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except MenuItem.DoesNotExist:
            continue
    
    return items, total

def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity', 1)
        
        if not request.session.get('cart'):
            request.session['cart'] = {}
        
        cart = request.session['cart']
        cart[item_id] = cart.get(item_id, 0) + quantity
        request.session.modified = True
        
        cart_count = get_cart_count(request)
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'message': 'Item added to cart successfully'
        })

@login_required
def checkout(request):
    """
    Handle checkout process
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pickup_time = data.get('pickup_time')
            notes = data.get('notes', '')
            cart = request.session.get('cart', {})

            if not cart:
                return JsonResponse({'status': 'error', 'message': 'Your cart is empty'})
            
            if not pickup_time:
                return JsonResponse({'status': 'error', 'message': 'Please select a pickup time'})

            try:
                pickup_datetime = datetime.fromisoformat(pickup_time)
                if pickup_datetime < datetime.now() + timedelta(minutes=30):
                    return JsonResponse({'status': 'error', 'message': 'Pickup time must be at least 30 minutes from now'})
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid pickup time format'})
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                status='pending',
                total_amount=sum(
                    MenuItem.objects.get(id=item_id).price * qty 
                    for item_id, qty in cart.items()
                ),
                pickup_time=pickup_datetime,
                notes=notes
            )
            
            # Create order items
            for item_id, quantity in cart.items():
                menu_item = MenuItem.objects.get(id=item_id)
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=menu_item.price
                )
            
            # Clear cart
            request.session['cart'] = {}
            
            return JsonResponse({
                'status': 'success',
                'redirect_url': reverse('order_confirmation', args=[order.id])
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    else:
        return redirect('login')

@login_required
def order_confirmation(request, order_id):
    cart_count = get_cart_count(request)
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_confirmation.html', {'order': order, 'cart_count': cart_count})

@login_required
def order_history(request):
    cart_count = get_cart_count(request)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/order_history.html', {'orders': orders, 'cart_count': cart_count})

@login_required
def order_detail(request, order_id):
    cart_count = get_cart_count(request)
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order, 'cart_count': cart_count})

@login_required
def cancel_order(request, order_id):
    """
    Handle order cancellation after phone confirmation.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Logic to check for phone confirmation (this can be a flag in the order model)
    if not order.is_phone_confirmed:
        messages.error(request, 'You need to confirm cancellation via phone first.')
        return redirect('order_detail', order_id=order.id)
    
    # Proceed with cancellation
    order.status = 'cancelled'
    order.save()
    messages.success(request, 'Your order has been cancelled successfully.')
    return redirect('order_history')

@login_required
def profile(request):
    """
    Display and handle user profile updates
    """
    cart_count = get_cart_count(request)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    
    # Get user's recent orders
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'recent_orders': recent_orders,
        'cart_count': cart_count,
    }
    return render(request, 'core/profile.html', context)

@login_required
def orders(request):
    cart_count = get_cart_count(request)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/orders.html', {'orders': orders, 'cart_count': cart_count})

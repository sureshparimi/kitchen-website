from .models import Testimonial
import random

def global_context(request):
    # Get approved testimonials
    testimonials = list(Testimonial.objects.filter(is_approved=True))
    
    # Get random testimonials if there are more than 5
    if len(testimonials) > 5:
        testimonials = random.sample(testimonials, 5)
    
    # Get random quote for logout
    quotes = [
        "Thank you for sharing your time with us. Your presence made our day special!",
        "We hope you enjoyed your meal. Come back soon for more delicious moments!",
        "Your satisfaction is our greatest reward. See you again soon!",
        "Thank you for choosing us. We can't wait to serve you again!",
        "Every guest is family here. Come back home soon!",
        "Your taste in food is as excellent as your company. Visit us again!",
        "Thanks for dining with us. Your next amazing meal is just a visit away!",
        "We'll miss you until your next visit. Take care and come back soon!",
    ]
    logout_quote = random.choice(quotes)
    
    return {
        'testimonials': testimonials,
        'logout_quote': logout_quote,
    }

def cart_count_processor(request):
    """
    Context processor to add cart count to all templates
    """
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if cart else 0
    return {'cart_count': cart_count}

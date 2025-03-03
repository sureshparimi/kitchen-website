from core.models import Category, MenuItem
from decimal import Decimal

# Clear existing data
Category.objects.all().delete()
MenuItem.objects.all().delete()

# Create categories
categories = {
    'Breakfast Specials': Category.objects.create(name='Breakfast Specials'),
    'Dosa Varieties': Category.objects.create(name='Dosa Varieties'),
    'Rice Specialties': Category.objects.create(name='Rice Specialties'),
    'Curries & Side Dishes': Category.objects.create(name='Curries & Side Dishes'),
    'Beverages': Category.objects.create(name='Beverages')
}

# Create menu items
menu_items = [
    {
        'category': 'Breakfast Specials',
        'name': 'Idli Sambar (4 pieces)',
        'description': """Savor our cloud-soft idlis served with piping hot sambar and fresh coconut chutney. Made from our signature fermented rice-lentil batter, these steamed delights are both nutritious and delicious.

✅ Perfectly Steamed – Light, fluffy, and melt-in-your-mouth soft
✅ Healthy Choice – High protein, naturally fermented, and easily digestible
✅ Complete Meal – Served with authentic sambar and fresh chutneys

Start your day with the authentic taste of South India! 🍚✨""",
        'price': Decimal('7.50'),
        'preparation_time': 15
    },
    {
        'category': 'Breakfast Specials',
        'name': 'Vada Sambar (2 pieces)',
        'description': """Crispy, golden-brown lentil donuts served with aromatic sambar and coconut chutney. Our vadas are crispy on the outside, soft on the inside, and packed with flavor.

✅ Perfectly Crispy – Golden brown exterior with soft, fluffy interior
✅ Authentic Recipe – Made with premium lentils and Indian spices
✅ Freshly Made – Prepared to order for the perfect crunch

Experience the perfect South Indian snack! 🍩✨""",
        'price': Decimal('6.50'),
        'preparation_time': 20
    },
    {
        'category': 'Dosa Varieties',
        'name': 'Masala Dosa',
        'description': """Experience our signature masala dosa – a crispy, golden crepe filled with perfectly spiced potato masala. Made from our fermented rice-lentil batter and served with sambar and chutneys.

✅ Extra Crispy – Perfectly thin and golden brown
✅ Flavorful Filling – Potatoes seasoned with authentic Indian spices
✅ Complete Meal – Served with sambar and two varieties of chutney

The ultimate South Indian comfort food! 🥞✨""",
        'price': Decimal('9.50'),
        'preparation_time': 20
    },
    {
        'category': 'Rice Specialties',
        'name': 'Lemon Rice',
        'description': """Aromatic basmati rice infused with tangy lemon, curry leaves, and crunchy peanuts. A perfect balance of citrus freshness and Indian spices that makes every bite memorable.

✅ Perfect Texture – Each grain separate and flavored
✅ Balanced Taste – Tangy, nutty, and mildly spiced
✅ Ready to Eat – Ideal for lunch or dinner

A refreshing twist on traditional rice! 🍚🍋✨""",
        'price': Decimal('8.50'),
        'preparation_time': 25
    },
    {
        'category': 'Curries & Side Dishes',
        'name': 'Dal Tadka',
        'description': """Rich, creamy lentils tempered with cumin, garlic, and fresh herbs. Our dal is slow-cooked to perfection and finished with a sizzling tadka of Indian spices.

✅ Rich & Creamy – Slow-cooked for perfect consistency
✅ Protein-Rich – Made with premium yellow lentils
✅ Fresh Tadka – Tempered with aromatic spices and herbs

A comforting bowl of goodness! 🥘✨""",
        'price': Decimal('7.50'),
        'preparation_time': 30
    },
    {
        'category': 'Beverages',
        'name': 'Masala Chai',
        'description': """Experience the warmth of traditional Indian chai, brewed with premium tea leaves and aromatic spices. Each cup is freshly prepared with our special blend of cardamom, ginger, and other secret spices.

✅ Perfect Blend – Premium tea leaves and fresh spices
✅ Freshly Brewed – Made to order, never pre-made
✅ Authentic Taste – Traditional recipe passed down generations

Warm your soul with a cup of tradition! ☕✨""",
        'price': Decimal('3.50'),
        'preparation_time': 10
    }
]

# Create menu items
for item in menu_items:
    MenuItem.objects.create(
        category=categories[item['category']],
        name=item['name'],
        description=item['description'],
        price=item['price'],
        preparation_time=item['preparation_time']
    )

print("Sample data created successfully!")

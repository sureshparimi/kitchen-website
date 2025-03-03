// Cart functionality
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    
    // Add to cart buttons
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            const quantity = document.querySelector(`#quantity-${itemId}`).value;
            addToCart(itemId, quantity);
        });
    });
    
    // Update quantity buttons
    document.querySelectorAll('.update-quantity').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            const action = this.dataset.action;
            updateQuantity(itemId, action);
        });
    });

    // Testimonials Slider
    const slider = document.querySelector('.testimonials-slider');
    const prevBtn = document.getElementById('prevTestimonial');
    const nextBtn = document.getElementById('nextTestimonial');
    let scrollAmount = 0;
    const cardWidth = 316; // 300px card + 16px margin

    if (slider && prevBtn && nextBtn) {
        prevBtn.addEventListener('click', () => {
            scrollAmount = Math.max(scrollAmount - cardWidth, 0);
            slider.style.transform = `translateX(-${scrollAmount}px)`;
        });

        nextBtn.addEventListener('click', () => {
            const maxScroll = slider.scrollWidth - slider.clientWidth;
            scrollAmount = Math.min(scrollAmount + cardWidth, maxScroll);
            slider.style.transform = `translateX(-${scrollAmount}px)`;
        });
    }

    // Auto-hide toasts after 5 seconds
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    });
});

// Add item to cart
function addToCart(itemId, quantity) {
    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            item_id: itemId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            updateCartCount();
            showMessage('Item added to cart successfully!', 'success');
        } else {
            showMessage('Error adding item to cart', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error adding item to cart', 'danger');
    });
}

// Update cart item quantity
function updateQuantity(itemId, action) {
    fetch('/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            item_id: itemId,
            action: action
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            showMessage('Error updating cart', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error updating cart', 'danger');
    });
}

// Update cart count in navbar
function updateCartCount() {
    fetch('/cart/count/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('cart-count').textContent = data.count;
    })
    .catch(error => console.error('Error:', error));
}

// Show message
function showMessage(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto dismiss after 3 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Form validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add('was-validated');
    });
});

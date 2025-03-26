// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Toggle Mobile Menu
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });
}
// Show the welcome modal when the page loads
document.addEventListener('DOMContentLoaded', function () {
    const welcomeModal = new bootstrap.Modal(document.getElementById('welcomeModal'));
    welcomeModal.show();
});
// JavaScript for Cart Functionality
document.addEventListener('DOMContentLoaded', function () {
    const cartPopup = document.getElementById('cartPopup');
    const closeCart = document.querySelector('.close-cart');
    const addToCartButtons = document.querySelectorAll('.btn-primary');
    const cartItemsContainer = document.querySelector('.cart-items');

    // Open Cart Popup
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function () {
            cartPopup.style.display = 'flex';

            // Add item to cart
            const productCard = button.closest('.product-card');
            const productName = productCard.querySelector('.card-title').innerText;
            const productPrice = productCard.querySelector('.price').innerText;

            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.innerHTML = `
            <p><strong>${productName}</strong> - ${productPrice}</p>
        `;
            cartItemsContainer.appendChild(cartItem);
        });
    });

    // Close Cart Popup
    closeCart.addEventListener('click', function () {
        cartPopup.style.display = 'none';
    });

    // Close Cart Popup when clicking outside
    window.addEventListener('click', function (event) {
        if (event.target === cartPopup) {
            cartPopup.style.display = 'none';
        }
    });
});
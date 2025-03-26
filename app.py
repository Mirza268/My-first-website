from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buraq_perfumes.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # For product images
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
db = SQLAlchemy(app)

# Create upload folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Models
class Perfume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    perfumes = Perfume.query.all()
    return render_template('index.html', perfumes=perfumes)

@app.route('/product/<int:perfume_id>')
def product_detail(perfume_id):
    perfume = Perfume.query.get_or_404(perfume_id)
    return render_template('product.html', perfume=perfume)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total_price=total_price)

@app.route('/add-to-cart/<int:perfume_id>', methods=['POST'])
def add_to_cart(perfume_id):
    perfume = Perfume.query.get(perfume_id)
    if perfume:
        cart = session.get('cart', [])
        cart.append({
            'id': perfume.id,
            'name': perfume.name,
            'price': perfume.price,
            'image': perfume.image
        })
        session['cart'] = cart
        return jsonify({"message": "Added to cart", "cart_size": len(cart)})
    return jsonify({"error": "Product not found"}), 404

@app.route('/remove-from-cart/<int:perfume_id>', methods=['POST'])
def remove_from_cart(perfume_id):
    cart = session.get('cart', [])
    updated_cart = [item for item in cart if item['id'] != perfume_id]
    session['cart'] = updated_cart
    return jsonify({"message": "Item removed", "cart_size": len(updated_cart)})

@app.route('/refund-policy')
def refund_policy():
    return render_template('refund_policy.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')

# Checkout with JazzCash/Easypaisa (Mock)
@app.route('/checkout', methods=['POST'])
def checkout():
    session.pop('cart', None)
    return jsonify({"message": "Order placed successfully! Payment integration pending."})

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Yahan message ko save ya email send karne ka code likho

        return jsonify({"message": "Message sent successfully!"})
    
    return render_template('contact.html')

# Admin Panel
@app.route('/admin')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    perfumes = Perfume.query.all()
    return render_template('admin/dashboard.html', perfumes=perfumes)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':  # Change in production!
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html')

@app.route('/admin/add-perfume', methods=['POST'])
def add_perfume():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    name = request.form.get('name')
    price = float(request.form.get('price'))
    description = request.form.get('description')
    
    image = request.files['image']
    if image:
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        image_path = f"uploads/{filename}"
    else:
        image_path = "default.jpg"
    
    new_perfume = Perfume(
        name=name,
        price=price,
        image=image_path,
        description=description
    )
    db.session.add(new_perfume)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

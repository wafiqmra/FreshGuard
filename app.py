import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date
from flask_mail import Mail, Message
from config import Config
from utils import is_near_expiry
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Add this to app.py (before your routes)

@app.template_test('date')
def is_date(value):
    """Test if a value is a date object"""
    from datetime import date
    return isinstance(value, date)

# Make sure this context processor is present
@app.context_processor
def utility_processor():
    def string_to_date(date_string, format='%Y-%m-%d'):
        from datetime import datetime
        return datetime.strptime(date_string, format).date()
    
    return dict(
        is_near_expiry=is_near_expiry,
        string_to_date=string_to_date
    )

# Add this to app.py
@app.template_test('date')
def is_date(value):
    """Test if a value is a date object"""
    from datetime import date
    return isinstance(value, date)

mysql = MySQL(app)
mail = Mail(app)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder uploads ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image_file(image_file):
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        return filename
    return None

def get_product_by_id(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, product_name, description, expiry_date, image FROM products WHERE id = %s AND user_id = %s",
                (product_id, session.get('user_id')))
    row = cur.fetchone()
    if row:
        return {
            'id': row[0],
            'product_name': row[1],
            'description': row[2],
            'expiry_date': row[3],
            'image_filename': row[4]
        }
    return None

def update_product(product_id, name, desc, expiry, image_filename):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE products SET product_name=%s, description=%s, expiry_date=%s, image=%s
        WHERE id=%s AND user_id=%s
    """, (name, desc, expiry, image_filename, product_id, session.get('user_id')))
    mysql.connection.commit()

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    send_expiry_notifications()

    cur = mysql.connection.cursor()
    
    # Get all products
    cur.execute("""
        SELECT id, product_name, description, expiry_date, image, created_at 
        FROM products 
        WHERE user_id=%s
        ORDER BY expiry_date ASC
    """, (session['user_id'],))
    products = cur.fetchall()
    
    # Get recent products (last 5 added)
    cur.execute("""
        SELECT id, product_name, description, expiry_date, image, created_at 
        FROM products 
        WHERE user_id=%s
        ORDER BY created_at DESC
        LIMIT 5
    """, (session['user_id'],))
    recent_products = cur.fetchall()
    
    cur.close()

    today = datetime.now().date()
    near_expiry_products = []
    expired_products = []
    
    for p in products:
        expiry_date = p[3]
        if isinstance(expiry_date, str):
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
        
        if expiry_date < today:
            expired_products.append(p)
        elif is_near_expiry(expiry_date):
            near_expiry_products.append(p)

    return render_template('index.html', 
                         products=products,
                         recent_products=recent_products,
                         near_expiry_products=near_expiry_products,
                         expired_products=expired_products,
                         today=today)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s OR username=%s", (email, username))
        existing = cur.fetchone()
        if existing:
            flash("Email atau username sudah terdaftar", 'danger')
            return redirect(url_for('signup'))

        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, hashed_password))
        mysql.connection.commit()
        flash("Registrasi berhasil, silahkan login", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password, username FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = user[2]
            flash(f"Selamat datang, {user[2]}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Email atau password salah", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Anda berhasil logout", "info")
    return redirect(url_for('login'))

@app.route('/add_product', methods=['POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    product_name = request.form['product_name']
    description = request.form['description']
    expiry_date = request.form['expiry_date']

    if 'image' not in request.files:
        flash("Tidak ada file gambar", "danger")
        return redirect(url_for('home'))

    file = request.files['image']
    if file.filename == '':
        flash("Tidak ada gambar yang dipilih", "danger")
        return redirect(url_for('home'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (user_id, product_name, description, expiry_date, image) VALUES (%s, %s, %s, %s, %s)",
                    (session['user_id'], product_name, description, expiry_date, filename))
        mysql.connection.commit()
        flash("Produk berhasil ditambahkan", "success")
    else:
        flash("Format gambar tidak didukung", "danger")

    return redirect(url_for('home'))

@app.route('/add_product_page')
def add_product_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('add_product.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s AND user_id = %s", (product_id, session['user_id']))
    mysql.connection.commit()
    flash("Produk berhasil dihapus", "success")
    return redirect(url_for('products'))

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    product = get_product_by_id(product_id)
    if not product:
        flash("Produk tidak ditemukan.", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        new_name = request.form['product_name']
        new_desc = request.form['description']
        new_expiry = request.form['expiry_date']

        if 'image' in request.files and request.files['image'].filename != '':
            image_file = request.files['image']
            filename = save_image_file(image_file)
        else:
            filename = product['image_filename']

        update_product(product_id, new_name, new_desc, new_expiry, filename)
        flash("Produk berhasil diupdate!", "success")
        return redirect(url_for('home'))

    # GET request -> render edit form dengan data produk lama
    return render_template('edit_product.html', product=product)

@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, product_name, description, expiry_date, image, created_at 
        FROM products 
        WHERE user_id=%s
        ORDER BY expiry_date ASC
    """, (session['user_id'],))
    raw_products = cur.fetchall()
    cur.close()

    # Convert all dates to date objects
    products = []
    today = datetime.today().date()
    expired_products = []
    
    for p in raw_products:
        # Convert expiry_date if it's a string
        expiry_date = p[3] if isinstance(p[3], date) else datetime.strptime(p[3], '%Y-%m-%d').date()
        
        # Create a new tuple with the converted date
        product = (p[0], p[1], p[2], expiry_date, p[4], p[5])
        products.append(product)
        
        if expiry_date < today:
            expired_products.append(product)

    return render_template('products.html',
                         products=products,
                         expired_products=expired_products,
                         today=today,
                         request=request)

@app.route('/about')
def about_page():
    return render_template('about.html')

def send_expiry_notifications():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT u.email, u.username, p.product_name, p.expiry_date, p.id
        FROM users u JOIN products p ON u.id = p.user_id
        WHERE p.notified = FALSE
    """)
    all_products = cur.fetchall()

    users_notified = set()

    for email, username, product_name, expiry_date, product_id in all_products:
        if isinstance(expiry_date, str):
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()

        if is_near_expiry(expiry_date):
            if email not in users_notified:
                users_notified.add(email)

            msg = Message(
                subject='Peringatan Produk Mendekati Kadaluarsa',
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            msg.body = f"Halo {username}, produk '{product_name}' Anda mendekati masa kadaluarsa pada tanggal {expiry_date}. Segera gunakan atau buang produk tersebut."

            try:
                mail.send(msg)
                print(f"Email terkirim ke {email} untuk produk {product_name}")

                cur2 = mysql.connection.cursor()
                cur2.execute("UPDATE products SET notified = TRUE WHERE id = %s", (product_id,))
                mysql.connection.commit()

            except Exception as e:
                print(f"Gagal kirim email ke {email}: {e}")

@app.route('/send_notifications')
def send_notifications():
    send_expiry_notifications()
    return "Email notifikasi terkirim (jika ada produk mendekati kadaluarsa)."

@app.route("/test_email")
def test_email():
    msg = Message("Test Email from FreshGuard",
                  recipients=["acckosonganyua@gmail.com"])
    msg.body = "Halo! Ini adalah email test dari FreshGuard."
    try:
        mail.send(msg)
        return "Email test berhasil dikirim!"
    except Exception as e:
        return f"Gagal kirim email: {e}"

if __name__ == '__main__':
    app.secret_key = app.config['SECRET_KEY']
    app.run(debug=True)

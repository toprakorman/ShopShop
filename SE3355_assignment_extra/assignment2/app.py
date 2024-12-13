from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)


def initDB():
    conn = sql.connect('database2.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        product_no TEXT,
        description TEXT,
        price REAL,
        image TEXT,
        category TEXT,
        sub_category_1 TEXT
    );''')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        products = [
            ('Etek', 'PR001', 'Tatlı bir etek.', 49.99, 'images/etek.jpg', 'Kadın', 'Kıyafet'),
            ('Elbise', 'PR002', 'Şık bir elbise.', 99.99, 'images/elbise.jpg', 'Kadın', 'Kıyafet'),
            ('Gömlek', 'PR003', 'Spor, gündelik bir gömlek.', 39.99, 'images/gomlek.jpg', 'Erkek', 'Kıyafet'),
            ('Takım Elbise', 'PR004', 'Resmi bir takım elbise.', 149.99, 'images/tux.jpg', 'Erkek', 'Kıyafet'),
            ('Küpe', 'PR005', 'Şık küpeler.', 24.99, 'images/kupe.jpg', 'Kadın', 'Aksesuar'),
            ('Kolye', 'PR006', 'Oldukça elegant ve zarif.', 29.99, 'images/kolye.jpg', 'Kadın', 'Aksesuar'),
            ('Saat', 'PR007', 'Lüks bir saat. En son Ali Koç takarken görüldü.', 199.99, 'images/image.jpg', 'Erkek', 'Aksesuar'),
            ('El Kremi', 'PR008', 'Kuru ciltler için.', 19.99, 'images/krem.jpg', 'Kadın', 'Bakım'),
            ('Ruj', 'PR009', 'Kremsi dokuda ve gece mavisi.', 14.99, 'images/ruj.jpg', 'Kadın', 'Bakım'),
            ('Deodorant', 'PR010', '48 gün etkili.', 14.99, 'images/deo.jpg', 'Erkek', 'Bakım'),
            ('Tıraş Makinesi', 'PR011', 'Anında keser.', 44.99, 'images/tiras.jpg', 'Erkek', 'Bakım'),
            ('Kol Düğmesi', 'PR012', 'Bu paraya sence cidden değer mi?', 199.99, 'images/kol.jpg', 'Erkek', 'Aksesuar'),
            ('Bileklik', 'PR013', 'Gerçek ametist taşından.', 69.99, 'images/bileklik.jpg', 'Erkek', 'Aksesuar'),
            ('Saç Kurutma Makinesi', 'PR014', 'Adında da yazdığı gibi.', 44.99, 'images/kurutma.jpg', 'Kadın', 'Bakım'),
            ('Çorap', 'PR015', 'Yok böyle bir kampanya. Daha iyisini bulamazsın.', 99.99, 'images/corap.jpg', 'Kadın', 'Kıyafet'),
            ('Kemer', 'PR016', 'Yeni moda.', 19.99, 'images/kemer.jpg', 'Kadın', 'Aksesuar'),
        ]
        conn.executemany("INSERT INTO products (name, product_no, description, price, image, category, sub_category_1) VALUES (?, ?, ?, ?, ?, ?, ?);", products)
        conn.commit()
    conn.close()


@app.route('/')
def home():
    conn = sql.connect('database2.db')
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products LIMIT 8")
    products = cursor.fetchall()
    conn.close()
    return render_template('home.html', products=products)


@app.route('/item/<int:item_id>')
def product_detail(item_id):
    conn = sql.connect('database2.db')
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (item_id,))
    product = cursor.fetchone()
    conn.close()

    if not product:
        return redirect(url_for('home'))

    breadcrumbs = [
        {"name": "Tüm Ürünler", "url": url_for('all_products')},
        {"name": product['category'], "url": url_for('search_results', query=product['category'])},
        {"name": product['sub_category_1'], "url": url_for('search_results', query=product['sub_category_1'])},
        {"name": product['name'], "url": None}
    ]
    return render_template('product_detail.html', product=product, breadcrumbs=breadcrumbs)



@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip()
    conn = sql.connect('database2.db')
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM products
        WHERE LOWER(name) LIKE ? OR LOWER(description) LIKE ? OR LOWER(category) LIKE ?
        OR LOWER(sub_category_1) LIKE ?
    """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
    products = cursor.fetchall()
    conn.close()
    return render_template('search_results.html', products=products, query=query)

@app.route('/all')
def all_products():
    conn = sql.connect('database2.db')
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('all_products.html', products=products)


if __name__ == '__main__':
    initDB()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from utils.logic import load_phones, calculate_profit, get_listing_status, condition_mapping

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == "admin" and password == "admin123":
        return redirect(url_for('dashboard'))
    return render_template('login.html', error="Invalid credentials")


@app.route('/dashboard', methods=['GET'])
def dashboard():
    brand_filter = request.args.get('brand', '').lower()
    model_filter = request.args.get('model', '').lower()
    
    phones = load_phones()
    platforms = ['X', 'Y', 'Z']
    phone_data = []

    for phone in phones:
        if brand_filter and brand_filter not in phone['brand'].lower():
            continue
        if model_filter and model_filter not in phone['model'].lower():
            continue

        row = {
            'id': phone['id'],
            'brand': phone['brand'],
            'model': phone['model'],
            'condition': phone['condition'],
            'price': phone['price'],
            'stock': phone['stock'],
            'sold_directly': phone['sold_directly'],
            'platforms': {}
        }
        for p in platforms:
            listed, reason = get_listing_status(phone, p)
            row['platforms'][p] = {
                'mapped_condition': condition_mapping[phone['condition']][p],
                'final_price': round(calculate_profit(phone['price'], p), 2),
                'listed': listed,
                'reason': reason
            }
        phone_data.append(row)

    return render_template('dashboard.html', phones=phone_data)

if __name__ == '__main__':
    app.run(debug=True)

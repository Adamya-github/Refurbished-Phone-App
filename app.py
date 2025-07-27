from flask import Flask, render_template, request, redirect, url_for
from utils.logic import load_phones, calculate_profit, is_listed, condition_mapping

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    phones = load_phones()
    platforms = ['X', 'Y', 'Z']
    phone_data = []

    for phone in phones:
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
            row['platforms'][p] = {
                'mapped_condition': condition_mapping[phone['condition']][p],
                'final_price': round(calculate_profit(phone['price'], p), 2),
                'listed': is_listed(phone, p)
            }
        phone_data.append(row)

    return render_template('dashboard.html', phones=phone_data)

if __name__ == '__main__':
    app.run(debug=True)

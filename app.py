
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Sample inventory data (list of dictionaries)
inventory = [
    {"name": "Laptop", "quantity": 10, "price": 60000, "category": "Electronics"},
    {"name": "Apple", "quantity": 50, "price": 120, "category": "Groceries"}
]

# Home route to display inventory
@app.route('/')
def index():
    total_value = sum(item['quantity'] * item['price'] for item in inventory)
    return render_template('index.html', inventory=inventory, total_value=total_value)

# Route to add an item
@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    category = request.form['category']
    
    # Basic validations
    if name and quantity > 0 and price > 0:
        inventory.append({"name": name, "quantity": quantity, "price": price, "category": category})
    return redirect(url_for('index'))

# Route to update an item
@app.route('/update', methods=['POST'])
def update_item():
    index = int(request.form['index'])
    inventory[index]['name'] = request.form['name']
    inventory[index]['quantity'] = int(request.form['quantity'])
    inventory[index]['price'] = float(request.form['price'])
    inventory[index]['category'] = request.form['category']
    return redirect(url_for('index'))

# Route to delete an item
@app.route('/delete/<int:index>')
def delete_item(index):
    if index < len(inventory):
        inventory.pop(index)
    return redirect(url_for('index'))

# Route for sorting items
@app.route('/sort/<string:order>')
def sort_items(order):
    if order == 'asc':
        inventory.sort(key=lambda x: x['price'])
    elif order == 'desc':
        inventory.sort(key=lambda x: x['price'], reverse=True)
    return redirect(url_for('index'))

# Route for searching items
@app.route('/search', methods=['GET'])
def search_items():
    query = request.args.get('q').lower()
    filtered_inventory = [item for item in inventory if query in item['name'].lower() or query in item['category'].lower()]
    total_value = sum(item['quantity'] * item['price'] for item in filtered_inventory)
    return render_template('index.html', inventory=filtered_inventory, total_value=total_value)

if __name__ == '__main__':
    app.run(debug=True)

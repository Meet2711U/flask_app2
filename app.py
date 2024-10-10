from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Connection
mongo_client = MongoClient("mongodb+srv://Dadyscale18:pOvnOAnGNrHsQu4Q@assignment2.oat4h.mongodb.net/?retryWrites=true&w=majority&appName=Assignment2")
db = mongo_client["app"]
products_collection = db["products"]  


mock_data = [
    {"name": "Laptop", "tag": "Electronics", "price": 899.99, "image_path": "static/images/laptop.png"},
    {"name": "Coffee Mug", "tag": "Kitchenware", "price": 12.99, "image_path": "static/images/coffee_mug.png"},
    {"name": "Headphones", "tag": "Electronics", "price": 199.99, "image_path": "static/images/headphone.jpg"}
]

# products_collection.insert_many(mock_data)

@app.route("/")
def index():
    return render_template("home.html")

@app.route('/products')
def show_products():
    all_products = products_collection.find()  
    return render_template('products.html', products=all_products)

if __name__ == '__main__':
    app.run(debug=True)

import pytest
from app import app # Import the Flask app
from pymongo import MongoClient
import os

# Fixture for the Flask test client
@pytest.fixture
def client():
    # Set up the Flask test client
    with app.test_client() as client:
        yield client

# Fixture for the MongoDB client
@pytest.fixture
def mongo_client():
    # Load credentials from environment variables (set by GitHub Secrets)
    db_username = os.getenv("DB_USERNAME")  # GitHub Secret
    db_password = os.getenv("DB_PASSWORD")  # GitHub Secret
    
    # Check if MongoDB credentials are provided
    if not db_username or not db_password:
        raise ValueError("MongoDB credentials are not set in GitHub Secrets")
    
    # Create a MongoDB client using credentials from environment variables
    client = MongoClient(f"mongodb+srv://{db_username}:{db_password}@assignment2.oat4h.mongodb.net/?retryWrites=true&w=majority&appName=Assignment2")
    yield client
    client.close()

# Fixture to access the 'app' database
@pytest.fixture
def db(mongo_client):
    # Access the database and collection
    db = mongo_client["app"]
    yield db
    # Cleanup: Delete test data after each test
    db.products.delete_many({"name": "Test Product"})  # Adjust as needed for other tests

# Test 1: Invalid HTTP Method to Products Route
def test_invalid_method_to_products(client):
    """
    Test to verify that sending a POST request to the /products route,
    which only accepts GET requests, returns a 405 status code.
    """
    response = client.post('/products')
    assert response.status_code == 405  # Method Not Allowed

# Test 2: Check MongoDB Connection
def test_mongo_connection(mongo_client):
    """
    Test to verify the MongoDB connection by sending a ping command
    to the database and checking the response.
    """
    # Ping the MongoDB server
    assert mongo_client.admin.command('ping')['ok'] == 1

# Test 3: Write Data to Database
def test_write_data_to_db(db):
    """
    Test to insert a document into the 'products' collection in MongoDB
    and verify that the insertion was successful.
    """
    # Define test data
    new_data = {"name": "Test Product", "tag": "Test", "price": 99.99}
    
    # Insert the test data into the database
    db.products.insert_one(new_data)
    
    # Verify that the data was inserted correctly
    inserted_data = db.products.find_one({"name": "Test Product"})
    assert inserted_data is not None
    assert inserted_data['name'] == 'Test Product'
    
    # Cleanup: Remove the test data to maintain a clean database
    db.products.delete_one({"name": "Test Product"})

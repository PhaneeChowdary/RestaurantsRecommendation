import os
import json
from bson import json_util, ObjectId
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS to allow all origins and methods
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
        "expose_headers": ["Access-Control-Allow-Origin"],
        "supports_credentials": True
    }
})

# MongoDB connection
try:
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    db = client[os.getenv("DB_NAME", "restaurants_db")]
    collection = db["Yelp"]
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")


@app.route("/api/restaurants", methods=["GET"])
def get_restaurants():
    try:
        # Get filter parameters
        city = request.args.get("city")
        price_range_min = request.args.get("price_range_min")
        categories = request.args.get("categories")
        parking = request.args.get("parking")
        sort = request.args.get("sort", "stars")
        order = int(request.args.get("order", "-1"))
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        
        # Calculate skip value for pagination
        skip = (page - 1) * per_page

        # Build query
        query = {}

        # Add city filter if provided
        if city and city != "don't include":
            query["city"] = city  # Exact match on city

        # Add price range filter
        if price_range_min and price_range_min != "don't include":
            query["attributes.RestaurantsPriceRange2"] = str(price_range_min)
        
        if categories:
            query["categories"] = {"$regex": categories, "$options": "i"}

        # Handle parking
        if parking and parking != "don't include":
            try:
                parking_dict = json.loads(parking)
                for key, value in parking_dict.items():
                    query["attributes.BusinessParking"] = {
                        "$regex": f"'{key}':\\s*{value}"
                    }
            except json.JSONDecodeError as e:
                print(f"Error parsing parking JSON: {parking}, Error: {str(e)}")

        # Debug: Print the final query
        print("Final query:", query)

        # Get total count
        total_count = collection.count_documents(query)

        # Define projection
        projection = {
            "name": 1,
            "city": 1,
            "state": 1,
            "stars": 1,
            "review_count": 1,
            "categories": 1,
            "attributes": 1,
            "hours": 1,
            "address": 1
        }

        # Execute query with projection, sorting, and pagination
        restaurants = (
            collection.find(query, projection)
            .sort([(sort, order), ("review_count", -1)])
            .skip(skip)
            .limit(per_page)
        )

        # Convert to list and handle serialization
        restaurants_list = json.loads(json_util.dumps(list(restaurants)))

        response = {
            "restaurants": restaurants_list,
            "total_count": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page,
            "query": query
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/restaurants", methods=["POST"])
def create_restaurant():
    try:
        restaurant_data = request.json
        
        # Format the parking data
        if 'parking' in restaurant_data:
            restaurant_data['attributes'] = restaurant_data.get('attributes', {})
            restaurant_data['attributes']['BusinessParking'] = str(restaurant_data['parking'])
            del restaurant_data['parking']

        # Add other attributes
        if 'price_range' in restaurant_data:
            restaurant_data['attributes']['RestaurantsPriceRange2'] = restaurant_data['price_range']
            del restaurant_data['price_range']
            
        if 'wifi' in restaurant_data:
            restaurant_data['attributes']['WiFi'] = restaurant_data['wifi']
            del restaurant_data['wifi']

        # Set default values
        restaurant_data['stars'] = 0.0
        restaurant_data['review_count'] = 0

        result = collection.insert_one(restaurant_data)
        return jsonify({
            "message": "Restaurant created successfully",
            "id": str(result.inserted_id)
        }), 201
    except Exception as e:
        print(f"Error creating restaurant: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/restaurants/<id>", methods=["PUT"])
def update_restaurant(id):
    try:
        restaurant_data = request.json

        # Format the parking data
        if 'parking' in restaurant_data:
            if 'attributes' not in restaurant_data:
                restaurant_data['attributes'] = {}
            restaurant_data['attributes']['BusinessParking'] = str(restaurant_data['parking'])
            del restaurant_data['parking']

        # Update other attributes
        if 'price_range' in restaurant_data:
            if 'attributes' not in restaurant_data:
                restaurant_data['attributes'] = {}
            restaurant_data['attributes']['RestaurantsPriceRange2'] = restaurant_data['price_range']
            del restaurant_data['price_range']
            
        if 'wifi' in restaurant_data:
            if 'attributes' not in restaurant_data:
                restaurant_data['attributes'] = {}
            restaurant_data['attributes']['WiFi'] = restaurant_data['wifi']
            del restaurant_data['wifi']

        result = collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": restaurant_data}
        )
        
        if result.modified_count:
            return jsonify({"message": "Restaurant updated successfully"}), 200
        return jsonify({"message": "No changes made"}), 200
    except Exception as e:
        print(f"Error updating restaurant: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/restaurants/<id>", methods=["DELETE"])
def delete_restaurant(id):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Restaurant deleted successfully"}), 200
        return jsonify({"message": "Restaurant not found"}), 404
    except Exception as e:
        print(f"Error deleting restaurant: {str(e)}")
        return jsonify({"error": str(e)}), 500

    
@app.route("/api/test", methods=["GET"])
def test_restaurants():
    try:
        # Get just one document to verify structure
        sample_doc = collection.find_one()
        if sample_doc:
            return jsonify({
                "sample_document": json.loads(json_util.dumps(sample_doc)),
                "message": "Found a document"
            })
        else:
            return jsonify({
                "message": "No documents found in collection",
                "collection_name": "Yelp",
                "database_name": db.name
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
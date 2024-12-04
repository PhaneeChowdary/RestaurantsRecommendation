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


# In app.py - Updated get_restaurants route
@app.route("/api/restaurants", methods=["GET"])
def get_restaurants():
    try:
        # Get all filter parameters
        name = request.args.get("name")  # Add this line for name search
        # Debug prints
        print("Received name parameter:", name)

        city = request.args.get("city")
        price_range_min = request.args.get("price_range_min")
        alcohol = request.args.get("alcohol")
        delivery = request.args.get("delivery")
        wifi = request.args.get("wifi")
        dogs_allowed = request.args.get("pets_allowed")
        parking = request.args.get("parking")
        min_stars = request.args.get("minStars")

        # Get pagination parameters
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        skip = (page - 1) * per_page

        # Debug prints
        print("Received parameters:", dict(request.args))
        print("Page:", page)
        print("Skip:", skip)
        print("Per page:", per_page)

        # Build query
        query = {}

        # Name search (case-insensitive partial match)
        if name and name.strip():
            query["name"] = {
                "$regex": f".*{name.strip()}.*",  # Changed this line to include .* on both sides
                "$options": "i"
            }
            # Debug print
            print("Final name query:", query)

        # City filter (case-insensitive)
        if city and city != "don't include":
            query["city"] = {"$regex": f"^{city}$", "$options": "i"}

        # Price range filter
        if price_range_min and price_range_min != "don't include":
            query["attributes.RestaurantsPriceRange2"] = str(price_range_min)

        # WiFi filter (case-insensitive)
        if wifi and wifi != "don't include":
            query["attributes.WiFi"] = {"$regex": f"^{wifi}$", "$options": "i"}

        # Alcohol filter (case-insensitive)
        if alcohol and alcohol != "don't include":
            query["attributes.Alcohol"] = {"$regex": f"^{alcohol}$", "$options": "i"}

        # Star rating filter
        if min_stars:
            query["stars"] = {"$gte": float(min_stars)}

        # Delivery filter (boolean)
        if delivery == "true":
            query["$or"] = [
                {"attributes.RestaurantsDelivery": True},
                {"attributes.RestaurantsDelivery": "True"},
                {"attributes.RestaurantsDelivery": "true"}
            ]
        elif delivery == "false":
            query["$or"] = [
                {"attributes.RestaurantsDelivery": False},
                {"attributes.RestaurantsDelivery": "False"},
                {"attributes.RestaurantsDelivery": "false"}
            ]

        # Dogs/Pets allowed filter (boolean)
        if dogs_allowed == "true":
            query["$or"] = [
                {"attributes.DogsAllowed": True},
                {"attributes.DogsAllowed": "True"},
                {"attributes.DogsAllowed": "true"}
            ]
        elif dogs_allowed == "false":
            query["$or"] = [
                {"attributes.DogsAllowed": False},
                {"attributes.DogsAllowed": "False"},
                {"attributes.DogsAllowed": "false"}
            ]

        # Parking filter
        if parking and parking != "don't include":
            try:
                parking_dict = json.loads(parking)
                for key, value in parking_dict.items():
                    if str(value).lower() == "true":
                        query["attributes.BusinessParking"] = {
                            "$regex": f"'{key}':\\s*(True|true)", 
                            "$options": "i"
                        }
                    elif str(value).lower() == "false":
                        query["attributes.BusinessParking"] = {
                            "$regex": f"'{key}':\\s*(False|false)", 
                            "$options": "i"
                        }
            except json.JSONDecodeError as e:
                print(f"Error parsing parking JSON: {parking}, Error: {str(e)}")

        # Smoking filter (case-insensitive)
        smoking = request.args.get("smoking")
        if smoking and smoking != "don't include":
            query["attributes.Smoking"] = {"$regex": f"^{smoking}$", "$options": "i"}

        # Debug print final query
        print("Final MongoDB Query:", json.dumps(query, indent=2))

        # Get total count before pagination
        total_count = collection.count_documents(query)
        print(f"Total matching documents: {total_count}")

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

        # Execute query with pagination
        restaurants = list(collection.find(query, projection)
                         .sort([("stars", -1), ("review_count", -1)])
                         .skip(skip)
                         .limit(per_page))

        print(f"Found {len(restaurants)} restaurants for page {page}")

        response = {
            "restaurants": json.loads(json_util.dumps(restaurants)),
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



@app.route("/api/filters", methods=["GET"])
def get_filter_options():
    """Endpoint to get all possible filter values"""
    try:
        # Get distinct values from the database for various attributes
        distinct_alcohol = collection.distinct("attributes.Alcohol")
        distinct_smoking = collection.distinct("attributes.Smoking")
        distinct_wifi = collection.distinct("attributes.WiFi")

        filter_options = {
            "price_range": ["1", "2", "3", "4"],
            "parking": {
                "garage": ["true", "false"],
                "street": ["true", "false"],
                "validated": ["true", "false"],
                "lot": ["true", "false"],
                "valet": ["true", "false"]
            },
            "pets_allowed": ["true", "false"],
            "delivery": ["true", "false"],
            "alcohol": sorted([opt for opt in distinct_alcohol if opt]),
            "smoking": sorted([opt for opt in distinct_smoking if opt]),
            "wifi": sorted([opt for opt in distinct_wifi if opt])
        }
        return jsonify(filter_options)
    except Exception as e:
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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
import json
import ijson
from pymongo import MongoClient
from datetime import datetime
from pprint import pprint
from decimal import Decimal


def convert_decimal(obj):
    """Recursively convert Decimal instances to float."""
    if isinstance(obj, list):
        return [convert_decimal(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_decimal(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj


def verify_attributes(collection):
    print("\nVerifying Attributes Structure:")
    print("-" * 50)

    # Get a sample document to verify structure
    sample_doc = collection.find_one({})
    if sample_doc and 'attributes' in sample_doc:
        print("Sample document attributes:")
        pprint(sample_doc['attributes'])

        # Count documents with each attribute
        print("\nAttribute Coverage Analysis:")
        print("-" * 30)
        attributes_list = sample_doc['attributes'].keys()

        for attr in sorted(attributes_list):
            count = collection.count_documents({f"attributes.{attr}": {"$exists": True}})
            print(f"{attr}: {count} documents")

            # Show value distribution for key attributes
            if attr in ['RestaurantsPriceRange', 'WiFi', 'Alcohol', 'Smoking']:
                pipeline = [
                    {"$match": {f"attributes.{attr}": {"$exists": True}}},
                    {"$group": {"_id": f"$attributes.{attr}", "count": {"$sum": 1}}},
                    {"$sort": {"_id": 1}}
                ]
                print(f"\nValue distribution for {attr}:")
                for result in collection.aggregate(pipeline):
                    print(f"  {result['_id']}: {result['count']} documents")
                print()


def upload_to_mongodb(file_path, connection_string, db_name, collection_name):
    # Initialize MongoDB connection
    try:
        client = MongoClient(connection_string)
        db = client[db_name]
        collection = db[collection_name]

        print(f"Connected to MongoDB database: {db_name}")

        # Drop existing collection if it exists
        if collection_name in db.list_collection_names():
            print(f"Dropping existing collection: {collection_name}")
            db[collection_name].drop()

        # Initialize counters
        total_documents = 0
        batch_size = 1000
        current_batch = []
        start_time = datetime.now()

        print("Starting data upload...")

        # Process the file
        with open(file_path, 'rb') as file:
            parser = ijson.items(file, 'item')

            for restaurant in parser:
                restaurant = convert_decimal(restaurant)
                total_documents += 1
                current_batch.append(restaurant)

                # Insert batch when it reaches batch_size
                if len(current_batch) >= batch_size:
                    collection.insert_many(current_batch)
                    print(f"Uploaded {total_documents} documents...")
                    current_batch = []

            # Insert any remaining documents
            if current_batch:
                collection.insert_many(current_batch)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Create indexes
        print("\nCreating indexes...")
        collection.create_index([("name", 1)])
        collection.create_index([("attributes.RestaurantsPriceRange", 1)])
        collection.create_index([("state", 1)])
        collection.create_index([("city", 1)])
        collection.create_index([("stars", 1)])
        collection.create_index([("categories", 1)])
        collection.create_index([("attributes.WiFi", 1)])
        collection.create_index([("attributes.Alcohol", 1)])
        collection.create_index([("attributes.RestaurantsDelivery", 1)])

        # Print summary
        print("\nUpload Summary:")
        print("-" * 30)
        print(f"Total documents uploaded: {total_documents}")
        print(f"Time taken: {duration:.2f} seconds")
        print(f"Upload rate: {total_documents / duration:.2f} documents/second")

        # Verify upload
        actual_count = collection.count_documents({})
        print(f"\nVerification:")
        print(f"Documents in collection: {actual_count}")
        if actual_count == total_documents:
            print("✅ Upload verified successfully!")
        else:
            print("❌ Warning: Document count mismatch!")

        # Verify attributes structure
        verify_attributes(collection)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        client.close()
        print("\nMongoDB connection closed")


def main():
    # MongoDB connection details
    connection_string = "mongodb://localhost:27017"  # Replace with your connection string
    db_name = "restaurants_db"  # Replace with your database name
    collection_name = "Yelp"  # Replace with your collection name

    try:
        file_path = "cleaned_restaurants.json"
        print(f"Starting upload of {file_path} to MongoDB")
        upload_to_mongodb(file_path, connection_string, db_name, collection_name)

    except FileNotFoundError:
        print("Error: JSON file not found!")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()



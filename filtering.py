import json
import ijson
from ast import literal_eval


def analyze_unique_values(file_path):
    # Initialize sets for unique values
    unique_values = {
        'wifi_values': set(),  # WiFi
        'dogs_values': set(),  # DogsAllowed
        'parking_values': {  # BusinessParking
            'garage': set(),
            'street': set(),
            'validated': set(),
            'lot': set(),
            'valet': set(),
            'unparseable': set()
        },
        'bike_parking_values': set(),  # BikeParking
        'alcohol_values': set(),  # Alcohol
        'delivery_values': set(),  # RestaurantsDelivery
        'takeout_values': set(),  # RestaurantsTakeOut
        'caters_values': set(),  # Caters
        'smoking_values': set(),  # Smoking
        'price_values': set()  # RestaurantsPriceRange2
    }

    total_restaurants = 0

    print("Starting analysis...")

    with open(file_path, 'rb') as file:
        parser = ijson.items(file, 'item')

        for restaurant in parser:
            total_restaurants += 1
            if total_restaurants % 1000 == 0:
                print(f"Processed {total_restaurants} restaurants...")

            attributes = restaurant.get('attributes', {})

            # Process each attribute
            if 'WiFi' in attributes:
                unique_values['wifi_values'].add(str(attributes['WiFi']))

            if 'DogsAllowed' in attributes:
                unique_values['dogs_values'].add(str(attributes['DogsAllowed']))

            if 'BusinessParking' in attributes:
                parking_value = attributes['BusinessParking']
                if parking_value not in ['None', None]:
                    try:
                        parking_dict = literal_eval(str(parking_value))
                        if isinstance(parking_dict, dict):
                            for parking_key, parking_value in parking_dict.items():
                                unique_values['parking_values'][parking_key].add(str(parking_value))
                    except:
                        unique_values['parking_values']['unparseable'].add(str(parking_value))

            if 'BikeParking' in attributes:
                unique_values['bike_parking_values'].add(str(attributes['BikeParking']))

            if 'Alcohol' in attributes:
                unique_values['alcohol_values'].add(str(attributes['Alcohol']))

            if 'RestaurantsDelivery' in attributes:
                unique_values['delivery_values'].add(str(attributes['RestaurantsDelivery']))

            if 'RestaurantsTakeOut' in attributes:
                unique_values['takeout_values'].add(str(attributes['RestaurantsTakeOut']))

            if 'Caters' in attributes:
                unique_values['caters_values'].add(str(attributes['Caters']))

            if 'Smoking' in attributes:
                unique_values['smoking_values'].add(str(attributes['Smoking']))

            if 'RestaurantsPriceRange2' in attributes:
                unique_values['price_values'].add(str(attributes['RestaurantsPriceRange2']))

    return unique_values, total_restaurants


def print_unique_values(unique_values, total_restaurants):
    print(f"\nAnalysis complete. Processed {total_restaurants} restaurants.\n")
    print("UNIQUE VALUES FOR EACH ATTRIBUTE:")
    print("=" * 50)

    # WiFi
    print("\nWiFi values:")
    print("-" * 30)
    print(sorted(unique_values['wifi_values']))

    # DogsAllowed
    print("\nDogs Allowed values:")
    print("-" * 30)
    print(sorted(unique_values['dogs_values']))

    # BusinessParking
    print("\nParking options and their possible values:")
    print("-" * 30)
    for parking_type, parking_values in unique_values['parking_values'].items():
        if parking_values:  # Only print if there are values
            print(f"{parking_type}: {sorted(parking_values)}")

    # BikeParking
    print("\nBike Parking values:")
    print("-" * 30)
    print(sorted(unique_values['bike_parking_values']))

    # Alcohol
    print("\nAlcohol values:")
    print("-" * 30)
    print(sorted(unique_values['alcohol_values']))

    # Delivery
    print("\nDelivery values:")
    print("-" * 30)
    print(sorted(unique_values['delivery_values']))

    # TakeOut
    print("\nTake Out values:")
    print("-" * 30)
    print(sorted(unique_values['takeout_values']))

    # Caters
    print("\nCaters values:")
    print("-" * 30)
    print(sorted(unique_values['caters_values']))

    # Smoking
    print("\nSmoking values:")
    print("-" * 30)
    print(sorted(unique_values['smoking_values']))

    # Price Range
    print("\nPrice Range values:")
    print("-" * 30)
    print(sorted(unique_values['price_values']))


def main():
    try:
        file_path = "cleaned_restaurants.json"
        print(f"Starting analysis of {file_path}")
        unique_values, total = analyze_unique_values(file_path)
        print_unique_values(unique_values, total)

    except FileNotFoundError:
        print("Error: File not found!")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
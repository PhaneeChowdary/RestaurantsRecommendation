import json
import ijson
from ast import literal_eval
from decimal import Decimal


# Custom JSON encoder to handle Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def clean_wifi(value):
    if value in ["u'free'", "'free'"]:
        return "free"
    elif value in ["u'no'", "'no'"]:
        return "no"
    elif value in ["u'paid'", "'paid'"]:
        return "paid"
    return "no"  # default value


def clean_boolean_with_none(value):
    if value in ['None', None, 'False', False]:
        return False
    return True


def clean_alcohol(value):
    if value in ["u'beer_and_wine'", "'beer_and_wine'"]:
        return "beer_and_wine"
    elif value in ["u'full_bar'", "'full_bar'"]:
        return "full_bar"
    return "none"


def clean_smoking(value):
    if value in ["u'no'", "'no'", "None", None]:
        return "no"
    elif value in ["u'outdoor'", "'outdoor'"]:
        return "outdoor"
    elif value in ["u'yes'", "'yes'"]:
        return "yes"
    return "no"


def clean_parking_dict(parking_str):
    if parking_str in ['None', None]:
        return "{'garage': False, 'street': False, 'validated': False, 'lot': False, 'valet': False}"

    try:
        parking_dict = literal_eval(str(parking_str))
        if isinstance(parking_dict, dict):
            # Clean up each value in the parking dictionary
            cleaned_dict = {}
            for key in ['garage', 'street', 'validated', 'lot', 'valet']:
                cleaned_dict[key] = bool(parking_dict.get(key)) if parking_dict.get(key) not in [None,
                                                                                                 'None'] else False
            return str(cleaned_dict)
    except:
        return "{'garage': False, 'street': False, 'validated': False, 'lot': False, 'valet': False}"

    return parking_str


def clean_data(input_file, output_file):
    print("Starting data cleaning process...")
    total_processed = 0

    # Open output file first to start fresh
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write('[\n')  # Start of JSON array
        is_first = True

        # Process input file
        with open(input_file, 'rb') as infile:
            parser = ijson.items(infile, 'item')

            for restaurant in parser:
                total_processed += 1
                if total_processed % 1000 == 0:
                    print(f"Processed {total_processed} restaurants...")

                if 'attributes' in restaurant:
                    attrs = restaurant['attributes']

                    # Clean WiFi
                    if 'WiFi' in attrs:
                        attrs['WiFi'] = clean_wifi(str(attrs['WiFi']))

                    # Clean DogsAllowed
                    if 'DogsAllowed' in attrs:
                        attrs['DogsAllowed'] = clean_boolean_with_none(attrs['DogsAllowed'])

                    # Clean BusinessParking
                    if 'BusinessParking' in attrs:
                        attrs['BusinessParking'] = clean_parking_dict(attrs['BusinessParking'])

                    # Clean BikeParking
                    if 'BikeParking' in attrs:
                        attrs['BikeParking'] = clean_boolean_with_none(attrs['BikeParking'])

                    # Clean Alcohol
                    if 'Alcohol' in attrs:
                        attrs['Alcohol'] = clean_alcohol(str(attrs['Alcohol']))

                    # Clean RestaurantsDelivery
                    if 'RestaurantsDelivery' in attrs:
                        attrs['RestaurantsDelivery'] = clean_boolean_with_none(attrs['RestaurantsDelivery'])

                    # Clean RestaurantsTakeOut
                    if 'RestaurantsTakeOut' in attrs:
                        attrs['RestaurantsTakeOut'] = clean_boolean_with_none(attrs['RestaurantsTakeOut'])

                    # Clean Caters
                    if 'Caters' in attrs:
                        attrs['Caters'] = clean_boolean_with_none(attrs['Caters'])

                    # Clean Smoking
                    if 'Smoking' in attrs:
                        attrs['Smoking'] = clean_smoking(str(attrs['Smoking']))

                # Write the restaurant to file
                if not is_first:
                    outfile.write(',\n')
                json.dump(restaurant, outfile, cls=DecimalEncoder, indent=2)
                is_first = False

        outfile.write('\n]')  # End of JSON array

    print(f"\nCleaning complete! Processed {total_processed} restaurants.")
    print(f"Cleaned data saved to {output_file}")


def main():
    try:
        input_file = "restaurants_with_attributes.json"
        output_file = "cleaned_restaurants.json"
        print(f"Starting to clean {input_file}")
        clean_data(input_file, output_file)

    except FileNotFoundError:
        print("Error: Input file not found!")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in input file!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
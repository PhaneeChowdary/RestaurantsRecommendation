from pymongo import MongoClient
import re
from collections import defaultdict
import pandas as pd


def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['restaurants_db']
    return db['Yelp']


def create_standardization_mapping():
    # Single words/incomplete names to remove
    invalid_cities = {
        'Blvd', 'Boulevard', 'Boyer', 'Bridge', 'Buck', 'Dade', 'Down', 'Doyles',
        'Earth', 'Elk', 'Flour', 'Garden', 'Gibbs', 'Granite', 'Had', 'Haver',
        'Hill', 'Jenkin', 'Jobs', 'Kenneth', 'Levit', 'Middle', 'Moores', 'New',
        'Plant', 'Potts', 'Quaker', 'Sumney', 'Sun', 'Terry', 'Tren', 'University',
        'View', 'Vincen', 'Virtual', 'West', 'Whites', 'Williams', 'Woods',
        'Wrights', 'Ybor', 'Wyndlake Condominium'
    }

    # City name variations that should be unified
    city_variations = {
        'Tampa': ['Tampa Florida', 'Tampa,Fl', 'Tampa Bay'],
        'Philadelphia': ['Phila', 'Philadephia'],
        'St. Petersburg': ['Saint Petersburg', 'St Petersburg', 'St Pete'],
        'St. Louis': ['Saint Louis', 'St Louis'],
        'Indianapolis': ['Inpolis', 'Indianopolis'],
        'Lansdale': ['Landsdale'],
        'New Square': ['Newsqaure', 'Newsquare'],
        'Spring Hill': ['Springhill'],
        'Woodbury Heights': ['Woodbury Hts'],
        'North Wales': ['N.wales'],
        'West Chester': ['W.chester'],
        'Mt. Laurel': ['Mt. Laurel Nj'],
        'Pinecrest West Park': ['Pinecrest. West. Park'],
        'St. Petersburg': ['St. Petersurg'],
        'Lutz': ['Lutz Fl', 'Lutz fl'],
        'Reno': ['Reno Nevada'],
        'Scott Air Force Base': ['Scott Afb'],
        'Temple Terrace': ['Temple Terr'],
        'Westmont': ['Westmont - Haddon Towsship'],
        'Southeast Edmonton': ['Southeast. Edmonton'],
        'South Tampa': ['Southwest. Tampa'],
        'Southwest Philadelphia': ['Southwest. Philadelphia'],
        'St. Louis': ['St. Louis Down'],
        "Town 'N' Country": ['& Country', 'And Country', "'n' Country", 'N Country'],
        'Clayton': ['​clayton']  # Added this line
    }

    # Regex patterns for standardization
    regex_patterns = {
        r'East\.\s+([A-Za-z]+)': r'East \1',
        r'West\.\s+([A-Za-z]+)': r'West \1',
        r'North\.\s+([A-Za-z]+)': r'North \1',
        r'South\.\s+([A-Za-z]+)': r'South \1',
        r'Saint\s+([A-Za-z]+)': r'St. \1',
        r'St\s+([A-Za-z]+)': r'St. \1',
        r'Mount\s+([A-Za-z]+)': r'Mt. \1',
        r'Mt\s+([A-Za-z]+)': r'Mt. \1',
        r'([A-Za-z\s]+),?\s*(?:PA|NJ|FL)$': r'\1',
        r'([A-Za-z]+)\s+Township': r'\1',
        r'([A-Za-z]+)\s+Twsp': r'\1',
        r'([A-Za-z]+)\s+Twp\.?': r'\1',
        r'([A-Za-z]+)\s+Borough': r'\1',
        r'([A-Za-z]+)\s+Boro': r'\1'
    }

    return regex_patterns, invalid_cities, city_variations


def standardize_city_name(city_name, regex_patterns, invalid_cities, city_variations):
    if not isinstance(city_name, str):
        return None

    # Remove leading/trailing whitespace
    city = city_name.strip()

    # Check if it's an invalid city
    if city in invalid_cities:
        return None

    # Check direct city variations first
    for standard_name, variations in city_variations.items():
        if city in variations:
            return standard_name

    # Apply regex patterns
    for pattern, replacement in regex_patterns.items():
        city = re.sub(pattern, replacement, city, flags=re.IGNORECASE)

    # Proper case (first letter of each word capitalized)
    city = ' '.join(word.capitalize() for word in city.split())

    return city.strip()


def update_database(collection, mapping):
    """Update city names in the database using the standardization mapping"""
    total_updates = 0

    print("\nUpdating database records...")
    for old_name, new_name in mapping.items():
        if old_name != new_name:
            if new_name is None:
                # If new_name is None, we want to remove these entries
                result = collection.delete_many({'city': old_name})
                if result.deleted_count > 0:
                    print(f"Removed {result.deleted_count} records with invalid city: '{old_name}'")
                    total_updates += result.deleted_count
            else:
                result = collection.update_many(
                    {'city': old_name},
                    {'$set': {'city': new_name}}
                )
                if result.modified_count > 0:
                    print(f"Updated {result.modified_count} records: '{old_name}' → '{new_name}'")
                    total_updates += result.modified_count

    print(f"\nTotal records affected: {total_updates}")
    return total_updates


def main():
    # Connect to MongoDB
    collection = connect_to_mongodb()

    # Get all unique cities from the database
    cities = collection.distinct('city')
    print(f"Found {len(cities)} unique cities in database")

    # Get standardization rules
    regex_patterns, invalid_cities, city_variations = create_standardization_mapping()

    # Create mapping of old names to new names
    standardization_mapping = {}
    for city in cities:
        standardized = standardize_city_name(city, regex_patterns, invalid_cities, city_variations)
        if standardized != city or standardized is None:
            standardization_mapping[city] = standardized

    # Print standardization report
    print("\nStandardization Report:")
    print("-" * 50)

    changes = pd.DataFrame([
        {'Original': old, 'Standardized': new if new is not None else 'REMOVE'}
        for old, new in standardization_mapping.items()
    ])

    if not changes.empty:
        print(f"\nFound {len(changes)} city names to standardize:")
        print(changes.to_string(index=False))

        # Confirm before updating
        response = input("\nDo you want to proceed with updating the database? (yes/no): ")
        if response.lower() == 'yes':
            total_updates = update_database(collection, standardization_mapping)
            print(f"\nStandardization complete. Updated {total_updates} records.")
        else:
            print("\nOperation cancelled. No changes made to the database.")
    else:
        print("No standardization needed. All city names are already consistent.")


if __name__ == "__main__":
    main()
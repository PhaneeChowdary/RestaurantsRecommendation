import json
from typing import Dict, Set, Tuple
from pathlib import Path

def load_restaurant_categories():
    """
    Load the predefined cuisine types and food establishments
    """
    cuisines = [
        "Afghan", "African", "American (New)", "American (Traditional)", "Arabic",
        "Argentine", "Armenian", "Asian Fusion", "Australian", "Austrian",
        "Bangladeshi", "Basque", "Belgian", "Brazilian", "British", "Burmese",
        "Cajun/Creole", "Calabrian", "Cambodian", "Canadian (New)", "Cantonese",
        "Caribbean", "Chinese", "Colombian", "Cuban", "Cucina campana", "Czech",
        "Dominican", "Eastern European", "Egyptian", "Ethiopian", "Filipino",
        "French", "Fuzhou", "Georgian", "German", "Greek", "Guamanian", "Hainan",
        "Haitian", "Hakka", "Hawaiian", "Himalayan/Nepalese", "Honduran",
        "Hong Kong Style Cafe", "Hungarian", "Iberian", "Indian", "Indonesian",
        "Irish", "Israeli", "Italian", "Japanese", "Korean", "Laotian",
        "Latin American", "Lebanese", "Malaysian", "Mediterranean", "Mexican",
        "Middle Eastern", "Modern European", "Mongolian", "Moroccan",
        "New Mexican Cuisine", "Nicaraguan", "Oriental", "Pakistani", "Pan Asian",
        "Persian/Iranian", "Peruvian", "Polish", "Portuguese", "Puerto Rican",
        "Roman", "Russian", "Salvadoran", "Sardinian", "Scandinavian", "Scottish",
        "Senegalese", "Serbo Croatian", "Shanghainese", "Singaporean", "Sicilian",
        "Somali", "Soul Food", "South African", "Southern", "Spanish", "Sri Lankan",
        "Syrian", "Szechuan", "Taiwanese", "Tex-Mex", "Thai", "Trinidadian",
        "Turkish", "Tuscan", "Ukrainian", "Uzbek", "Venezuelan", "Vietnamese"
    ]
    
    food_establishments = [
        "Acai Bowls", "Bagels", "Bakeries", "Barbeque", "Bars", "Beer", "Beer Bar",
        "Beer Gardens", "Beer Hall", "Beverage Store", "Bistros", "Breakfast & Brunch",
        "Breweries", "Brewpubs", "Bubble Tea", "Buffets", "Burgers", "Butcher",
        "Cafes", "Cafeteria", "Candy Stores", "Champagne Bars", "Cheese Shops",
        "Cheesesteaks", "Chicken Shop", "Chicken Wings", "Chocolatiers & Shops",
        "Cideries", "Cocktail Bars", "Coffee & Tea", "Coffee Roasteries",
        "Coffeeshops", "Comfort Food", "Convenience Stores", "Conveyor Belt Sushi",
        "Cooking Classes", "Cooking Schools", "Creperies", "Cupcakes", "Custom Cakes",
        "Delicatessen", "Delis", "Desserts", "Dim Sum", "Diners", "Dinner Theater",
        "Distilleries", "Donairs", "Donburi", "Donuts", "Dumplings", "Empanadas",
        "Falafel", "Farmers Market", "Fast Food", "Fish & Chips", "Food", "Food Banks",
        "Food Court", "Food Delivery Services", "Food Stands", "Food Tours",
        "Food Trucks", "Fondue", "Fruits & Veggies", "Gastropubs", "Gelato",
        "Grocery", "Halal", "Hot Dogs", "Hot Pot", "Ice Cream & Frozen Yogurt",
        "Imported Food", "International", "Izakaya", "Japanese Curry",
        "Juice Bars & Smoothies", "Kebab", "Kombucha", "Kosher", "Live/Raw Food",
        "Lounges", "Macarons", "Meat Shops", "Noodles", "Olive Oil", "Organic Stores",
        "Pancakes", "Pasta Shops", "Patisserie/Cake Shop", "Pita", "Pizza", "Poke",
        "Pop-Up Restaurants", "Popcorn Shops", "Poutineries", "Pretzels", "Pubs",
        "Ramen", "Restaurant Supplies", "Restaurants", "Salad", "Sandwiches",
        "Seafood", "Seafood Markets", "Shaved Ice", "Shaved Snow", "Smokehouse",
        "Soup", "Specialty Food", "Steakhouses", "Street Vendors", "Supper Clubs",
        "Sushi Bars", "Tapas Bars", "Tapas/Small Plates", "Tea Rooms", "Teppanyaki",
        "Themed Cafes", "Tiki Bars", "Tonkatsu", "Vegan", "Vegetarian", "Waffles",
        "Whiskey Bars", "Wine & Spirits", "Wine Bars", "Wine Tasting Room",
        "Wineries", "Wraps"
    ]
    
    # Convert to set for faster lookup and make all lowercase for case-insensitive matching
    return {c.lower() for c in cuisines}, {f.lower() for f in food_establishments}


def print_statistics(stats: Dict[str, int]) -> None:
    """
    Print processing statistics and file information.
    """
    print("\n=== Processing Statistics ===")
    print(f"Total records processed: {stats['total_processed']:,}")
    
    print(f"\nRecords by category:")
    print(f"1. Target Restaurants: {stats['target_restaurants']:,} "
          f"({stats['target_restaurants']/stats['total_processed']*100:.2f}%)")
    print(f"2. Other Businesses: {stats['other_businesses']:,} "
          f"({stats['other_businesses']/stats['total_processed']*100:.2f}%)")
    print(f"3. Businesses without categories: {stats['no_categories']:,} "
          f"({stats['no_categories']/stats['total_processed']*100:.2f}%)")
    
    print("\nOutput files created:")
    files = [
        ('target_restaurants.json', stats['target_restaurants']),
        ('other_businesses.json', stats['other_businesses'])
    ]
    
    for filename, count in files:
        try:
            size_mb = Path(filename).stat().st_size / (1024 * 1024)
            print(f"\n{filename}:")
            print(f"- Contains {count:,} records")
            print(f"- File size: {size_mb:.2f} MB")
        except FileNotFoundError:
            print(f"\nWarning: {filename} was not created properly")
    
    print("\nMatched Categories Found:")
    print("(First 50 categories shown, sorted alphabetically)")
    for category in sorted(stats['matched_categories'])[:50]:
        print(f"- {category}")
    if len(stats['matched_categories']) > 50:
        print(f"... and {len(stats['matched_categories']) - 50} more categories")


def is_target_restaurant(categories: str, cuisine_set: Set[str], establishment_set: Set[str]) -> Tuple[bool, Set[str]]:
    """
    Determine if a business matches our specific restaurant categories.
    
    Args:
        categories (str): Category string from business record
        cuisine_set (Set[str]): Set of cuisine types to match
        establishment_set (Set[str]): Set of food establishments to match
        
    Returns:
        Tuple[bool, Set[str]]: (is_match, matched_categories)
    """
    if not categories:
        return False, set()
    
    # Split categories, clean them, and convert to lowercase for case-insensitive matching
    business_categories = {cat.strip().lower() for cat in categories.split(',')}
    
    # Find matching categories
    matched_cuisines = business_categories & cuisine_set
    matched_establishments = business_categories & establishment_set
    all_matches = matched_cuisines | matched_establishments
    
    return bool(all_matches), all_matches

def split_specific_restaurants(input_file: str) -> Dict[str, int]:
    """
    Split business records based on specific restaurant categories.
    """
    target_restaurant_file = 'target_restaurants.json'
    other_file = 'other_businesses.json'
    log_file = 'classification_log.txt'  # New log file
    
    cuisine_set, establishment_set = load_restaurant_categories()
    
    stats = {
        'total_processed': 0,
        'target_restaurants': 0,
        'other_businesses': 0,
        'no_categories': 0,
        'matched_categories': set()
    }
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(target_restaurant_file, 'w', encoding='utf-8') as rest_out, \
         open(other_file, 'w', encoding='utf-8') as other_out, \
         open(log_file, 'w', encoding='utf-8') as log:  # Open log file
        
        rest_out.write('[\n')
        other_out.write('[\n')
        
        first_records = {'rest': True, 'other': True}
        
        for line in infile:
            stats['total_processed'] += 1
            
            try:
                business = json.loads(line.strip())
                
                def write_record(file, record_type):
                    if not first_records[record_type]:
                        file.write(',\n')
                    first_records[record_type] = False
                    json.dump(business, file, indent=2)
                
                categories = business.get('categories', '')
                
                # Log the business being processed
                log.write(f"\nProcessing business: {business['name']}\n")
                log.write(f"Categories: {categories}\n")
                
                if not categories:
                    stats['no_categories'] += 1
                    write_record(other_out, 'other')
                    log.write("Result: No categories found\n")
                    continue
                
                is_match, matched_cats = is_target_restaurant(categories, cuisine_set, establishment_set)
                
                if is_match:
                    stats['target_restaurants'] += 1
                    write_record(rest_out, 'rest')
                    stats['matched_categories'].update(matched_cats)
                    log.write(f"Result: MATCH. Matched categories: {matched_cats}\n")
                else:
                    stats['other_businesses'] += 1
                    write_record(other_out, 'other')
                    log.write("Result: NO MATCH\n")
                
            except json.JSONDecodeError:
                log.write("Error: Failed to parse JSON\n")
                continue
            
            if stats['total_processed'] % 10000 == 0:
                print(f"Processed {stats['total_processed']:,} records...")
        
        rest_out.write('\n]')
        other_out.write('\n]')
    
    return stats

def main():
    """
    Main function to split restaurant records based on specific categories.
    """
    try:
        input_file = 'yelp_academic_dataset_business.json'
        print(f"Starting to process {input_file}...")
        print("A detailed log will be created in 'classification_log.txt'")
        
        stats = split_specific_restaurants(input_file)
        
        print_statistics(stats)
        
        print("\nProcessing complete! Check classification_log.txt for detailed matching information.")
        
    except FileNotFoundError:
        print(f"Error: Could not find the input file '{input_file}'")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

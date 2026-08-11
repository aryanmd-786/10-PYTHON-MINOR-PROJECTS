

import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1"

def get_random_meal():
    """Fetch a random meal from the API."""
    try:
        url = f"{BASE_URL}/random.php"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        meals = data.get("meals", [])
        if meals:
            return meals[0]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None

def search_meal(query):
    """Search for a meal by name."""
    try:
        url = f"{BASE_URL}/search.php?s={query.strip()}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        meals = data.get("meals", [])
        return meals if meals else None
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None

def extract_ingredients(meal):
    """
    Extract all ingredients and their measures from the meal dict.
    Returns a list of tuples: [(ingredient, measure), ...]
    """
    ingredients = []
    for i in range(1, 21):  # API supports up to 20 ingredients
        ingredient_key = f"strIngredient{i}"
        measure_key = f"strMeasure{i}"
        ingredient = meal.get(ingredient_key, "").strip()
        measure = meal.get(measure_key, "").strip()
        if ingredient and ingredient.lower() != " ":
            ingredients.append((ingredient, measure))
    return ingredients

def display_meal(meal):
    """Print the meal details beautifully."""
    if not meal:
        print("❌ Meal not found.")
        return

    print("\n" + "🍽️ " + "=" * 60)
    print(f"📛 Name       : {meal.get('strMeal', 'Unknown')}")
    print(f"📂 Category   : {meal.get('strCategory', 'N/A')}")
    print(f"🌍 Region     : {meal.get('strArea', 'N/A')}")
    print(f"🖼️ Image Link : {meal.get('strMealThumb', 'N/A')}")
    print("-" * 60)

    # Ingredients
    ingredients = extract_ingredients(meal)
    if ingredients:
        print("🛒 Ingredients:")
        for ing, measure in ingredients:
            print(f"   • {ing} : {measure if measure else 'As needed'}")
    else:
        print("🛒 Ingredients: Not available")

    print("-" * 60)
    print("📖 Instructions:")
    instructions = meal.get('strInstructions', 'Instructions not available.')
    # Split instructions into lines for better readability
    for line in instructions.split('. '):
        if line.strip():
            print(f"   ➤ {line.strip()}.")
    print("=" * 60 + "\n")

def main():
    print("🍳 === Recipe Finder & Random Meal Generator === 🍳")

    while True:
        print("\n" + "-" * 40)
        print("1. 🎲 Get a random recipe")
        print("2. 🔍 Search recipe by name")
        print("3. 🚪 Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            print("⏳ Fetching a random delicious meal...")
            meal = get_random_meal()
            if meal:
                display_meal(meal)
            else:
                print("❌ Could not fetch a random meal. Please try again.")

        elif choice == '2':
            query = input("Enter dish name (e.g., Pasta, Biryani, Cake): ").strip()
            if not query:
                print("❌ Dish name cannot be empty.")
                continue

            print(f"⏳ Searching for '{query}'...")
            meals = search_meal(query)
            if meals:
                print(f"✅ Found {len(meals)} result(s).")
                for i, meal in enumerate(meals, start=1):
                    print(f"\n--- Result #{i} ---")
                    display_meal(meal)
            else:
                print(f"❌ No recipes found for '{query}'. Please try another name.")

        elif choice == '3':
            print("👋 Thanks for using the Recipe Finder! Happy cooking! 🍜")
            break

        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
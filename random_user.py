

import requests
import json
from datetime import datetime

BASE_URL = "https://randomuser.me/api/"

def fetch_random_users(count=1, nationality=None):
    """
    Fetch random users from API.
    count: number of users (1-50)
    nationality: ISO country code (e.g., 'IN', 'US', 'GB')
    Returns list of user dictionaries or None on error.
    """
    params = {
        "results": count,
        "inc": "name,email,location,phone,picture,login,nat",  # only needed fields
        "noinfo": True
    }
    if nationality:
        params["nat"] = nationality.upper()
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None

def display_user(user, index=None):
    """Print a single user's details in a nice format."""
    name = user["name"]
    full_name = f"{name['title']}. {name['first']} {name['last']}"
    email = user["email"]
    location = user["location"]
    address = f"{location['street']['number']}, {location['street']['name']}, {location['city']}, {location['state']} - {location['postcode']}"
    country = location["country"]
    phone = user["phone"]
    picture = user["picture"]["large"]
    nat = user["nat"]
    
    prefix = f"User #{index+1}" if index is not None else "User"
    print("\n" + "=" * 60)
    print(f"{prefix} 👤")
    print("=" * 60)
    print(f"Name    : {full_name}")
    print(f"Email   : {email}")
    print(f"Phone   : {phone}")
    print(f"Address : {address}")
    print(f"Country : {country} ({nat})")
    print(f"Picture : {picture}")   # URL of image (can open in browser)
    print("=" * 60)

def save_users(users, filename="users.txt"):
    """Save all user details to a text file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n")
        for i, user in enumerate(users, start=1):
            name = user["name"]
            full_name = f"{name['title']}. {name['first']} {name['last']}"
            f.write(f"User #{i}: {full_name}\n")
            f.write(f"Email: {user['email']}\n")
            f.write(f"Phone: {user['phone']}\n")
            loc = user["location"]
            f.write(f"Address: {loc['street']['number']} {loc['street']['name']}, {loc['city']}, {loc['state']} - {loc['postcode']}, {loc['country']}\n")
            f.write(f"Picture: {user['picture']['large']}\n")
            f.write("-" * 60 + "\n")
    print(f"✅ Users saved to '{filename}'")

def main():
    print("👤 === Random User Profile Generator === 👤")
    
    while True:
        print("\n" + "-" * 40)
        print("1. Generate random users")
        print("2. Generate with nationality filter")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            try:
                count = int(input("How many users? (1-50): ") or "1")
                if count < 1 or count > 50:
                    print("❌ Please enter between 1 and 50.")
                    continue
            except ValueError:
                print("❌ Invalid number.")
                continue
            
            users = fetch_random_users(count)
            if users:
                for i, user in enumerate(users):
                    display_user(user, i)
                # Ask to save
                save = input("Save these users to file? (y/n): ").strip().lower()
                if save == 'y':
                    save_users(users)
            else:
                print("❌ Could not fetch users. Please try again.")

        elif choice == '2':
            nat = input("Enter country code (e.g., IN, US, GB, AU, CA): ").strip().upper()
            if not nat:
                print("❌ Country code cannot be empty.")
                continue
            try:
                count = int(input("How many users? (1-50): ") or "1")
                if count < 1 or count > 50:
                    print("❌ Please enter between 1 and 50.")
                    continue
            except ValueError:
                print("❌ Invalid number.")
                continue
            
            users = fetch_random_users(count, nat)
            if users:
                for i, user in enumerate(users):
                    display_user(user, i)
                save = input("Save these users to file? (y/n): ").strip().lower()
                if save == 'y':
                    save_users(users)
            else:
                print(f"❌ No users found for nationality '{nat}'. Try another code.")

        elif choice == '3':
            print("👋 Goodbye! Thanks for using the generator.")
            break

        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
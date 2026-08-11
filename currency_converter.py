

import requests

# Base URLs for the fawazahmed0 API
CDN_BASE = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest"

# Cache for currencies list and exchange rates
CURRENCY_CACHE = None
RATES_CACHE = {}   # { base_currency: { target: rate, ... } }

def get_currency_list():
    """Fetch list of all supported currencies."""
    global CURRENCY_CACHE
    if CURRENCY_CACHE:
        return CURRENCY_CACHE

    try:
        url = f"{CDN_BASE}/currencies.json"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        # data is like: { "usd": "United States Dollar", "inr": "Indian Rupee", ... }
        # Convert keys to uppercase for consistency
        CURRENCY_CACHE = { k.upper(): v for k, v in data.items() }
        return CURRENCY_CACHE
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching currency list: {e}")
        return None

def get_rates(base_currency):
    """
    Fetch exchange rates for a given base currency (e.g., 'USD')
    Returns dict of { target: rate } or None
    """
    if base_currency in RATES_CACHE:
        return RATES_CACHE[base_currency]

    try:
        url = f"{CDN_BASE}/currencies/{base_currency.lower()}.json"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        # data is like: { "date": "...", "usd": { "inr": 83.5, ... } }
        rates = data.get(base_currency.lower(), {})
        if not rates:
            print(f"❌ No rates found for {base_currency}")
            return None
        # Convert keys to uppercase
        rates_upper = { k.upper(): v for k, v in rates.items() }
        RATES_CACHE[base_currency] = rates_upper
        return rates_upper
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching rates for {base_currency}: {e}")
        return None

def convert_currency(amount, from_curr, to_curr):
    """
    Convert amount from one currency to another using cross rates.
    """
    from_curr = from_curr.upper()
    to_curr = to_curr.upper()

    # Agar dono same hain toh directly return
    if from_curr == to_curr:
        return amount, 1.0

    # Pehle from_curr ki rates fetch karein
    rates = get_rates(from_curr)
    if not rates:
        return None

    if to_curr not in rates:
        print(f"❌ Target currency '{to_curr}' not available for {from_curr}")
        return None

    rate = rates[to_curr]
    converted = amount * rate
    return converted, rate

def display_currencies():
    """Show all currencies nicely."""
    currencies = get_currency_list()
    if not currencies:
        print("❌ Currency list fetch nahi ho paayi.")
        return

    print(f"\n📋 Supported Currencies (Total: {len(currencies)}):")
    print("-" * 60)
    sorted_items = sorted(currencies.items())
    for i, (code, name) in enumerate(sorted_items, start=1):
        print(f"{i:3}. {code:5} - {name}")
    print("-" * 60)

def main():
    print("💱 === Real-Time Currency Converter (Stable) === 💱")

    # Pehle currency list fetch karein
    currencies = get_currency_list()
    if not currencies:
        print("⚠️ Currency list fetch nahi ho paayi. Internet check karein ya baad mein try karein.")
        return

    while True:
        print("\n" + "=" * 50)
        print("1. 🔄 Convert Currency")
        print("2. 📋 Show all supported currencies")
        print("3. 🚪 Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            from_curr = input("From currency (e.g., USD, INR, EUR): ").strip().upper()
            to_curr = input("To currency (e.g., INR, GBP, JPY): ").strip().upper()

            # Validate
            if from_curr not in currencies:
                print(f"❌ '{from_curr}' supported nahi hai. Please check spelling.")
                continue
            if to_curr not in currencies:
                print(f"❌ '{to_curr}' supported nahi hai. Please check spelling.")
                continue

            try:
                amount = float(input(f"Enter amount in {from_curr}: "))
                if amount < 0:
                    print("❌ Amount negative nahi ho sakta.")
                    continue
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")
                continue

            result = convert_currency(amount, from_curr, to_curr)
            if result:
                converted_amount, rate = result
                print("\n" + "=" * 50)
                print(f"💵 {amount:.2f} {from_curr}  =  {converted_amount:.2f} {to_curr}")
                print(f"📊 Exchange Rate: 1 {from_curr} = {rate:.4f} {to_curr}")
                print("=" * 50)

        elif choice == '2':
            display_currencies()

        elif choice == '3':
            print("👋 Shukriya! Currency Converter band kar rahe hain. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
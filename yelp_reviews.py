import requests
from urllib.parse import quote

# Your Yelp API Key
API_KEY = "your_yelp_api_key"

HEADERS = {"Authorization": f"Bearer {API_KEY}"}

SEARCH_URL = "https://api.yelp.com/v3/businesses/search"
REVIEWS_URL = "https://api.yelp.com/v3/businesses/{}/reviews"

def search_restaurant(name, location):
    """Searches for a restaurant on Yelp and shows its information."""
    params = {
        "term": name,
        "location": location,
        "limit": 1 
    }
    
    response = requests.get(SEARCH_URL, headers=HEADERS, params=params)
    data = response.json()

    if "businesses" not in data or len(data["businesses"]) == 0:
        print("❌ No restaurant found.")
        return None

    business = data["businesses"][0]
    business_id = business["id"]
    name = business["name"]
    rating = business.get("rating", "N/A")
    address = ", ".join(business["location"]["display_address"])
    image_url = business.get("image_url", "Not available")
    yelp_url = business["url"]
    review_count = business.get("review_count", 0)

    # Try to get the menu URL if available
    menu_url = business.get("attributes", {}).get("menu_url", "Not available")

    print(f"\n✅ Restaurant found: {name}")
    print(f"📍 Address: {address}")
    print(f"⭐ Rating: {rating} ({review_count} reviews)")
    print(f"🖼️ Image: {image_url}")
    print(f"🔗 More info: {yelp_url}")
    print(f"📜 Menu: {menu_url}\n")
    
    return business_id, yelp_url

def get_reviews(business_id, yelp_url):
    """Shows the reviews of a restaurant and provides a direct link to the reviews on Yelp."""
    print(f"🔍 Business ID (before formatting): {business_id!r}")  # For debugging

    # Encode business_id to avoid errors in the URL
    safe_business_id = quote(business_id.strip(), safe="")
    url = REVIEWS_URL.format(safe_business_id)

    response = requests.get(url, headers=HEADERS)
    reviews_data = response.json()

    print("🔍 Yelp API response (debugging):")
    print(reviews_data)

    if "reviews" not in reviews_data:
        print("❌ No reviews found in the API.")
        print(f"🔗 See more reviews on Yelp: {yelp_url}#reviews\n")
        return

    print("📢 Reviews found:\n")
    for review in reviews_data["reviews"]:
        print(f"📝 User: {review['user']['name']}")
        print(f"⭐ Rating: {review['rating']} stars")
        print(f"💬 Comment: {review['text']}\n")
        print("="*40)

    print(f"🔗 See more reviews on Yelp: {yelp_url}#reviews\n")

if __name__ == "__main__":
    restaurant = input("🔍 Restaurant name: ")
    location = input("📍 Location (city/address): ")

    result = search_restaurant(restaurant, location)

    if result:
        business_id, yelp_url = result
        get_reviews(business_id, yelp_url)

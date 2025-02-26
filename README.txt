Yelp Reviews Scraper
This Python script allows you to search for restaurants on Yelp and fetch their reviews.

Requirements
To run this script, you need to have a Yelp API key. If you don't have one, you can obtain it by following these steps:

Visit the Yelp Developers website.
Sign up and create a new app to get your API Key.
Replace the API_KEY variable in the code with your own Yelp API Key.
Installation
Clone or download the repository.
Install the necessary Python libraries by running the following command in your terminal:
nginx
Copiar
Editar
pip install requests
Running the Program
To run the script, follow these steps:

Open your terminal or command prompt.

Navigate to the directory where the script is located.

Run the following command:

nginx
Copiar
Editar
python yelp_reviews.py
The program will prompt you to enter the name of the restaurant (e.g., "Starbucks") and the location (e.g., "Miami").

The script will then show the restaurant information, including the Yelp rating, address, image, menu (if available), and reviews.

Example:
yaml
Copiar
Editar
🔍 Restaurant name: Starbucks
📍 Location (city/address): Miami

✅ Restaurant found: Starbucks
📍 Address: 1234 Main St, Miami, FL
⭐ Rating: 4.5 (200 reviews)
🖼️ Image: https://example.com/starbucks.jpg
🔗 More info: https://www.yelp.com/biz/starbucks-miami
📜 Menu: Not available

🔍 Reviews found:

📝 User: John Doe
⭐ Rating: 5 stars
💬 Comment: Great place for coffee!

========================================
🔗 See more reviews on Yelp: https://www.yelp.com/biz/starbucks-miami#reviews
Troubleshooting
Make sure to replace the API key in the script with your own Yelp API key.
Ensure your Python version is 3.x or higher.
If the script doesn't show any results, try changing the search term or location.
For any issues or suggestions, feel free to open an issue on the repository!
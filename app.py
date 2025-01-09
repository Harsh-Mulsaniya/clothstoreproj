from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import re
from model import recommend_item

# Dictionary mapping clothing classes to image filenames
class_images = {
    'Dresses': 'dresses.jpg',
    'Pants': 'pants.jpg',
    'Blouses': 'blouses.jpg',
    'Knits': 'knits.jpg',
    'Intimates': 'intimates.jpg',
    'Outerwear': 'outerwear.jpg',
    'Lounge': 'lounge.jpg',
    'Sweaters': 'sweaters.jpg',
    'Skirts': 'skirts.jpg',
    'Fine gauge': 'fine_gauge.jpg',
    'Sleep': 'sleep.jpg',
    'Jackets': 'jackets.jpg',
    'Swim': 'swim.jpg',
    'Trend': 'trend.jpg',
    'Jeans': 'jeans.jpg',
    'Shorts': 'shorts.jpg',
    'Legwear': 'legwear.jpg',
    'Layering': 'layering.jpg',
    'Casual bottoms': 'casual_bottoms.jpg',
    'Chemises': 'chemises.jpg'
}

app = Flask(__name__)

# Load the clothing dataset
clothing_data = pd.read_csv('data/clothing_data.csv')

def search_items(keyword):
    # Compile the regex pattern to make the search case-insensitive
    pattern = re.compile(keyword, re.IGNORECASE)

    # Filter the DataFrame using the keyword on both ClassName and cloth_Description columns
    matches = clothing_data[
        clothing_data['ClassName'].str.contains(pattern, na=False) |
        clothing_data['cloth_Description'].str.contains(pattern, na=False)
    ].copy()  # Use .copy() to avoid SettingWithCopyWarning

    # Assign image filenames based on 'ClassName'
    matches['Image'] = matches['ClassName'].apply(lambda x: class_images.get(x, 'default.jpg'))

    # Provide a message if no matches are found (optional: log or show to user)
    if matches.empty:
        print(f"No items found for keyword: {keyword}")

    return matches

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = search_items(keyword)
        return render_template('search.html', keyword=keyword, results=results)
    return redirect(url_for('index'))

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item(item_id):
    try:
        item = clothing_data.iloc[item_id]
    except IndexError:
        return f"Item with ID {item_id} not found.", 404

    recommended = recommend_item(item.get('review_text', ''))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        override = request.form.get('override', recommended)  # Use override or model recommendation

        # Display the review (extend this to save in DB/CSV as needed)
        review = {"Title": title, "Description": description, "Recommended": override}
        return render_template('item.html', item=item, review=review, recommended=recommended, class_images=class_images)

    return render_template('item.html', item=item, recommended=recommended, class_images=class_images)

if __name__ == '__main__':
    app.run(debug=True)

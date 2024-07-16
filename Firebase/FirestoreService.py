import firebase_admin
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import ArrayUnion

from Scraping import scraper

# initialize firestore
cred = credentials.Certificate("mobilert-9271f-firebase-adminsdk-981fn-361436fc97.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# initialize flask
app = Flask(__name__)

def add_query(query):
    queries_ref = db.collection('queries')
    listings = scraper.scrape(query)
    data = {'listings': listings}
    result = queries_ref.document(query).set(data)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    jsondata = request.json
    email = jsondata['email']
    query = jsondata['query']
    target_price = jsondata['price']

    user_ref = db.collection('users').document(email)

    # Update existing document with new subscription
    subscription = {
        "query": query,
        "targetPrice": target_price
    }

    # Check if the user document exists
    user_doc = user_ref.get()

    if user_doc.exists:
        update_result = user_ref.update({
            "subscriptions": ArrayUnion([subscription])
        })
        print(f"Updated document at: {update_result.update_time}")
    else:
        # Create new document with initial subscription
        user_data = {
            "subscriptions": [subscription]  # Initial subscription
        }
        create_result = user_ref.set(user_data, merge=True)
        print(f"Created document at: {create_result.update_time}")

    return "Success", 200

if __name__ == '__main__':
    app.run(debug=True)
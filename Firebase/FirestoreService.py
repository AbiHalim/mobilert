import firebase_admin
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import ArrayUnion

from Scraping import scraper

# initialize firestore
cred = credentials.Certificate("mobilert-9271f-firebase-adminsdk-981fn-361436fc97.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# initialize flask
app = Flask(__name__)
CORS(app)

def add_query(query):
    queries_ref = db.collection('queries')
    listings = scraper.scrape(query)
    data = {'listings': listings}
    nquery = query.lower().replace(" ", "")  # normalized query, removes caps and whitespace
    result = queries_ref.document(nquery).set(data)
    print(f"Succesfully added query {query} to database")

@app.route('/subscribe', methods=['POST'])
def subscribe():
    jsondata = request.json
    email = jsondata['email']
    query = jsondata['query']
    target_price = jsondata['price']

    nquery = query.lower().replace(" ", "")  # normalized query, removes caps and whitespace

    user_ref = db.collection('users').document(email)

    subscription = {
        "query": nquery,
        "targetPrice": target_price
    }

    # check if the user document exists
    user_doc = user_ref.get()

    if user_doc.exists:
        update_result = user_ref.update({
            "subscriptions": ArrayUnion([subscription])
        })
        print(f"Updated user {email} at: {update_result.update_time}")
    else:
        # create new document with initial subscription
        user_data = {
            "subscriptions": [subscription]
        }
        create_result = user_ref.set(user_data, merge=True)
        print(f"Created new user {email} at: {create_result.update_time}")

    # adding query to query list
    query_ref = db.collection('queries').document(nquery)

    # check if the query exists in the queries database
    query_doc = query_ref.get()

    if not query_doc.exists:
        add_query(query)

    return "Success", 200

if __name__ == '__main__':
    app.run(port=1738, debug=True)
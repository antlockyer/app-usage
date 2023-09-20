from flask import Flask, render_template
from pymongo import MongoClient
from bson.son import SON

app = Flask(__name__)

# MongoDB connection settings
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'focused_app_logs'
MONGO_COLLECTION = 'app_usage'

# Initialize MongoDB client and collection
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

@app.route('/')
def display_logs():
    # Aggregate data to calculate total time spent per application
    pipeline = [
        {
            '$group': {
                '_id': '$application',
                'total_time_spent': {'$sum': '$time_spent'},
                'website': {'$first': '$website'}
            }
        },
        {
            '$sort': SON([('total_time_spent', -1)])
        }
    ]

    logs = list(collection.aggregate(pipeline))

    # Render the HTML template and pass the data
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)

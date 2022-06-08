from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import pickle
import numpy as np
import json
from datetime import datetime
app = Flask(__name__)
api = Api(app)

# Create parser for the payload data
parser = reqparse.RequestParser()
parser.add_argument('data')


# Define how the api will respond to the post requests
class TaxiPrediction(Resource):
    def get(self):
        longitude = (request.args.get('longitude'))
        latitude = (request.args.get('latitude'))
        distance = (request.args.get("https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248327dfbd785f541cfa1c6314bcbeb3cd3&start=8.681495,49.41461&end=8.687872,49.420318"))
        requestTime = datetime.now().time()
        #request time to seconds
        requestTimeSeconds = requestTime.hour * 3600 + requestTime.minute * 60 + requestTime.second
        travel_time = model.predict([[longitude, latitude, requestTimeSeconds]])
        return {'longitude': longitude, 'latitude': latitude, 'travel_time': travel_time}

    def post(self):
        args = parser.parse_args()
        X = np.array(json.loads(args['data']))
        prediction = model.predict(X)
        return jsonify(prediction.tolist())


# asasdasd
api.add_resource(TaxiPrediction, '/taxi')

if __name__ == '__main__':
    # Load model
    with open('model.pickle', 'rb') as f:
        model = pickle.load(f)

    app.run(debug=True)

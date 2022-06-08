from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import pickle
import numpy as np
import json
import requests
from zones import latlonToZoneId
from datetime import datetime
app = Flask(__name__)
api = Api(app)

# Create parser for the payload data
parser = reqparse.RequestParser()
parser.add_argument('data')


# Define how the api will respond to the post requests
class TaxiPrediction(Resource):
    def get(self):
        fromLon = (request.args.get('fromLon'))
        fromLat = (request.args.get('fromLat'))
        toLon = (request.args.get('toLon'))
        toLat = (request.args.get('toLat'))

        distance = (request.args.get("https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248327dfbd785f541cfa1c6314bcbeb3cd3&start=8.681495,49.41461&end=8.687872,49.420318"))
        import requests

        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }
        call = requests.get('https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248327dfbd785f541cfa1c6314bcbeb3cd3&start={0},{1}&end={2},{3}'.format(fromLon,fromLat,toLon,toLat), headers=headers)
        #print(call.status_code, call.reason)
        #print(call.text)
        response = json.loads(call.text)
        features = response['features'][0]
        print(features)
        #summary = features['summary']
        #distanceMeters = summary["distance"]
        #distanceMiles = distanceMeters*0.0006213712
        requestTime = datetime.now().time()
        #request time to seconds
        requestTimeSeconds = requestTime.hour * 3600 + requestTime.minute * 60 + requestTime.second
        #travel_time = model.predict([[requestTime, distanceMiles,latlonToZoneId(fromLon,fromLat), latlonToZoneId(toLon,toLat)]])
        return 50

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

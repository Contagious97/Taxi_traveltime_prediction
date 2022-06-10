from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import shapefile as shp
from shapely.geometry import Polygon, Point
import pickle
import requests
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
        fromLon = (request.args.get('fromLon', type=float))
        fromLat = (request.args.get('fromLat', type=float))
        toLon = (request.args.get('toLon', type=float))
        toLat = (request.args.get('toLat', type=float))
        pickupTime = (request.args.get('requesttime', type=str))

        pickupTimeString = pickupTime.split(":")
        pickupTimeHours = int(pickupTimeString[0])
        pickupTimeMinutes = int(pickupTimeString[1])
        pickupTime = pickupTimeHours * 3600 + pickupTimeMinutes * 60
        pickupID = latlonToZoneId(fromLon, fromLat)
        dropOffID = latlonToZoneId(toLon, toLat)

        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }
        call = requests.get(
            'https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248327dfbd785f541cfa1c6314bcbeb3cd3&start={0},{1}&end={2},{3}'.format(
                fromLon, fromLat, toLon, toLat), headers=headers)

        response = json.loads(call.text)
        features = response['features'][0]
        summary = features['properties']['summary']
        distanceMeters = summary["distance"]
        distanceMiles = distanceMeters * 0.0006213712
        X = np.array([[pickupTime, float(distanceMiles), pickupID, dropOffID]])
        travel_time = model.predict(X)
        print(travel_time)
        return {"Travel time in seconds: ": travel_time[0]}

    def post(self):
        args = parser.parse_args()
        X = np.array(json.loads(args['data']))
        prediction = model.predict(X)
        return jsonify(prediction.tolist())


# asasdasd
api.add_resource(TaxiPrediction, '/taxi')


def latlonToZoneId(lon, lat):
    x, y = lon, lat
    __sf = shp.Reader("data/zones/taxi_zones.zip")

    point = Point(x, y)

    # find the zone that contains the point
    for sr in __sf.shapeRecords():
        sr: shp.ShapeRecord
        shape: shp.Shape = sr.shape
        polygon = Polygon(shape.points)
        if polygon.contains(point):
            return sr.record[0]

    return None


if __name__ == '__main__':
    # Load model
    with open('model.pickle', 'rb') as f:
        model = pickle.load(f)

    app.run(debug=True)

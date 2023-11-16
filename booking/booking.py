from flask import Flask, render_template, request, jsonify, make_response
import requests
import json

import grpc
import showtime_pb2
import showtime_pb2_grpc

PORT = 3201
HOST = '127.0.0.1'
showtimePort = 3202

app = Flask(__name__)

with open('{}/data/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


def run():
    with grpc.insecure_channel(f"{HOST}:{showtimePort}") as channel:
        showTimeStub = showtime_pb2_grpc.ShowTimesStub(channel)

        def get_schedule_by_date(strDate):
            showTimeDate = showtime_pb2.Date(date=strDate)
            movie = showTimeStub.GetScheduleByDate(showTimeDate)

            return "movie"

        get_schedule_by_date("20151130")


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_json():
    return make_response(jsonify(bookings), 200)


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid: str):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking), 200)
            return res
    return make_response(jsonify({"error": "User ID not found"}), 400)


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid: str):
    req = request.get_json()
    movieid = str(req["movieid"])
    moviedate = str(req["date"])

    try:
        showtime = requests.get(f"http://{HOST}:{showtimePort}/showmovies/{moviedate}")
    except Exception as e:
        # print(e)
        return make_response(jsonify({"error": f'error when requesting showtime'}), 400)

    if showtime.status_code != 200 or movieid not in showtime.json()["movies"]:
        return make_response(jsonify({"error": "no showtime found for this booking"}), 400)

    booking = None
    for el in bookings:
        if str(el["userid"]) == str(userid):
            booking = el
            break

    if booking is None:
        return make_response(jsonify({"error": "User ID not found"}), 400)

    for date in booking["dates"]:
        if str(date["date"]) == moviedate:
            date["movies"].append(movieid)
            return make_response(jsonify({"message": "booking added"}), 200)

    booking["dates"].append({"date": moviedate, "movies": [movieid]})
    return make_response(jsonify({"message": "booking added"}), 200)


if __name__ == "__main__":
    # run()
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)

from flask import Flask, render_template, request, jsonify, make_response
import requests
import json

import grpc
import showtime_pb2
import showtime_pb2_grpc

from concurrent import futures
import booking_pb2
import booking_pb2_grpc

PORT = 3201
HOST = '[::]'
showTimeHOST = "localhost"
showtimePort = 3202

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
        super().__init__() # useless as the super class have no constructor
    
    def GetAllBookings(self, request, context):
        for book in self.db:
            yield booking_pb2.Book(userid = book.userid, dates = [booking_pb2.BookingDate(date=daty.dates, movies = daty.movies) for daty in book.dates])
    
    def GetBookingByUser(self, request, context):
        for book in self.db:
            if str(book["userid"]) == str(request.userid):
                return booking_pb2.Book(userid = book.userid, dates = [booking_pb2.BookingDate(date=daty.dates, movies = daty.movies) for daty in book.dates])
        return booking_pb2.Book(userid = "-1", dates = [])

    def AddBookingByUser(self, request, context):
        movieid = request.movieid
        moviedate = request.date

        try:
            with grpc.insecure_channel(f"{showTimeHOST}:{showtimePort}") as channel:
                showTimeStub = showtime_pb2_grpc.ShowTimesStub(channel)
                showTimeDate = showtime_pb2.Date(date = moviedate)
                showtime = showTimeStub.GetScheduleByDate(showTimeDate)
        except Exception as e:
            return booking_pb2.Book(userid = "-1", dates = [])

        if showtime.date == -1 or movieid not in showtime.movies:
            return booking_pb2.Book(userid = "-1", dates = [])

        booking = None
        for el in bookings:
            if str(el["userid"]) == str(userid):
                booking = el
                break

        if booking is None:
            booking = {
                "userid": userid,
                "dates": [
                ]
            }
        else:
            for date in booking["dates"]:
                if str(date["date"]) == moviedate:
                    date["movies"].append(movieid)
                    return booking_pb2.Book(userid = userid, dates =  [booking_pb2.BookingDate(date=daty.dates, movies = daty.movies) for daty in booking.dates])

        

        booking["dates"].append({"date": moviedate, "movies": [movieid]})
        return booking_pb2.Book(userid = userid, dates = [booking_pb2.BookingDate(date=daty.dates, movies = daty.movies) for daty in booking.dates])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port(f"{HOST}:{PORT}")
    print(f"Server running on {HOST}:{PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

# app = Flask(__name__)

# with open('{}/data/bookings.json'.format("."), "r") as jsf:
#     bookings = json.load(jsf)["bookings"]


# def get_all_times():
#     times = []
#     showTimeEmpty = showtime_pb2.Empty()
#     allTime = showTimeStub.GetAllTimes(showTimeEmpty)
#     for time in allTime:
#         times += [time]
            


# @app.route("/", methods=['GET'])
# def home():
#     return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


# @app.route("/bookings", methods=['GET'])
# def get_json():
#     return make_response(jsonify(bookings), 200)


# @app.route("/bookings/<userid>", methods=['GET'])
# def get_booking_for_user(userid: str):
#     for booking in bookings:
#         if str(booking["userid"]) == str(userid):
#             res = make_response(jsonify(booking), 200)
#             return res
#     return make_response(jsonify({"error": "User ID not found"}), 400)


# @app.route("/bookings/<userid>", methods=['POST'])
# def add_booking_byuser(userid: str):
#     req = request.get_json()
#     movieid = str(req["movieid"])
#     moviedate = str(req["date"])
    

#     try:
#         with grpc.insecure_channel(f"{showTimeHOST}:{showtimePort}") as channel:
#             showTimeStub = showtime_pb2_grpc.ShowTimesStub(channel)
#             showTimeDate = showtime_pb2.Date(date = moviedate)
#             showtime = showTimeStub.GetScheduleByDate(showTimeDate)
#     except Exception as e:
#         return make_response(jsonify({"error": f'error when requesting showtime'}), 400)

#     if showtime.date == -1 or movieid not in showtime.movies:
#         return make_response(jsonify({"error": "no showtime found for this booking"}), 400)

#     booking = None
#     for el in bookings:
#         if str(el["userid"]) == str(userid):
#             booking = el
#             break

#     if booking is None:
#         return make_response(jsonify({"error": "User ID not found"}), 400)

#     for date in booking["dates"]:
#         if str(date["date"]) == moviedate:
#             date["movies"].append(movieid)
#             return make_response(jsonify({"message": "booking added"}), 200)

#     booking["dates"].append({"date": moviedate, "movies": [movieid]})
#     return make_response(jsonify({"message": "booking added"}), 200)


# if __name__ == "__main__":
#     print("Server running in port %s" % (PORT))
#     app.run(host=HOST, port=PORT)
   
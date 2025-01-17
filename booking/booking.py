import os

import json

import grpc
import showtime_pb2
import showtime_pb2_grpc

from concurrent import futures
import booking_pb2
import booking_pb2_grpc

### config var ###

bookingHost = os.environ["BOOKING_HOST"]
bookingPort = int(os.environ['BOOKING_PORT'])
showtimeHost = os.environ["SHOWTIME_HOST"]
showtimePort = int(os.environ['SHOWTIME_PORT'])


###            ###


# Servicer giving definition of our API routes #
class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
        # super().__init__() would be useless as the super class have no constructor

    def GetAllBookings(self, request, context):
        for book in self.db:
            yield booking_pb2.Book(
                userid=book['userid'],
                dates=[
                    booking_pb2.BookingDate(date=daty['date'], movies=daty['movies']) for daty in book['dates']
                ]
            )

    def GetBookingByUser(self, request, context):
        for book in self.db:
            if str(book["userid"]) == str(request.userid):
                return booking_pb2.Book(
                    userid=book['userid'],
                    dates=[
                        booking_pb2.BookingDate(date=daty['date'], movies=daty['movies']) for daty in book['dates']
                    ]
                )
        # if user id not found in book, returning an error object, with userId to -1
        return booking_pb2.Book(userid="-1", dates=[])

    def AddBookingByUser(self, request, context):
        movieid = request.movieid
        moviedate = request.date

        # verify the booking is available in the showtime servicer
        try:
            with grpc.insecure_channel(f"{showtimeHost}:{showtimePort}") as channel:
                showTimeStub = showtime_pb2_grpc.ShowTimesStub(channel)
                showTimeDate = showtime_pb2.Date(date=moviedate)
                showtime = showTimeStub.GetScheduleByDate(showTimeDate)
        except Exception as e:
            # if booking can't be done, returning an error object, with userId to -1
            return booking_pb2.Book(userid="-1", dates=[])

        if showtime.date == -1 or movieid not in showtime.movies:
            # if booking can't be done, returning an error object, with userId to -1
            return booking_pb2.Book(userid="-1", dates=[])

        # get user 
        userIndex = None
        for i, userBooking in enumerate(self.db):
            if str(userBooking["userid"]) == str(request.userid):
                userIndex = i
                break

        # or create it if it doesn't already exist
        if userIndex is None:
            user = {'userid': request.userid, 'dates': []}
            self.db.append(user)
            userIndex = len(self.db) - 1

        # get date
        dateIndex = None
        for i, userDate in enumerate(self.db[userIndex]['dates']):
            if str(userDate["date"]) == str(request.date):
                dateIndex = i
                break

        # or create it if it doesn't already exist
        if dateIndex is None:
            date = {'date': request.date, 'movies': []}
            self.db[userIndex]['dates'].append(date)
            dateIndex = len(self.db[userIndex]['dates']) - 1

        self.db[userIndex]['dates'][dateIndex]['movies'].append(request.movieid)
        with open('{}/data/bookings.json'.format("."), "w") as jsf:
            json.dump(self.db, jsf)

        # like in REST convention, returning the just created object
        return booking_pb2.Book(userid=request.userid,
                                dates=[booking_pb2.BookingDate(
                                    date=self.db[userIndex]['dates'][index]['date'],
                                    movies=self.db[userIndex]['dates'][index]['movies']
                                ) for index in range(len(self.db[userIndex]['dates']))])


def serve():
    host = "[::]"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port(f"{host}:{bookingPort}")
    print(f"Server running on {host}:{bookingPort}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

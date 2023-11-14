import json
import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
from werkzeug.exceptions import NotFound

PORT = 3202
HOST = '[::]'


class ShowTimesServicer(showtime_pb2_grpc.ShowTimesServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
        super().__init__() # useless as the super class have no constructor
    
    def GetAllTimes(self, request, context):
        for time in self.db:
            yield showtime_pb2.Time(date=time["date"], movies = time["movies"])
    
    def GetScheduleByDate(self, request, context):
        for schedule in self.db:
            if str(schedule["date"]) == str(request.date):
                return showtime_pb2.Time(date=schedule["date"], movies = schedule["movies"])
        return showtime_pb2.Time(date="-1", movies = [])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowTimesServicer_to_server(ShowTimesServicer(), server)
    server.add_insecure_port(f"{HOST}:{PORT}")
    print(f"Server running on {HOST}:{PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
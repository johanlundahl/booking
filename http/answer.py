from flask import Response
from http.http_status_code import HTTPStatusCode as http
from http.jsoncoder import Encoder

class Send(Response):
    
    @staticmethod
    def created(obj):
        return Response(response=Encoder().encode(obj), status=http.CREATED, mimetype='application/json')

    @staticmethod
    def ok(obj):
        return Response(response=Encoder().encode(obj), status=http.OK, mimetype='application/json')

    @staticmethod
    def deleted():
        return Response(response='', status=http.OK, mimetype='application/json')

    @staticmethod
    def patched():
        return Response(response='', status=http.NO_CONTENT, mimetype='application/json')
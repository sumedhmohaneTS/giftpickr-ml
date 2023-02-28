# utils/api_utils.py

from flask import jsonify

def success_response(data):
    response = {
        'status': 'success',
        'data': data
    }
    return jsonify(response)

def error_response(error_message):
    response = {
        'status': 'error',
        'message': error_message
    }
    return jsonify(response)

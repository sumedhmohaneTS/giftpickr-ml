# utils/api_utils.py


def success_response(message, data=None):
    response = {
        'status': 'success',
        'message': message,
    }
    if data:
        response['data'] = data
    return response


def error_response(error_message):
    response = {
        'status': 'error',
        'message': error_message
    }
    return response

from rest_framework.views import exception_handler

def customExceptionHandler(exc, context):
    response = exception_handler(exc, context)
    print(response)
    if response.status_code == 403:
        response.data = {'status': False, 'message': response.data['detail']}

    return response
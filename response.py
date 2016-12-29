def success(response):
    return {
        'status': 'success',
        'response': response
    }


def error():
    return {
        'status': 'error'
    }


def error_with(response):
    result = error()
    result['response'] = response
    return result

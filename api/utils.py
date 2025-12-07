def format_rate_limit_response(message, retry_after=None):
    resp = {'status': 429, 'message': message}
    headers = {}
    if retry_after:
        headers['Retry-After'] = str(retry_after)
    return resp, headers

import math



def http_header_permutation_middleware(get_response):

    # covert message should be a single int
    full_covert_message = int.from_bytes(b'Say No To War!', "little")

    def middleware_function(request):
        response = get_response(request)

        covert_message_left = request.session.get('covert_message_left', full_covert_message)
        if covert_message_left == 0:
            covert_message_left = full_covert_message
        max_number = math.factorial(len(request.headers))
        number_to_send = covert_message_left % max_number

        sorted_headers_keys = sorted(response.headers.keys(), key = lambda x: x.lower())
        new_headers = {}
        while True:
            headers_left = len(sorted_headers_keys)
            if headers_left == 0:
                break
            header_index = number_to_send % headers_left
            number_to_send = number_to_send // headers_left
            header_key = sorted_headers_keys.pop(header_index)
            new_headers[header_key] = response.headers[header_key]

        response.headers = new_headers
        request.session['covert_message_left'] = covert_message_left // max_number

        return response

    return middleware_function
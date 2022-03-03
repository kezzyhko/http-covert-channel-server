import math



def http_header_permutation_middleware(get_response):

    # covert message should be a single int
    full_covert_message = int.from_bytes(b'Say No To War!', "little")

    def middleware_function(request):
        response = get_response(request)

        covert_message_left = request.session.get('covert_message_left', full_covert_message)
        covert_bits_sent = request.session.get('covert_bits_sent', 0)

        sorted_headers_keys = sorted(response.headers.keys(), key = lambda x: x.lower())
        hidden_bits_amount = math.floor(math.log2(math.factorial(len(sorted_headers_keys))))

        bits_left = covert_message_left.bit_length()
        if bits_left < hidden_bits_amount:
            covert_message_left += full_covert_message << (bits_left + (8 - (covert_bits_sent + bits_left) % 8))

        number_to_send = covert_message_left & ((1 << hidden_bits_amount) - 1)

        request.session['covert_message_left'] = covert_message_left >> hidden_bits_amount
        request.session['covert_bits_sent'] = covert_bits_sent + hidden_bits_amount

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

        return response

    return middleware_function
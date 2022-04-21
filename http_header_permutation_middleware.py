import math
from db_mutex.db_mutex import db_mutex as mutex
from db_mutex import DBMutexError



def http_header_permutation_middleware(get_response):

    # covert message should be a single int
    full_covert_message = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    full_covert_message = int.from_bytes(full_covert_message, "little")

    def middleware_function(request):
        response = get_response(request)
        response.headers['Age'] = None # this header will be added later, but we have to include it in count now
        hidden_bits_amount = math.floor(math.log2(math.factorial(len(response.headers))))

        if not request.session.session_key:
            request.session.create()

        while True:
            try:
                with mutex('covert-session-' + request.session.session_key):
                    request.session.update(request.session.load())
                    covert_bits_sent = request.session.get('covert_bits_sent', 0)
                    if full_covert_message.bit_length() > covert_bits_sent + hidden_bits_amount:
                        request.session['covert_bits_sent'] = covert_bits_sent + hidden_bits_amount
                    else:
                        request.session['covert_bits_sent'] = 0
                    request.session.save()
            except DBMutexError:
                continue
            else:
                break


        response.headers['Age'] = covert_bits_sent
        sorted_headers_keys = sorted(response.headers.keys(), key = lambda x: x.lower())
        number_to_send = (full_covert_message >> covert_bits_sent) & ((1 << hidden_bits_amount) - 1)

        new_headers = {}
        while True:
            headers_left = len(sorted_headers_keys)
            if headers_left == 0:
                break
            header_index = number_to_send % headers_left
            number_to_send //= headers_left
            header_key = sorted_headers_keys.pop(header_index)
            new_headers[header_key] = response.headers[header_key]

        response.headers = new_headers

        return response

    return middleware_function
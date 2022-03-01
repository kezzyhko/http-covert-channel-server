def http_header_permutation_middleware(get_response):

    headers_order = [
        "Cross-Origin-Opener-Policy", 
        # "Date", 
        "Referrer-Policy", 
        # "Server", 
        "X-Content-Type-Options", 
        "X-Frame-Options",
        "Content-Length", 
        "Content-Type", 
    ]

    def middleware_function(request):
        response = get_response(request)

        old_headers = response.headers
        response.headers = dict()
        for header_name in headers_order:
            response.headers[header_name] = old_headers[header_name]

        return response

    return middleware_function
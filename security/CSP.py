def setup_csp(resp):
    resp.headers['Content-Security-Policy'] = "default-src *;" \
                                               "style-src *;" \
                                               "script-src 'unsafe-inline' 'unsafe-eval'"
    return resp
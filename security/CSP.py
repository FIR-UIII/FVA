def setup_csp(resp):
    resp.headers['Content-Security-Policy'] = "default-src *;" \
                                               "style-src *;" \
                                               "frame-src *;" \
                                               "script-src 'self' 'unsafe-inline' 'unsafe-eval'"
    return resp
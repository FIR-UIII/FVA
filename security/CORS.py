from flask_cors import CORS

def setup_cors(app):
    cors = CORS(app, resources={
        r"/*": {
            "origins": "*",  # allow any origin to request resources from site
            "methods": ["GET", "POST"],
            "headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
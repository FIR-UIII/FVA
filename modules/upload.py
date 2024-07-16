from flask import render_template, Blueprint

upload_bp = Blueprint('sw_xss', __name__)

@upload_bp.route('/upload')
def upload():
    return render_template('/upload.html')


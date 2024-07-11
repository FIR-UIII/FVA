from flask import render_template, send_file, Blueprint, request
from os import getcwd as root_folder
from modules.require_authentication import require_authentication


path_travers_bp = Blueprint("path_travers", __name__)


def path_traversal_image(file_path):
    try:
        # vuln here => unsafe func root_folder() and get user {file_path} input without validation
        image_path = f"{root_folder()}{file_path}"
        return send_file(image_path)
    except FileNotFoundError:
        return "File not found", 404


@path_travers_bp.route('/path_travers', methods=['GET'])
@require_authentication
def path_travers():
    return render_template("path_travers.html")


@path_travers_bp.route('/path_travers_img/', methods=['GET'])
def path_travers_img():
    query_param = request.args.get('img')
    return path_traversal_image(query_param)

# http://localhost:8888/path-travers-img/?img=/static/scripting.png
# exploit
# http://localhost:8888/path_travers_img/?img=/secret.txt
# http://localhost:8888/path_travers_img/?img=/../venv.txt
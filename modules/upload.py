from flask import Flask, request, jsonify, render_template, Blueprint
import os

upload_bp = Blueprint('sw_xss', __name__)

@upload_bp.route('/upload')
def upload():
    return render_template('/sw.html')


from flask import Blueprint, render_template, request, jsonify, make_response
import os

simple_bp = Blueprint("simple_web", __name__)


@simple_bp.route('/simple')
def home():
    return render_template('basic_web_fun.html')


@simple_bp.route('/simple/get_content', methods=['GET', 'HEAD'])
def simple_get_content():
    content = {"message": "New Content", "status": "success"}
    response = make_response(jsonify(content), 200)
    return response

@simple_bp.route('/simple/head_content', methods=['HEAD'])
def simple_head_content():
    return '', 204
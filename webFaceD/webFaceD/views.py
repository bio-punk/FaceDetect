"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import jsonify
from webFaceD import app

@app.route('/')
@app.route('/home')
def home():
    rt = {
        "title": "home page",
        "/api": ""
    }
    return (rt)

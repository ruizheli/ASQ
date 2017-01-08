"""
Routes and views for the bottle application.
"""
#test

from bottle import route, view
from datetime import datetime

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/upload')
@view('upload')
def upload():
    """Renders the info page."""
    return dict(
        title='Upload Video',
        year=datetime.now().year
    )

@route('/upload/upload_success')
@view('upload_success')
def upload_success():
    """Renders the info page."""
    return dict(
        title='Upload Success',
        year=datetime.now().year
    )

@route('/upload/upload_fail')
@view('upload_fail')
def upload_success():
    """Renders the info page."""
    return dict(
        title='Upload Success',
        year=datetime.now().year
    )

from flask import Blueprint, render_template, abort, current_app as app
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

@simple_page.route('/')
def show():
    context = {
        'requester': app.fake_api_requester,
        'database': app.fake_database,
    }
    try:
        return render_template('index.html', **context)
    except TemplateNotFound:
        abort(404)

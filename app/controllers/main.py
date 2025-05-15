from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'client':
            return redirect(url_for('client.dashboard'))
        else:  # lawyer
            return redirect(url_for('lawyer.dashboard'))
    return render_template('main/index.html')

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
import webapp.modules.wol as wolModule

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.profile'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, pcList=wolModule.GetPCsList())
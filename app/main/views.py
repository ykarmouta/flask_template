from flask import render_template, session, redirect, url_for, flash, request
from . import main
from ..models import Logement, Batiment
from ..models import User
from flask_login import login_user, logout_user, login_required, \
    current_user

"""
Variable actuelement par défaut:
title: titre de la page
description: description de la page
"""


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None and user.verify_password(request.form['password']):
            login_user(request.form['email'])
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
        attempted_username = request.form['email']
        attempted_password = request.form['password']
    return render_template('index.html')
from flask import render_template, session, redirect, url_for, flash, request
from . import main
from ..models import Logement, Batiment


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
    return render_template('index.html')
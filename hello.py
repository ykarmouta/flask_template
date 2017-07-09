import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField, SelectField
from wtforms.validators import Required
from flask_sqlalchemy import  SQLAlchemy
from flask import jsonify
from flask_pymongo import PyMongo

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MONGO_DBNAME'] = 'locatif'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'
mongo = PyMongo(app)


manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

db.init_app(app)

class Batiment(db.Model):
    __tablename__ = 'batiment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    logements = db.relationship('Logement', backref='batiment')
    def __repr__(self):
        return '<Role %r>' % self.name


class Logement(db.Model):
    __tablename__ = 'logement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    loyer = db.Column(db.Integer)
    batiment_id = db.Column(db.Integer, db.ForeignKey('batiment.id'))
    def __repr__(self):
        return '<Role %r>' % self.name


class batiment_form(FlaskForm):
    name = StringField('nom du logement ?', validators=[Required()])
    submit = SubmitField('Valider')



class logement_form(FlaskForm):
    query_batiment = Batiment.query.all()
    list_batiment = []
    for x in query_batiment:
        list_batiment.append((x.id,x.name))
    name = StringField('nom du logement ?', validators=[Required()])
    loyer = IntegerField('loyers par mois', validators=[Required()])
    batiment = SelectField('A quelle batiment appartient le logement ?',choices=list_batiment)
    submit = SubmitField('Valider')


def make_shell_context():
    return dict(app=app, db=db, Logement=Logement, Batiment=Batiment)
manager.add_command("shell", Shell(make_context=make_shell_context))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = logement_form()
    form2 = batiment_form()
    all_logements = Logement.query.all()
    all_batiments = Batiment.query.all()

    if form.validate_on_submit():
        logement_name = Logement.query.filter_by(name=form.name.data).first()
        if logement_name is None:
            logement = Logement(name=form.name.data, loyer=form.loyer.data, batiment=form.batiment.data)
            db.session.add(logement)
        else:
            flash('ce logement exist deja')
        return redirect(url_for('index'))

    if form2.validate_on_submit():
        batiment_name = Batiment.query.filter_by(name=form2.name.data).first()
        if batiment_name is None:
            batiment = Batiment(name=form2.name.data)
            db.session.add(batiment)
        else:
            flash('ce batiment exist deja')
        return redirect(url_for('index'))
    return render_template('index.html', form=form,form2=form2, name=session.get('name'),
                           all_logements=all_logements, all_batiments=all_batiments)


if __name__ == '__main__':
    manager.run()
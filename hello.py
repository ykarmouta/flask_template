import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField, SelectField
from wtforms.validators import Required
from flask_sqlalchemy import  SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


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
    name = StringField('nom du logement ?', validators=[Required()])
    loyer = IntegerField('loyers par mois', validators=[Required()])
    batiment = SelectField('A quelle batiment appartient le logement ?',choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
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
            logement = Logement(name=form.name.data, loyer=form.loyer.data)
            db.session.add(logement)
        else:
            flash('ce logement exist deja')
        return redirect(url_for('index'))

    if form2.validate_on_submit():
        batiment_name = Batiment.query.filter_by(name=form2.name.data).first()
        print(form2.name.data)
        print(batiment_name)
        if batiment_name is None:
            batiment = Batiment(name=form2.name.data)
            db.session.add(batiment)
        else:
            flash('ce batiment exist deja')
        return redirect(url_for('index'))
    return render_template('index.html', form=form,form2=form2, name=session.get('name'),
                           all_logements=all_logements, all_batiments=all_batiments)


@app.route("/edit/logement/<name>", methods=["GET"])
def edit_logement(name):
    app.logger.debug('returning view_conversation')
    return render_template('example.html')


if __name__ == '__main__':
    manager.run()
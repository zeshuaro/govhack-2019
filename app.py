import os

from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import NumberRange

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
def start_route():
    session['percent'] = 50
    start_form = StartForm()

    if request.method == 'POST' and start_form.validate():
        return redirect(url_for('gender_route'))

    return render_template(
        'index.html', form_type='start', form=start_form, text='Press Start to begin', percent=None)


@app.route('/gender', methods=['GET', 'POST'])
def gender_route():
    gender_form = GenderForm(request.form)
    percent = session['percent']
    text = 'What\'s your gender?'

    if request.method == 'POST':
        if (gender_form.male.data or gender_form.female.data) and gender_form.validate():
            if gender_form.male.data:
                percent += 10
            else:
                percent -= 5

            session['percent'] = percent

            return redirect(url_for('age_route'))

    return render_template(
        'index.html', form_type='gender', form=gender_form, text=text, percent=percent)


@app.route('/age', methods=['GET', 'POST'])
def age_route():
    age_form = AgeForm(request.form)
    percent = session['percent']
    text = 'What\'s your age?'

    if request.method == 'POST':
        if age_form.age.data and age_form.validate():
            age = age_form.age.data
            if age >= 50:
                percent += 10
            else:
                percent -= 5

            session['percent'] = percent

        return redirect(url_for('occupation'))

    return render_template(
        'index.html', form_type='age', form=age_form, text=text, percent=percent)


class StartForm(FlaskForm):
    submit = SubmitField(label='Start')


class GenderForm(FlaskForm):
    form_type = 'gender'
    male = SubmitField(label='Male')
    female = SubmitField(label='Female')


class AgeForm(FlaskForm):
    age = IntegerField('Age', [NumberRange(min=1)])


class OccupationForm(FlaskForm):
    occupation = StringField('Occupation')


class MarriageForm(FlaskForm):
    marriage = StringField('Marriage Status')


if __name__ == '__main__':
    app.run()

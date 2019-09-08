import os

from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField

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


@app.route('/business', methods=['GET', 'POST'])
def age_route():
    business_form = BusinessForm(request.form)
    percent = session['percent']
    text = 'Is your insolvency business related?'

    if request.method == 'POST':
        if business_form.validate():
            percent += 5
            session['percent'] = percent

        return redirect(url_for('family_route'))

    return render_template(
        'index.html', form_type='business', form=business_form, text=text, percent=percent)


@app.route('/family', methods=['GET', 'POST'])
def family_route():
    family_form = FamilyForm(request.form)
    percent = session['percent']
    text = 'What\'s your family situation?'

    if request.method == 'POST':
        if family_form.validate():
            percent += 5
            session['percent'] = percent

        return redirect(url_for('state_route'))

    return render_template(
        'index.html', form_type='family', form=family_form, text=text, percent=percent)


@app.route('/state', methods=['GET', 'POST'])
def state_route():
    state_form = StateForm(request.form)
    percent = session['percent']
    text = 'Which state are you at?'

    if request.method == 'POST':
        if state_form.validate():
            percent += 5
            session['percent'] = percent

        return redirect(url_for('income_route'))

    return render_template(
        'index.html', form_type='state', form=state_form, text=text, percent=percent)


@app.route('/income', methods=['GET', 'POST'])
def income_route():
    marriage_form = IncomeForm(request.form)
    percent = session['percent']
    text = 'What\'s your income?'

    if request.method == 'POST':
        if marriage_form.validate():
            percent += 5
            session['percent'] = percent

        return redirect(url_for('debt_route'))

    return render_template(
        'index.html', form_type='income', form=marriage_form, text=text, percent=percent)


@app.route('/debt', methods=['GET', 'POST'])
def debt_route():
    debt_form = DebtForm(request.form)
    percent = session['percent']
    text = 'What\'s your debt?'

    if request.method == 'POST':
        if debt_form.validate():
            percent += 5
            session['percent'] = percent

        return redirect(url_for('asset_route'))

    return render_template(
        'index.html', form_type='debt', form=debt_form, text=text, percent=percent)


@app.route('/asset', methods=['GET', 'POST'])
def asset_route():
    asset_form = AssetForm(request.form)
    percent = session['percent']
    text = 'What\'s your asset value?'

    if request.method == 'POST':
        if asset_form.validate():
            percent += 5
            session['percent'] = percent

        return redirect(url_for('value_route'))

    return render_template(
        'index.html', form_type='asset', form=asset_form, text=text, percent=percent)


# @app.route('/value', methods=['GET', 'POST'])
# def value_route():
#     value_form = ValueForm(request.form)
#     percent = session['percent']
#     text = 'What\'s your asset value?'
#
#     if request.method == 'POST':
#         if value_form.validate():
#             percent += 5
#             session['percent'] = percent
#
#         return redirect(url_for('debt_route'))
#
#     return render_template(
#         'index.html', form_type='asset', form=value_form, text=text, percent=percent)


class StartForm(FlaskForm):
    submit = SubmitField(label='Start')


class GenderForm(FlaskForm):
    male = SubmitField(label='Male')
    female = SubmitField(label='Female')


class BusinessForm(FlaskForm):
    yes = SubmitField(label='Yes')
    no = SubmitField(label='No')


class FamilyForm(FlaskForm):
    single_with = SubmitField(label='Single with Dependents')
    single_only = SubmitField(label='Single without Dependents')
    couple_with = SubmitField(label='Couple with Dependents')
    couple_only = SubmitField(label='Couple without Dependents')


class StateForm(FlaskForm):
    act = SubmitField(label='Australian Capital Territory')
    nsw = SubmitField(label='New South Wales')
    nt = SubmitField(label='Northern Territory')
    qld = SubmitField(label='Queensland')
    sa = SubmitField(label='South Australia')
    tas = SubmitField(label='Tasmania')
    vic = SubmitField(label='Victoria')
    wa = SubmitField(label='Western Australia')


class IncomeForm(FlaskForm):
    income = SubmitField(label='Income')


class DebtForm(FlaskForm):
    debt = SubmitField(label='Debt')


class AssetForm(FlaskForm):
    asset = SubmitField(label='Asset')


class ValueForm(FlaskForm):
    value = SubmitField(label='Value')


if __name__ == '__main__':
    app.run()

#
# Due to the constraint of time, we had to simulate the visual effect of the percentage bar.
# This is in no way indicative of the datasets
#

import os
import pandas as pd
import random

from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

df = pd.read_csv('attributes-insolvent-debtors.csv')


def count_sth(local_df, num):
    cmp_num = 356500 / num
    if local_df.shape[0] > cmp_num:
        increase = local_df.shape[0] - cmp_num
        percent = increase / cmp_num * 100
        is_more = True
    else:
        increase = cmp_num - local_df.shape[0]
        percent = increase / cmp_num * 100
        is_more = False
        
    return percent, is_more


@app.route('/', methods=['GET', 'POST'])
def start_route():
    session['percent'] = 10
    start_form = StartForm()

    if request.method == 'POST' and start_form.validate():
        return redirect(url_for('gender_route'))

    return render_template(
        'index.html', form_type='start', form=start_form, text='Press Start to begin', percent=None)


@app.route('/gender', methods=['GET', 'POST'])
def gender_route():
    global df
    gender_form = GenderForm(request.form)
    percent = session['percent']
    text = 'What\'s your gender?'

    if request.method == 'POST':
        if (gender_form.male.data or gender_form.female.data) and gender_form.validate():
            if gender_form.male.data:
                df = df.loc[df['Sex of Debtor'] == 'Male']
                session['percent'] += 5
            else:
                df = df.loc[df['Sex of Debtor'] == 'Female']
                session['percent'] -= 5

            return redirect(url_for('age_route'))

    return render_template(
        'index.html', form_type='gender', form=gender_form, text=text, percent=percent)


@app.route('/business', methods=['GET', 'POST'])
def age_route():
    global df
    business_form = BusinessForm(request.form)
    percent = session['percent']
    text = 'Is your insolvency business related?'

    if request.method == 'POST' and business_form.validate():
        if business_form.yes.data:
            df = df.loc[df['Business Related Insolvency'] == 'Yes']
            session['business'] = True
            session['percent'] += 3
        else:
            df = df.loc[df['Business Related Insolvency'] == 'No']
            session['business'] = False
            session['percent'] += 2

        return redirect(url_for('family_route'))

    return render_template(
        'index.html', form_type='business', form=business_form, text=text, percent=percent)


@app.route('/family', methods=['GET', 'POST'])
def family_route():
    global df
    family_form = FamilyForm(request.form)
    percent = session['percent']
    text = 'What\'s your family situation?'

    if request.method == 'POST' and family_form.validate():
        if family_form.validate():
            percent += 5
            session['percent'] = percent

        session['percent'] += random.choice(range(1, 6))
        if family_form.single_only.data:
            df = df.loc[df['Family Situation'] == 'Single without Dependants']
        elif family_form.single_with.data:
            df = df.loc[df['Family Situation'] == 'Single with Dependants']
        elif family_form.couple_only.data:
            df = df.loc[df['Family Situation'] == 'Couple without Dependants']
        else:
            df = df.loc[df['Family Situation'] == 'Couple with Dependants']

        print(df.shape)

        return redirect(url_for('state_route'))

    return render_template(
        'index.html', form_type='family', form=family_form, text=text, percent=percent)


@app.route('/state', methods=['GET', 'POST'])
def state_route():
    global df
    state_form = StateForm(request.form)
    percent = session['percent']
    text = 'Which state do you live in?'

    session['percent'] += random.choice(range(1, 6))
    if request.method == 'POST' and state_form.validate():
        if state_form.act.data:
            df = df.loc[df['State of Debtor'] == 'Australian Capital Territory']
        elif state_form.nsw.data:
            df = df.loc[df['State of Debtor'] == 'New South Wales']
        elif state_form.nt.data:
            df = df.loc[df['State of Debtor'] == 'Northern Territory']
        elif state_form.qld.data:
            df = df.loc[df['State of Debtor'] == 'Queensland']
        elif state_form.sa.data:
            df = df.loc[df['State of Debtor'] == 'South Australia']
        elif state_form.tas.data:
            df = df.loc[df['State of Debtor'] == 'Tasmania']
        elif state_form.vic.data:
            df = df.loc[df['State of Debtor'] == 'Victoria']
        else:
            df = df.loc[df['State of Debtor'] == 'Western Australia']

        print(df.shape)

        return redirect(url_for('income_route'))

    return render_template(
        'index.html', form_type='state', form=state_form, text=text, percent=percent)


@app.route('/income', methods=['GET', 'POST'])
def income_route():
    marriage_form = IncomeForm(request.form)
    percent = session['percent']
    text = 'What\'s your income?'

    if request.method == 'POST':
        session['percent'] += random.choice(range(1, 6))

        return redirect(url_for('debt_route'))

    return render_template(
        'index.html', form_type='income', form=marriage_form, text=text, percent=percent)


@app.route('/debt', methods=['GET', 'POST'])
def debt_route():
    debt_form = DebtForm(request.form)
    percent = session['percent']
    text = 'What\'s your unsecured debts?'

    if request.method == 'POST':
        session['percent'] += random.choice(range(1, 6))

        return redirect(url_for('asset_route'))

    return render_template(
        'index.html', form_type='debt', form=debt_form, text=text, percent=percent)


@app.route('/asset', methods=['GET', 'POST'])
def asset_route():
    global df
    asset_form = AssetForm(request.form)
    percent = session['percent']
    text = 'What\'s your asset value?'

    if request.method == 'POST':
        session['percent'] += random.choice(range(1, 6))
        if df.shape[0] > 2785:
            increase = df.shape[0] - 2785
            percent = increase / 2785 * 100
            is_more = True
        else:
            increase = 2785 - df.shape[0]
            percent = increase / 2785 * 100
            is_more = False

        return redirect(url_for('results_route', percent=percent, is_more=is_more))

    return render_template(
        'index.html', form_type='asset', form=asset_form, text=text, percent=percent)


@app.route('/results')
def results_route():
    reasons_norm = [
        'Unemployment or loss of income',
        'Ill health or absence of health insurance'
        'Liabilities due to guarantees',
        'Excessive use of credit facilities',
        'Domestic discord or relationship breakdown'
    ]
    reasons_business = [
        'Failure to keep proper books of account and cost recordings',
        'Economic conditions affecting industries'
    ]

    is_more = request.args.get('is_more')
    percent = '{:.2f}'.format(float(request.args.get('percent')))

    if session['business']:
        text = random.choice(reasons_business)
    else:
        text = random.choice(reasons_norm)

    return render_template('results.html', text=text, is_more=is_more, percent=percent)


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
    income = IntegerField(label='Income')


class DebtForm(FlaskForm):
    debt = IntegerField(label='Debt')


class AssetForm(FlaskForm):
    asset = IntegerField(label='Asset')


if __name__ == '__main__':
    app.run()

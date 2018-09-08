from flask import Flask, render_template, request
from wtforms import Form, TextField, BooleanField, validators
import sys, os, time, glob
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class InputForm(Form):
    name =  TextField(
            label='AAPL/AMZN/FB/GOOG/WMT',
            default='AAPL',
            validators=[validators.InputRequired()])
    open =  BooleanField(
            label='OPENING PRICE',
            default=False,
            #validators=[validators.InputRequired()]
            )
    high =  BooleanField(
            label='HIGHEST PRICE',
            default=False,
            # validators=[validators.InputRequired()]
            )
    low =   BooleanField(
            label='LOWEST PRICE',
            default=False,
            # validators=[validators.InputRequired()]
            )
    close = BooleanField(
            label='CLOSING PRICE',
            default=False,
            #validators=[validators.InputRequired()]
            )

def generate_plot(company, variables_needed):
    """Return filename of plot of the damped_vibration function."""
    data = pd.read_csv(company+'_short.csv', index_col=0,
                       parse_dates=True)
    data = data[variables_needed]
    data = data.iloc[:30, :]
    plt.figure()
    data.plot()
    plt.ylabel('Price')
    plt.title(company.upper()+' stock price over a month')
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)

    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    return plotfile


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        name_map = {"AAPL": 'apple',
                    "AMZN": 'amazon',
                    "FB": 'facebook',
                    "GOOG": 'google',
                    "WMT": 'walmart'}
        company = name_map[form.name.data]
        variables_needed = []
        if form.open.data: variables_needed.append('Open')
        if form.high.data: variables_needed.append('High')
        if form.low.data: variables_needed.append('Low')
        if form.close.data: variables_needed.append('Close')
        result = generate_plot(company, variables_needed)
    else:
        result = None

    return render_template('view4.html',
                           form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)

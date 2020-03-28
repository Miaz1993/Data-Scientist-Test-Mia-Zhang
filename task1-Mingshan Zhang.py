import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import re

""" Get dataframe"""

df = pd.read_csv('topline_metrics.csv')

""" Get dataframe"""

del df['Date.1']  # Remove df['Date.1'], because it is same as df['Date']

df['Date'] = pd.to_datetime(df['Date'])   # set datetime

df = df.drop_duplicates()   # Get the unique rows in a DataFrame

df['Country'] = df['Country'].apply(lambda x: re.sub(r'\(.*?\)', '', x))   # remove chinese of df['Country']



""" Build dash app """

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

""" Plot countries """

countries = ['Australia', 'Iran', 'China', 'Syria', 'new Zealand', 'Ukraine', 'United States']

plats = list(df['Platform'].value_counts().keys())

def generate_bar1():

    res = []
    for i in plats:
        df1 = df[df['Platform'] == i]
        y = [df1[df1['Country'] == ii].shape[0] for ii in countries]
        res.append({'x': countries, 'y': y, 'type': 'bar', 'name': i})

    return dcc.Graph(
        id='example-graph',
        figure={
            # Use generate_bar1()
            'data': res,
            'layout': {
                'title': 'Platform numbers for different Country'
            }
        }
    )


def generate_bar2():

    bin = [0,2,2.5,3,3.5,4,4.5,5,5.5,6]
    df['cut_Conversion'] = pd.cut(df['Conversion'], bin)

    bins = ["0 ~%2", "2% ~ 2.5%", "2.5% ~ 3%", "3% ~3.5%", "3.5% ~ 4%", "4% ~ 4.5%", "4.5% ~ 5.0%",'5.0% ~ 5.5%', "5.5% ~ 6.0%"]

    plats = [str(i) for i in list(df['Platform'].value_counts().keys())]
    res = []
    for i in plats:
        # df1 = df[df['cut_Conversion']==i]
        df1 = df[df['Platform'] == i]
        y = df1['cut_Conversion'].value_counts().values.tolist()
        print(y)
        res.append({'x': bins[:-1], 'y': y[:-1], 'type': 'bar', 'name': i})
    del df['cut_Conversion']

    return dcc.Graph(
        id='example-graph1',
        figure={
            # Use generate_bar2()
            'data': res,
            'layout': {
                'title': 'Platform numbers for different Conversion'
            }
        }
    )

def generate_tru():

    ress = []
    for i in plats:
        # df1 = df[df['cut_Conversion']==i]
        df1 = df[df['Platform'] == i]
        res = df1.groupby('Date')['TRU'].mean()
        x = [str(i)[:10] for i in list(res.keys())]
        y = res.values.tolist()
        ress.append({'x': x, 'y': y, 'name': i})

    return dcc.Graph(
        id='example-graph2',
        figure={
            'data': ress,
            'layout': {
                'title': 'TRU changes for different Platform'
            }
        }
    )

def generate_DAU():

    ress = []
    for i in plats:
        # df1 = df[df['cut_Conversion']==i]
        df1 = df[df['Platform'] == i]
        res = df1.groupby('Date')['DAU'].mean()
        x = [str(i)[:10] for i in list(res.keys())]
        y = res.values.tolist()
        ress.append({'x': x, 'y': y, 'name': i})

    return dcc.Graph(
        id='example-grapH3',
        figure={
            'data': ress,
            'layout': {
                'title': 'DAU changes for different Platform'
            }
        }
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    # html.H4(children='table display'),
    # generate_table(df),
    html.H4(children='1. Platform distribution for different Country'),
    generate_bar1(),

    html.H4(children='2. Platform distribution for different Conversion'),
    generate_bar2(),

    html.H4(children='3. TRU with datetime'),
    generate_tru(),

    html.H4(children='4. DAU with datetime'),
    generate_DAU()



])


if __name__ == '__main__':
    app.run_server(debug=True, port="1337")
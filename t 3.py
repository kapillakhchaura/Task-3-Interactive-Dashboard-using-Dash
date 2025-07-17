import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv('data/tweets.csv')

# Sentiment count
sentiment_counts = df['airline_sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']

# Charts
fig_pie = px.pie(
    sentiment_counts,
    names='Sentiment',
    values='Count',
    title='Sentiment Distribution',
    color_discrete_sequence=px.colors.qualitative.Set2,
    width=600,
    height=450
)

fig_bar = px.bar(
    sentiment_counts,
    x='Sentiment',
    y='Count',
    color='Sentiment',
    title='Tweet Count per Sentiment',
    width=700,
    height=450,
    color_discrete_map={
        'positive': '#2ca02c',
        'negative': '#d62728',
        'neutral': '#1f77b4'
    }
)

# Dash app
app = dash.Dash(__name__)
app.title = "Airline Dashboard"

# Layout
app.layout = html.Div(style={
    'fontFamily': 'Segoe UI, sans-serif',
    'padding': '25px',
    'backgroundColor': '#f4f4f4'
}, children=[
    html.H1("✈️ Airline Tweets Sentiment Dashboard", style={
        'textAlign': 'center',
        'color': '#003366',
        'marginBottom': '30px',
        'fontSize': '30px'
    }),

    html.Div(style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'flexWrap': 'wrap',
        'gap': '30px',
        'marginBottom': '40px'
    }, children=[
        html.Div(style={
            'flex': '1',
            'minWidth': '500px',
            'boxShadow': '0 4px 10px rgba(0,0,0,0.1)',
            'padding': '15px',
            'borderRadius': '10px',
            'backgroundColor': '#ffffff'
        }, children=[
            dcc.Graph(figure=fig_pie, config={'displayModeBar': False})
        ]),
        html.Div(style={
            'flex': '1',
            'minWidth': '500px',
            'boxShadow': '0 4px 10px rgba(0,0,0,0.1)',
            'padding': '15px',
            'borderRadius': '10px',
            'backgroundColor': '#ffffff'
        }, children=[
            dcc.Graph(figure=fig_bar, config={'displayModeBar': False})
        ])
    ]),

    html.H2("📄 Sample Tweets", style={
        'textAlign': 'center',
        'color': '#003366',
        'fontSize': '24px'
    }),

    html.Div(style={
        'marginTop': '20px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
        'padding': '20px',
        'borderRadius': '10px',
        'backgroundColor': '#ffffff'
    }, children=[
        dash_table.DataTable(
            data=df[['airline', 'airline_sentiment', 'text']].head(10).to_dict('records'),
            columns=[{'name': col.capitalize(), 'id': col} for col in ['airline', 'airline_sentiment', 'text']],
            style_table={'overflowX': 'auto'},
            style_header={
                'backgroundColor': '#003366',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'whiteSpace': 'normal',
                'fontSize': '15px'
            },
            style_data_conditional=[
                {'if': {'filter_query': '{airline_sentiment} = "positive"', 'column_id': 'airline_sentiment'},
                 'backgroundColor': '#d4edda'},
                {'if': {'filter_query': '{airline_sentiment} = "negative"', 'column_id': 'airline_sentiment'},
                 'backgroundColor': '#f8d7da'},
                {'if': {'filter_query': '{airline_sentiment} = "neutral"', 'column_id': 'airline_sentiment'},
                 'backgroundColor': '#fff3cd'}
            ]
        )
    ])
])

if __name__ == '__main__':
    app.run(debug=True)

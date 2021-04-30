# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Mon Apr 26 20:55:07 2021

# @author: kate
# """
###game names df.index and dcc.checklist callback
    
    
import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd 
import plotly as plt 

stylesheet = [ 'https://codepen.io/chriddyp/pen/bWLwgP.css']

# pandas dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

df = pd.read_csv("MA_lottery_complete.csv", index_col = 0)

app = dash.Dash(__name__, external_stylesheets=stylesheet)

#PREPARE MASTER DATA FRAME
#df = pd.read_csv("MA_lottery.csv", index_col = 0)
# for game in df.index:
#     game_df = pd.read_csv("games/" + game + ".csv")
#     game_df["result"] = game_df.prize_amt / game_df.odds_in_one
#     df.loc[game, 'expected_payout'] = game_df["result"].sum() 


# df["payout_ratio"] = df["expected_payout"] / df["card_price"]

# df.to_csv("MA_lottery_complete.csv")

df['Ticket'] = df.index
#df['Max Prize'] =df.max_prize 
#df['Expected Payout'] =df.expected_payout
#df['Payout Ratio'] =df.payout_ratio
#df['Card Price'] =df.card_price

fig = px.scatter(df, x="expected_payout", y="payout_ratio",
                 hover_data=['Ticket'], color='payout_ratio',
                   labels={'Card Price' : 'Payout Ratio'}, height=400)

fig2 = px.scatter(df, x='payout_ratio', y='card_price',
                   hover_data=['expected_payout', 'max_prize'], color='payout_ratio',
                   labels={'Card Price' : 'Payout Ratio'}, height=400), 

#app layout

dropdown_labels = [{'label' : game, 'value' : game} for game in df.index]

app.layout = html.Div([
    html.H1('Da$h for Ca$h', style={'color': 'green',
                                    'fontSize': 65,
                                    'font-style' : 'oblique',
                                    'font-weight' : '900',
                                    'textAlign' : 'center'}),
    html.Br(), 
    dcc.Graph(figure=fig, id='graph'),
    html.Label('Select Your Favorite Mass State Lottery Instant Tickets for Payout Numbers', style={'color': 'black',
                                          'fontSize' : 30,
                                          'font-style' : 'oblique',
                                          'font-weight' : '600',
                                          'color' : 'green'}),
    html.Br(), 
    dcc.Dropdown(options=dropdown_labels,
                 value=df.index,
                 #value=['$1 - Decade of Dollars', '$1,000,000 Bonus Cash'],
                 id = 'dropdown',
                 multi = True),
    html.Br(),
    html.Label('Get the Best Odds', style={'color': 'green',
                                          'fontSize' : 30,
                                          'font-style' : 'oblique',
                                          'font-weight' : '600',
                                          'color' : 'green'}),
    dcc.Checklist(
        id="card_price_checklist",
        options = [
            {'label' : '$1' , 'value' : 1},
            {'label' : '$2' , 'value' : 2},
            {'label' : '$5' , 'value' : 5},
            {'label' : '$10' , 'value' : 10},
            {'label' : '$20' , 'value' : 20},
            {'label' : '$30' , 'value' : 30}
        ],
        value = [1, 2, 5, 10, 20, 30], 
        labelStyle={"display" : "inline-block"},
    ),
    html.Br(), 
    html.Div(id='table'),
    
    html.Br(), 
   
    html.Div(id='slider-output-container'),
    html.Br(), 
    #dcc.Graph(id='graph2'),
    html.A('Get Paid Today? Check Out All the Ways to Spend Your Ca$h!!', 
           href='http://www.masslottery.com',
           target='_blank'),
#Add images
    # fig.add_layout_image(
    #     dict(
    #         source="https://images.ctfassets.net/45roy5e8ztfd/5gMViikY5S2XohWm188WnA/fe19438e57cd9fe04794a8586503d361/mass-logo-300x100.png",
    #         x=0.75,
    #         y=0.65,
    # ))
    ]
)
    
#graph scatter    
@app.callback(
    Output(component_id="graph", component_property='figure'),
    [Input(component_id="dropdown", component_property="value")]
)
def update_plot(games):
    df2 = df.loc[games,].sort_values('card_price')
    df2.card_price = [str(price) for price in df2.card_price]
    fig = px.scatter(df2, x="expected_payout", y = "payout_ratio",
                     color='card_price',
                     hover_data=['Ticket'],
                     title="Ticket Values",
                     labels={"expected_payout" : "Expected Payout ($)",
                             "payout_ratio" : "Payout Ratio",
                             "card_price" : "Card Price"})
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    fig.update_layout(
        font_color="blue",
        title_font_color="green",
        legend_title_font_color="blue"
    )
    
    return fig

#dropdown
@app.callback(
    Output('table', 'children'),
    [Input('dropdown', 'value'),
     Input('card_price_checklist', 'value')]
)
def update_table(games, card_prices):
    df2 = df.loc[games,].sort_values('expected_payout', ascending=False)
    df2 = df2[df2.card_price.isin(card_prices)]
    return generate_table(df2)

# @app.callback(
#     Output("card_price_checklist", "value"),
#     [Input("card_price_checklist", "value")],
# )
# def select_all_none(all_selected, options):
#     all_or_none = []
#     all_or_none = [options["value"] for price in options if all_selected]
#     return all_or_none

#bar chart
# @app.callback(
#     Output(component_id="graph2", component_property='figure'),
#     [Input(component_id="dropdown", component_property="value")]
# )
# def update_plot(games):
#     df2 = df.loc[games,].sort_values('max_prize')
#     df2.max_prize = [str(prize) for prize in df2.max_prize]
#     fig2 = px.scatter(df, x='max_prize', y='card_price',
#                   color='max_prize',
#                   title="Tickets",
#                   labels={"df.index" : "Ticket",
#                           "expected_payout" : "Expected Payout",
#                           "payout_ratio" : "Payout Ratio"})
#     fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
#     fig2.update_layout(
#         font_color="blue",
#         title_font_color="green",
#         legend_title_font_color="blue"
#     )
   
    return fig2
    # html.A('Click Here for the Latest Ma$$ Lottery Instant Games', href='https://www.masslottery.com/games/draw-and-instants?game_types=Instant', 
    #        target='_Blank')

server = app.server

if __name__ == '__main__': 
    app.run_server(debug=True)
    
    
    
    

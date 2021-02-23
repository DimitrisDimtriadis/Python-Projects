from dash_html_components.H1 import H1
from numpy import median
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

def programsPerBU():
    
    dff = df.copy()
    dff = dff.groupby(['Business Unit'])['Business Unit'].size()

    fig = px.bar(
        data_frame=dff,
        x="Business Unit",
        text="Business Unit",
        orientation="h",
        color=dff.index,
        labels={
            "index":"<b>Business Unit</b>"
        }
    )
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside', showlegend=False)
    fig.update_layout(
        uniformtext_minsize=8, 
        uniformtext_mode='hide', 
        plot_bgcolor='rgba(0,0,0,0)',
        height=250,
        width=300,        
        xaxis=dict(range=[3,3]),
        margin=dict(
            t=0
        ))  

    fig.update_layout(xaxis_visible=False, xaxis_showticklabels=False)  

    return fig

def dollarPerBusinessUnit():
    
    dff = df.copy()
    dff = dff.groupby(['Business Unit'])[['Funding Type','Business Unit','Dollar Amount']].sum()
    dff.reset_index(inplace=True)

    mfig = mainGraph(dff, 'Business Unit')
    return mfig

def dollarPerCountry():
    
    dff = df.copy()
    dff = dff.groupby(['Recipient Country'])[['Funding Type','Business Unit','Dollar Amount']].sum()
    dff.reset_index(inplace=True)

    mfig = mainGraph(dff, 'Recipient Country')
    return mfig

def dollarsBySDOH():
    
    dff = df.copy()
    dff = dff.groupby(['SDOH Domain'])[['Funding Type','Business Unit','Dollar Amount']].sum()
    dff.reset_index(inplace=True)
    
    mfig = mainGraph(dff, 'SDOH Domain')
    return mfig

def SDOHDomain():
    
    dff = df.copy()
    dff = dff.groupby(['SDOH Domain', 'Business Unit'])[['Funding Type','Business Unit','Dollar Amount']].sum()
    dff.reset_index(inplace=True)

    fig = px.bar(
        data_frame=dff,
        x='Dollar Amount',
        y='Business Unit',
        text="Dollar Amount",
        color='Business Unit',
        orientation="h",
        facet_col='SDOH Domain' ,
        labels={
            "Business Unit":"<b>Business Unit</b>"
        }       
    )
    fig.update_traces(texttemplate='%{text:$,.2f}', textposition='outside', showlegend=False) #Set view of values right of bars And if need to show Dialog on the right
    fig.update_layout(
        uniformtext_minsize=8, 
        uniformtext_mode='hide', 
        plot_bgcolor='rgba(255,0,0,0)',
        xaxis=dict(range=[0,2000000]),
        margin=dict(
            t=0
        ))

    fig.update_xaxes(showline=True, linewidth=1, linecolor='gray', tickformat=",.2r")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='gray', categoryorder='array', categoryarray=['WRD', 'PBG-IM', 'Corporate Affairs', 'CBO'])
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

    return fig

def mainGraph(mDf ,mainRowForGraph):

    print(mDf[:2])    

    fig = px.bar(
        data_frame=mDf,
        y=mainRowForGraph,
        x="Dollar Amount",
        text="Dollar Amount",
        orientation="h",
        color=mainRowForGraph,
        labels={
            "Dollar Amount":"<b>Dollar Amount</b>",
            mainRowForGraph: "<b>" + mainRowForGraph + "</b>"
        }
    )
    fig.update_traces(texttemplate='%{text:$,.2f}', textposition='outside', showlegend=False) #Set view of values right of bars And if need to show Dialog on the right
    fig.update_layout(
        uniformtext_minsize=8, 
        uniformtext_mode='hide', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[0,2000000]),
        width=500,
        height=250,
        margin=dict(
            t=0
        ))  

    return fig


app = dash.Dash(__name__)
df = pd.read_csv("TestData.csv")

app.layout = html.Div([

    html.Div([    
        html.Div([html.H3("Programs per BU", style={'text-align': 'center'}),
        dcc.Graph(id="my_bee_map0", figure=programsPerBU())], style={'width':'300px', 'heigh':'250px'}),
    
        html.Div([
            html.Div([html.H3("Dollars per Business Unit", style={'text-align': 'center'}),
            dcc.Graph(id="my_bee_map1", figure=dollarPerBusinessUnit())], style={'width':'500px', 'heigh':'250px'}),

            html.Div([html.H3("Dollars per Country", style={'text-align': 'center'}),
            dcc.Graph(id="my_bee_map2", figure=dollarPerCountry())], style={'width':'500px', 'heigh':'250px'}),

            html.Div([html.H3("Dollars by SDOH", style={'text-align': 'center'}),
            dcc.Graph(id="my_bee_map3", figure=dollarsBySDOH())], style={'width':'500px', 'heigh':'250px'})
        ], style={'display':'flex'}),
    ], style={'display':'flex'}),

    html.Div([html.H3("SDOH Domain", style={'text-align': 'center'}),
    dcc.Graph(id="my_bee_map4", figure=SDOHDomain())]),
])   

if __name__ == "__main__":
    app.run_server(debug=True)
#!/home/co60/optsoft/envs/cnv_surf/bin/


import sys
from dash import Dash, html, dcc, Input, Output, callback
# from flask import g
# from numpy import greater
# from pandas.core.apply import relabel_result
# import plotly.express as px
import plotly.graph_objects as go
# from plotly.subplots import make_subplots
import pandas as pd





def annotator(std_value):
    '''This function sets sdt ranges for relevant genes to be shown on a plot.
    It does some cleaning and z-score standardization beforehand. It will output
    two dataframes. First is a matrix with cnv marker positions. Second is
    a matrix with positions of relevant genes on the cnv plot'''

    # TODO replace target .cnn file with app upload
    pth = sys.argv[1]
    df = pd.read_csv(pth, sep="\t")

    df = df[df["gene"] != "-"]
    df["chr_position"] = df["chromosome"].astype(str) + "_" + df["start"].astype(str)
    df["zscore"] = (df["log2"] - df["log2"].mean())/df["log2"].std()
    rel_genes = df[(df['zscore'] >= std_value) | (df['zscore'] <= - std_value)]
    rel_genes["chr_pos_gene"] = df["chr_position"].astype(str) + "_" + df["gene"].astype(str)

    return df, rel_genes


def graphics(df, rel_genes):
    '''This function takes background cnv data and relevant genes cnv data
    and plots it using plotly library'''

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df["chr_position"],
                             y=df["zscore"],
                             mode='markers',
                             opacity=0.7,
                             name='CNV'))

    fig.add_trace(go.Scatter(x=rel_genes["chr_position"],
                             y=rel_genes["zscore"],
                             hovertext=rel_genes["gene"],
                             mode='markers',
                             marker={'size': 10},
                             opacity=0.7,
                             name='Relevant Genes'))

    fig.update_layout(template = "plotly_dark",
                      xaxis_title="Chromosomal Position",
                      yaxis_title="Z-Score",
                      # plot_bgcolor = "rgba(0,0,0,0)",
                      # paper_bgcolor = "rgba(0,0,0,0)",
                      # width=1500,
                      height=900
    )

      
    return fig




backgound_cnv, rel_genes_cvn = annotator(3)

#----------------------- APP LAYOUT --------------------------------


app = Dash(__name__)

app.layout = html.Div(children=[

                      html.Div(className='row',  # Define the row element
                               children=[
                                
                                  html.Div(className='four columns div-user-controls',
                                           children=[html.H1("CNV and Relevant\
                                           genes"),
                                                     html.P('''Move the slider
                                                     to change the standard
                                                     deviation cut-off for
                                                     amplifierd and/or lost
                                                     genes'''),
                                                     html.Label('''Std'''),
                                                     dcc.Slider(id="input_slider",
                                                            min=0.5,
                                                            max=10.0,
                                                            value=3
                                                    ),
                                                     
                                            ]),

                                  html.Div(className='eight columns div-for-charts bg-grey',
                                           children=[
                                                dcc.Graph(id='example-graph',
                                                        animate=True,
                                                        figure = graphics(backgound_cnv, rel_genes_cvn),
                                                ),
                                           ]), 

                                  ])
                                ])


@callback(
    Output(component_id="example-graph", component_property='figure'),
    Input(component_id="input_slider", component_property="value")
)


def update_output_div(input_value):
    print(f"here is the value {input_value}")
    backgound_cnv, rel_genes_cvn = annotator(input_value)
    fig = graphics(backgound_cnv, rel_genes_cvn )

    return fig


#----------------------- ENTRY POINT --------------------------------

if __name__ == '__main__':

    app.run(debug=True)




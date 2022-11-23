import plotly.graph_objects as go 

def render_scatter(df1, df2, y_column_1, y_column_2): 
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                  x = df1[y_column_1],
                  y = df2[y_column_2],
                  mode = 'markers', 
                 ),)
    
    fig.update_xaxes(title_text=f"{y_column_1}")
    fig.update_yaxes(title_text=f"{y_column_2}")
    return fig
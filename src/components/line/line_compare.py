import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_two_lines(df1, df2, x_column, y_column_1, y_column_2, color_column=None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
                  x = df1[x_column],
                  y = df1[y_column_1],
                  mode = 'lines'),
                  secondary_y=False)
    fig.add_trace(go.Scatter(
                  x = df2[x_column],
                  y = df2[y_column_2],
                  mode = 'lines'),
                  secondary_y=True)
    
    fig.update_yaxes(title_text=f"{y_column_1}", secondary_y=False)
    fig.update_yaxes(title_text=f"{y_column_2}", secondary_y=True)
    return  fig
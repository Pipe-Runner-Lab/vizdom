from dash.exceptions import PreventUpdate


def get_date_range(relayoutData):
  if relayoutData is None or relayoutData.get("dragmode", None) == "pan":
    raise PreventUpdate

  start_date = relayoutData.get("xaxis.range[0]", None)
  end_date = relayoutData.get("xaxis.range[1]", None)

  return start_date, end_date
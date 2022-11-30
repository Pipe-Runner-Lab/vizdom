def data_bars(df, column):
    n_bins = 100
    # bounds = np.arange(-1.0, 1.01, 0.01)
    # bounds = bounds.round(5)
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [i for i in bounds]
    color_above = 'green'
    color_below = 'red'
    styles = []
    midpoint_pos = 1 / 2
    midpoint_neg = -1 / 2
    for i in range(1, len(bounds)):
        background = None
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        min_bound_percentage = bounds[i - 1] * 100
        max_bound_percentage = bounds[i] * 100
        style = {
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (
                            i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'paddingBottom': 2,
                'paddingTop': 2
            }
        for corr in df['Correlation']:
            absCorr = abs(corr)
            print(absCorr)
            
            if max_bound > midpoint_pos:
                background = (
                """
                    linear-gradient(to right,
                    {color_above} 0%,
                    {color_above} {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(
                    max_bound_percentage=max_bound_percentage,
                    color_above=color_above
                )
            )
            elif max_bound <= midpoint_pos:
                background = (
                """
                    linear-gradient(to right,
                    {color_below} 0%,
                    {color_below} {min_bound_percentage}%,
                    white {min_bound_percentage}%,
                    white 100%)
                """.format(
                    min_bound_percentage=min_bound_percentage,
                    color_below=color_below
                )
            )
            
            style['background'] = background
            styles.append(style)
    
    return styles
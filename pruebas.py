app.layout = html.Div(
    className="container scalable",
    children=[
        html.Div(
            id="banner",
            className="banner",
            children=[
                html.H6("US Flights"),
                html.Img(src=app.get_asset_url("plotly_logo.png")),
            ],
        ),
        html.Div(children='Desarrollado por Rodrigo Ramirez', style={
                    'textAlign': 'center',
                    'color': colors2['text']
                }),

        html.Div(
            className="app_main_content",
            children=[
                html.Div(
                    id="dropdown-select-outer",
                    children=[
                        html.Div(
                            [
                                html.P("Select Departure/Arrival"),
                                dcc.Dropdown(
                                    id="dropdown-select",
                                    options=[
                                        {"label": "Departure", "value": "dep"},
                                        {"label": "Arrival", "value": "arr"},
                                    ],
                                    value="dep",
                                ),
                            ],
                            className="selector",
                        ),
                        html.Div(
                            [
                                html.P("Select Date Range"),
                                dcc.DatePickerRange(
                                    id="date-picker-range",
                                    min_date_allowed=dt(2008, 1, 1),
                                    max_date_allowed=dt(
                                        2008, 1, 7
                                    ),  # set maximum limit according to local casting
                                    initial_visible_month=dt(2008, 1, 1),
                                    minimum_nights=3,
                                    display_format="MMM Do, YY",
                                    start_date=dt(2008, 1, 1),
                                    end_date=dt(2008, 1, 7),
                                ),
                            ],
                            id="date-picker-outer",
                            className="selector",
                        ),
                    ],
                ),
                html.Div(
                    id="top-row",
                    className="row",
                    children=[
                        html.Div(
                            id="map_geo_outer",
                            className="seven columns",
                            # avg arrival/dep delay by destination state
                            children=dcc.Graph(id="choropleth"),
                        ),
                        html.Div(
                            id="flights_by_day_hm_outer",
                            className="five columns",
                            children=dcc.Loading(children=dcc.Graph(id="flights_hm")),
                        ),
                    ],
                ),
                html.Div(
                    id="middle-row",
                    className="row",
                    children=[
                        html.Div(
                            id="Flights-by-city-outer",
                            className="six columns",
                            children=dcc.Loading(
                                children=dcc.Graph(id="value_by_city_graph")
                            ),
                        ),
                        html.Div(
                            id="time-series-outer",
                            className="six columns",
                            children=dcc.Loading(
                                children=dcc.Graph(
                                    id="flights_time_series",
                                    figure=generate_time_series_chart(
                                        "",
                                        "2018-01-01 00:00:00",
                                        "2018-01-08 00:00:00",
                                        "dep",
                                    ),
                                )
                            ),
                        ),
                    ],
                ),
                html.Div(
                    id="bottom-row",
                    className="row",
                    children=[
                        html.Div(
                            id="Count_by_days_outer",
                            className="four columns",
                            children=dcc.Loading(
                                children=dcc.Graph(id="count_by_day_graph")
                            ),
                        ),
                        html.Div(
                            id="flight_info_table_outer",
                            className="eight columns",
                            children=dcc.Loading(
                                id="table-loading",
                                children=dash_table.DataTable(
                                    id="flights-table",
                                    columns=[
                                        {"name": i, "id": i}
                                        for i in [
                                            "flightnum",
                                            "dep_timestamp",
                                            "arr_timestamp",
                                            "origin_city",
                                            "dest_city",
                                        ]
                                    ],
                                    filter_action="native",
                                    fill_width=True,
                                    data=[],
                                    style_as_list_view=True,
                                    style_header={
                                        "textTransform": "Uppercase",
                                        "fontWeight": "bold",
                                        "backgroundColor": "#ffffff",
                                        "padding": "10px 0px",
                                    },
                                    style_data_conditional=[
                                        {
                                            "if": {"row_index": "even"},
                                            "backgroundColor": "#f5f6f7",
                                        },
                                        {
                                            "if": {"row_index": "odd"},
                                            "backgroundColor": "#ffffff",
                                        },
                                    ],
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ],
)
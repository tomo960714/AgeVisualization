import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    # Sidebar
    html.Nav(id='sidebar', className='bg-light', children=[
        html.Div(id='dismiss', children=[
            html.I(className='fas fa-arrow-left')
        ]),
        html.Div(className='sidebar-header', children=[
            html.H3('Bootstrap Sidebar')
        ]),
        html.Ul(className='list-unstyled components', children=[
            html.P('Dummy Heading'),
            html.Li(className='active', children=[
                html.A(href='#homeSubmenu', children='Home', data_toggle='collapse', aria_expanded='false'),
                html.Ul(className='collapse list-unstyled', id='homeSubmenu', children=[
                    html.Li(children=[
                        html.A(href='#', children='Home 1')
                    ]),
                    html.Li(children=[
                        html.A(href='#', children='Home 2')
                    ]),
                    html.Li(children=[
                        html.A(href='#', children='Home 3')
                    ]),
                ])
            ]),
            html.Li(children=[
                html.A(href='#', children='About'),
                html.A(href='#pageSubmenu', children='Pages', data_toggle='collapse', aria_expanded='false'),
                html.Ul(className='collapse list-unstyled', id='pageSubmenu', children=[
                    html.Li(children=[
                        html.A(href='#', children='Page 1')
                    ]),
                    html.Li(children=[
                        html.A(href='#', children='Page 2')
                    ]),
                    html.Li(children=[
                        html.A(href='#', children='Page 3')
                    ]),
                ])
            ]),
            html.Li(children=[
                html.A(href='#', children='Portfolio')
            ]),
            html.Li(children=[
                html.A(href='#', children='Contact')
            ]),
        ])
    ]),

    # Page Content
    html.Div(id='content', children=[
        html.Nav(className='navbar navbar-expand-lg navbar-light bg-light', children=[
            html.Div(className='container-fluid', children=[
                html.Button(id='sidebarCollapse', type='button', className='btn btn-info', children=[
                    html.I(className='fas fa-align-left'),
                    html.Span('Toggle Sidebar')
                ])
            ])
        ])
    ]),

    # Dark Overlay element
    html.Div(id='overlay', className='overlay')
])

# Callback to toggle the sidebar and overlay visibility
@app.callback(
    [Output('sidebar', 'className'),
     Output('overlay', 'className')],
    [Input('dismiss', 'n_clicks'),
     Input('sidebarCollapse', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_sidebar(dismiss_clicks, collapse_clicks):
    ctx = dash.callback_context
    if ctx.triggered_id == 'dismiss':
        return 'bg-light', 'overlay'
    elif ctx.triggered_id == 'sidebarCollapse':
        return 'bg-light active', 'overlay active'
    else:
        return dash.no_update, dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)

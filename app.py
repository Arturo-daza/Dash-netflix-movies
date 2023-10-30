import dash
from dash import dcc, html, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd


df_netflix = pd.read_csv('netflix_titles.csv', encoding='ISO-8859-1', sep = ";")

df_netflix = df_netflix.sort_values(by="release_year", ascending=False)

pie_type = px.pie(df_netflix, values="show_id", names="type", title="Pie Chart of Shows by Type")

df_freq_rating = df_netflix.groupby(["type", "rating"]).size().reset_index(name="Quantity")
df_freq_rating = df_freq_rating.sort_values(by = "Quantity", ascending = False)
bar_rating = px.bar(df_freq_rating, x="Quantity", y="rating", color="type", title="Bar Chart of Shows by Rating and Type", orientation = "h")

# Quantity of movies by year and type 
df_freq = df_netflix.groupby(["type", "release_year"]).size().reset_index(name="Quantity")
line_bar_year = px.line(df_freq, x="release_year", y="Quantity", color="type", title="Quantity of movies by year and type")


# Top 5 Countrys Shows by Type
df_freq_country = df_netflix.groupby(["type", "country"]).size().reset_index(name="Quantity")
df_freq_country = df_freq_country.sort_values(by = "Quantity", ascending = False)
bar_country = px.bar(df_freq_country.iloc[0:7], x="country", y="Quantity", color="type", title="Top 5 Countrys Shows by Type")

rating_list = df_netflix['rating'].drop_duplicates().dropna().values.tolist()


app = dash.Dash()

app.layout = html.Div([html.Div(children=f'Netflix Movies, total register {df_netflix.shape[0]}'),
                        html.Hr(),     
                        html.Div([
                            "Select a type",
                            dcc.Dropdown(id='type', options=[{'label':'All', 'value':'All'},{'label':'Movie', 'value':'Movie'},{'label':'TV Show', 'value':'TV Show'}],value='All')
                        ], style={'width' :'50%', 'display':'inline-block'}),   
                        html.Div([
                            "Select a rating",
                            dcc.Dropdown(id="rating", options=rating_list, placeholder = "You can select many", multi=True)
                        ], style={'width' :'50%', 'display':'inline-block'}),          
                        html.Div([dcc.Graph(id='pie_type',figure=pie_type)], style={'width' :'50%', 'display':'inline-block'}),
                        html.Div([dcc.Graph(id='bar_country',figure=bar_country)], style={'width' :'50%', 'display':'inline-block'}),
                        html.Hr(),
                        html.Div([dcc.Graph(id='bar_rating',figure=bar_rating)], style={'width' :'100%', 'display':'inline-block'}),
                        html.Hr(),
                        html.Div([dcc.Graph(id='line_bar_year',figure=line_bar_year)], style={'width' :'100%', 'display':'inline-block'}), 
                        html.Hr(),
                        dash_table.DataTable(data=df_netflix[["title", "director", "release_year", "rating", "duration"]].to_dict('records'), page_size=10)
                        ])

@callback(
    [Output(component_id='pie_type', component_property='figure'),Output(component_id='bar_rating', component_property='figure'), Output(component_id='bar_country', component_property='figure'), Output(component_id='line_bar_year', component_property='figure')],
    [Input(component_id='type', component_property='value')], 
    [Input(component_id='rating', component_property='value')] 
)

def update_graph(types, rating):
    condition_types = df_netflix['type'] == types
    if rating == []:
        rating =None
    if rating is not None:
        condition_rating = df_netflix['rating'].isin(rating)
        
    if types != 'All' and rating is not None:
        df_netflix_type = df_netflix[condition_types & condition_rating]
    elif types != 'All' and  rating is None:
        df_netflix_type = df_netflix[condition_types]
    elif types == "All" and rating is not None:
        df_netflix_type = df_netflix[condition_rating]
    else:
        df_netflix_type = df_netflix
    pie_type = px.pie(df_netflix_type, values="show_id", names="type", title="Pie Chart of Shows by Type")
    #bar_rating= px.bar(df_netflix_type, x="show_id", y="rating", color="type", title="Bar Chart of Shows by Rating and Type", orientation = "h")
    df_freq_rating = df_netflix_type.groupby(["type", "rating"]).size().reset_index(name="Quantity")
    df_freq_rating = df_freq_rating.sort_values(by = "Quantity", ascending = False)
    bar_rating = px.bar(df_freq_rating, x="Quantity", y="rating", color="type", title="Bar Chart of Shows by Rating and Type", orientation = "h")
    
    
    df_freq = df_netflix_type.groupby(["type", "release_year"]).size().reset_index(name="Quantity")
    line_bar_year = px.line(df_freq, x="release_year", y="Quantity", color="type", title="Quantity of movies by year and type")
    df_freq_country = df_netflix_type.groupby(["type", "country"]).size().reset_index(name="Quantity")
    df_freq_country = df_freq_country.sort_values(by = "Quantity", ascending = False)
    bar_country = px.bar(df_freq_country.iloc[0:7], x="country", y="Quantity", color="type", title="Countrys Shows by Type")




    return pie_type, bar_country, bar_rating, line_bar_year
    



if __name__ == '__main__':
    app.run_server(debug=True)
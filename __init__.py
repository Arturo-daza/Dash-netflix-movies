# %%
import plotly.express as px
import pandas as pd

df_ventas = pd.read_csv('VentasProductosDeportivos.csv')
df_ventas.head()

# %%
df_ventas = df_ventas.sort_values(by='Fecha')

line_graph = px.line(data_frame=df_ventas, x='Fecha', y='Total', title='Ventas diarias')
line_graph.update_xaxes(type='category')
line_graph.show()

# %%
bar_graph = px.bar(data_frame=df_ventas, y = 'Descripcion', x = 'Cantidad', title='Ventas unidades', orientation='h')
bar_graph.update_layout(width=800, height=400)
bar_graph.show()

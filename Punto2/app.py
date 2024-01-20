import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

#------------------------------------------------------------------------------------------------------------------------------------------------------
# Lectura de datos
#------------------------------------------------------------------------------------------------------------------------------------------------------

month_places = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
# Concepto puede ser Cost o Revenue
def leer_y_limpiar_data(filepath,concept):
    work_file = pd.read_csv(filepath)
    
    if concept=='Revenue':
        id_cols = ['N', 'Client Name', 'Line Of Business']
    elif concept=='Cost':
        id_cols = ['N', 'Expense Item', 'Line Of Business']
        
    work_file_unpivot = pd.melt(work_file, id_vars=id_cols, var_name='Month', value_name=concept)
    work_file_unpivot = work_file_unpivot[work_file_unpivot['Month'] != 'Total']
    work_file_unpivot['Month'] = work_file_unpivot['Month'].str.lower().map(month_places)
    work_file_unpivot['Month'] = work_file_unpivot['Month'].astype(str) + '-' + work_file_unpivot['Month'].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%b'))
    
    if concept=='Revenue':
        work_file_unpivot[concept] = work_file_unpivot[concept].str.replace('$', '')
        work_file_unpivot[concept] = work_file_unpivot[concept].str.rstrip('0')
        work_file_unpivot[concept] = work_file_unpivot[concept].str.replace('.', '')
        work_file_unpivot[concept] = work_file_unpivot[concept].str.replace(',', '')
        work_file_unpivot['Line Of Business'] = work_file_unpivot['Line Of Business'].str.replace(' Revenue', '')

    work_file_unpivot[concept] = pd.to_numeric(work_file_unpivot[concept], downcast="float")
    work_file_unpivot = work_file_unpivot.groupby(id_cols + ['Month']).agg({concept: 'sum'}).reset_index()
    work_file_unpivot = work_file_unpivot.groupby(['Line Of Business', 'Month']).agg({concept: 'sum'}).reset_index()
    work_file_unpivot["Concept"] = concept
    work_file_unpivot.columns = ["Line Of Business","Month","Value","Concept"]

    return work_file_unpivot

costs_unpivot = leer_y_limpiar_data('./data/costs_2022.csv', 'Cost')
revenue_unpivot = leer_y_limpiar_data('./data/revenue_2022.csv', 'Revenue')
df_melted = pd.concat([costs_unpivot, revenue_unpivot], ignore_index=True)

#------------------------------------------------------------------------------------------------------------------------------------------------------
# Dashboard
#------------------------------------------------------------------------------------------------------------------------------------------------------
df = df_melted
app = dash.Dash(__name__)

# Layout del dashboard
app.layout = html.Div([
    dcc.Dropdown(
        id='category-filter',
        options=[{'label': category, 'value': category} for category in df['Line Of Business'].unique()],
        multi=True,
        value=df['Line Of Business'].unique()
    ),
    
    dcc.Graph(id='line-chart'),
])

# Callback para actualizar el gráfico según los valores seleccionados
@app.callback(
    Output('line-chart', 'figure'),
    [Input('category-filter', 'value')]
)



def update_chart(selected_categories):
    # Crear gráfica. Separa entre cost y revenue.
    fig = go.Figure()
    df_selected = df[df['Line Of Business'].isin(selected_categories)]

    for line_of_business in df_selected['Line Of Business'].unique():
        for concept in df_selected['Concept'].unique():
            df_filtered = df_selected[(df_selected['Line Of Business'] == line_of_business) & (df_selected['Concept'] == concept)]
            trace = go.Scatter(
                x=df_filtered['Month'],
                y=df_filtered['Value'],
                mode='lines+markers',
                name=f"{line_of_business} - {concept}",
                line=dict(dash='dash' if concept == 'Cost' else 'solid')
            )
            # Fijar segundo eje y
            if concept == 'Revenue':
                trace.update(dict(yaxis='y2'))

            fig.add_trace(trace)

    # Actualizar layout
    fig.update_layout(
        xaxis=dict(title='Month'),
        yaxis=dict(title='Cost'),
        yaxis2=dict(title='Revenue', overlaying='y', side='right'),
        title='Cost and Revenue, per Line of Business',
        legend=dict(x=1.1, y=0.5)      )

    
    return fig

#------------------------------------------------------------------------------------------------------------------------------------------------------
# Correr la app
#------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
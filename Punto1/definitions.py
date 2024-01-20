import pandas as pd
from tabulate import tabulate
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

#------------------------------------------------------------------------------------------------------------------------------------------------------
# Definicion de funciones
#------------------------------------------------------------------------------------------------------------------------------------------------------
months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
opciones = ['Q1_Forecast', 'Q2_Forecast', 'Q3_Forecast','Q4_Forecast']

# Creación de las subseries propias y compartidas que componen los Forecast
def crear_estructura_forecast_trim (months, trimestre):
    inicio = (trimestre - 1) * 3
    fin = trimestre * 3
    Data = [{month: None} for month in months[inicio:fin]]
    DataAdicional = [{month: None} for month in months[fin:]]
    
    return Data, DataAdicional

def crear_estructura():
    global Q1_Data, Q1_DataAdicional, Q2_Data, Q2_DataAdicional, Q3_Data, Q3_DataAdicional, Q4_Data, Q4_DataAdicional
    Q1_Data, Q1_DataAdicional= crear_estructura_forecast_trim(months,1)
    Q2_Data, Q2_DataAdicional= crear_estructura_forecast_trim(months,2)
    Q3_Data, Q3_DataAdicional= crear_estructura_forecast_trim(months,3)
    Q4_Data, Q4_DataAdicional= crear_estructura_forecast_trim(months,4)

# Consolidación del modelo de datos. Los forecast son la unión de subseries.
def consolidar():
    Q1_Forecast = Q1_Data + Q1_DataAdicional
    Q2_Forecast = Q1_Data + Q2_Data + Q2_DataAdicional
    Q3_Forecast = Q1_Data + Q2_Data + Q3_Data + Q3_DataAdicional
    Q4_Forecast = Q1_Data + Q2_Data + Q3_Data + Q4_Data
    forecasts = [Q1_Forecast, Q2_Forecast, Q3_Forecast, Q4_Forecast]
    return forecasts

def resumir_forecast (forecasts):
    tmp_forecast = []
    for i, forecast in enumerate(forecasts, start=1):
        df_temp = pd.DataFrame({'Forecast': f'Q{i}_Forecast',**{k: [v] for diccionario in forecast for k, v in diccionario.items()}})
        tmp_forecast.append(df_temp)
    resumen_forecast = pd.concat(tmp_forecast, ignore_index=True).fillna('')
    resumen_forecast = tabulate(resumen_forecast, headers='keys', tablefmt='pretty', showindex=False)
    return resumen_forecast

# Actualización del valor en el forecast especificado y se comparte el valor con los demás forecast, según corresponda
def update_un_forecast(Q_Listas, Mes, Valor):
        for Q_Lista in Q_Listas:
            for dictionary in Q_Lista:
                if Mes in dictionary:
                    dictionary[Mes] = Valor

def actualizar_todo(Q, Mes, Valor):
    if Q == "Q1_Forecast":
        update_un_forecast( [Q1_Data, Q1_DataAdicional], Mes, Valor)
    elif (Q == "Q2_Forecast"):
        update_un_forecast( [Q1_Data, Q2_Data, Q2_DataAdicional], Mes, Valor)
    elif Q == "Q3_Forecast":
        update_un_forecast( [Q1_Data, Q2_Data, Q3_Data, Q3_DataAdicional], Mes, Valor)
    elif Q == "Q4_Forecast":
        update_un_forecast( [Q1_Data, Q2_Data, Q3_Data, Q4_Data], Mes, Valor)
    else:
        print(f"Note: {Q} no existe.")


def actualizar_y_mostrar_prediccion(Q, Mes, Valor):
    actualizar_todo(Q, Mes, Valor)
    forecasts = consolidar()
    print(resumir_forecast(forecasts))



#------------------------------------------------------------------------------------------------------------------------------------------------------
# Inicialización
crear_estructura()
#------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------
# Definición del layout para la aplicación.
# Contiene widgets para establecer la serie, mes y el valor a actualizar, y botones para correr/reiniciar.
#------------------------------------------------------------------------------------------------------------------------------------------------------

# Fondo
css_code = """
<style>
    .output_wrapper {
        background-color: blue;  /* Cambia este valor según tus preferencias */
    }
    
    .widget-box {
        background-color: lightblue;  /* Cambia este valor según tus preferencias */
    }
</style>
"""

display(HTML(css_code))

# Definición de Widgets
layout = widgets.Layout(width='auto', height='400px')
title = widgets.HTML('<h2>Actualización de forecast para datos compartidos.</h2>')
dropdown_forecast = widgets.Dropdown(options=opciones)
dropdown_month = widgets.Dropdown(options=months)
input_prediction = widgets.FloatText(value=0.0)
run_button = widgets.Button(description='Run', style=widgets.ButtonStyle(button_color='mediumseagreen'))
restart_button = widgets.Button(description='Restart', style=widgets.ButtonStyle(button_color='dodgerblue'))

# Organizar los widgets
vbox = widgets.VBox([title,
                    widgets.Label('Forecast a actualizar'), 
                     dropdown_forecast,
                     widgets.Label('Mes'), 
                     dropdown_month,
                     widgets.Label('Valor pronosticado'),
                     input_prediction,
                     run_button,
                     restart_button]) 


# Funciones para manejar los cambios o el click en los botones
def on_input_prediction_change(change):
    entered_value = change['new']

def on_option_change(change):
    selected_option = change['new']

def on_run_button_click(run_button):
    with out:
        clear_output()
        Q = dropdown_forecast.value
        Mes = dropdown_month.value
        Valor = input_prediction.value
        print('----------------------------------------------------------------------------------------')
        print(f'Actualizando: {Q},  Mes: {Mes}, Valor: {Valor}')
        print('----------------------------------------------------------------------------------------')
        actualizar_y_mostrar_prediccion(Q, Mes, Valor)

def on_restart_button_click(restart_button):
    with out:
        clear_output()
        crear_estructura()
        print('----------------------------------------------------------------------------------------')
        print(f'Reiniciando. Por favor, realice una nueva predicción')
        print('----------------------------------------------------------------------------------------')
        return
        


# Observar cambios
dropdown_forecast.observe(on_option_change, names='value')
dropdown_month.observe(on_option_change, names='value')
input_prediction.observe(on_input_prediction_change, names='value')
run_button.on_click(on_run_button_click)
restart_button.on_click(on_restart_button_click)

# Visualización
display(vbox)
out = widgets.Output()
display(out)


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import requests
import json
import plotly.graph_objs as go
import plotly.express as px

from flask import Flask
import os


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']




server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')
app = dash.Dash(name = __name__, server = server,external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True


casos_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto13/CasosNuevosCumulativo.csv')
data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
fallecidos_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
grupo_uci_reg = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto8/UCI.csv')
data_comunas = pd.read_csv('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/Casos-Comunas/COVID19.csv')
data_casos_por_comuna2 = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv')
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')


#comuna
data_casos_por_comuna = pd.read_csv('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/Casos-Comunas/casosAcumulados.csv')
data_fallecidos_por_comuna = pd.read_csv('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/Casos-Comunas/fallecidosAcumulados.csv')
data_activos_por_comuna = pd.read_csv('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/Casos-Comunas/casosActivos.csv')

#comunas:

fecha_casos_comuna =data_casos_por_comuna2.columns
fecha_casos_comuna= fecha_casos_comuna[5:]

fecha_fallecidos_comuna =data_fallecidos_por_comuna.columns
fecha_fallecidos_comuna= fecha_fallecidos_comuna[5:]

fecha_activos_comuna =data_activos_por_comuna.columns
fecha_activos_comuna= fecha_activos_comuna[5:]
#Regiones
#hospitalizaciones
hosp_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto8/UCI.csv')
fecha_hosp_region =hosp_region.columns
fecha_hosp_region= fecha_hosp_region[3:]


data_activos_region = data_activos_por_comuna[data_activos_por_comuna['Comuna']=='Total']
data_activos_region.loc[data_activos_region['Region'] == 'Tarapaca', "Region"] = 'Tarapacá'
data_activos_region.loc[data_activos_region['Region'] == 'Valparaiso', "Region"] = 'Valparaíso'
data_activos_region.loc[data_activos_region['Region'] == 'Biobio', "Region"] = 'Biobío'
data_activos_region.loc[data_activos_region['Region'] == 'Araucania', "Region"] = 'Araucanía'
data_activos_region.loc[data_activos_region['Region'] == 'Los Rios', "Region"] = 'Los Ríos'
data_activos_region.loc[data_activos_region['Region'] == 'Aysen', "Region"] = 'Aysén'
data_activos_region.loc[data_activos_region['Region'] == 'Magallanes y la Antartica', "Region"] = 'Magallanes'
data_activos_region.loc[data_activos_region['Region'] == 'Del Libertador General Bernardo O’Higgins', "Region"] = 'O’Higgins'
data_activos_region.loc[data_activos_region['Region'] == 'La Araucania', "Region"] = 'Araucanía'

fecha_activos_region =data_activos_region.columns
fecha_activos_region= fecha_activos_region[5:]


ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]






#CHILE

fecha_casos_totales =data_crec_por_dia.columns
fecha_casos_totales= fecha_casos_totales[1:]

data_region = data_chile[['Region',ultima_fecha_cl]]
data_region = data_region.rename(columns={ultima_fecha_cl:'Casos'})

#carga de mapas json
resp = requests.get('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/geo-json/regiones.json')
geo_region = json.loads(resp.content)

resp_comunas = requests.get('https://raw.githubusercontent.com/rgcl/geojson-cl/master/comunas.json')
geo_comunas = json.loads(resp_comunas.content)


fecha_cd =casos_por_dia.columns
fecha_cd= fecha_cd[1:]


fecha_fd =fallecidos_por_dia.columns
fecha_fd= fecha_fd[1:]

fecha_uci=grupo_uci_reg.columns
fecha_uci= fecha_uci[3:]


#MUNDO

data_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recoveries_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

mundo = requests.get('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')
geo_mundo = json.loads(mundo.content)


data_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

ultima_fecha_mundo = data_confirmed.columns
ultima_fecha_mundo= ultima_fecha_mundo[-1]


data_confirmed.loc[data_confirmed['Country/Region'] == 'US', "Country/Region"] = 'United States of America'

data_confirmed.loc[data_confirmed['Country/Region'] == 'US', "Country/Region"] = 'United States of America'
data_confirmed.loc[data_confirmed['Country/Region'] == 'Congo (Kinshasa)', "Country/Region"] = 'Democratic Republic of the Congo'

#AGREGAR French Guiana COMO PAIS Y NO PROVICNCIA DE FRANCIA PERO SE SUMAR A EL TOTAL DE FRANCIA IGUAL
data_confirmed = data_confirmed.append({'Country/Region':'French Guiana',ultima_fecha_mundo: int(data_confirmed[data_confirmed['Province/State']=='French Guiana'][ultima_fecha_mundo])}, ignore_index=True)

data_confirmed.loc[data_confirmed['Country/Region'] == "Cote d'Ivoire", "Country/Region"] = 'Ivory Coast'
data_confirmed.loc[data_confirmed['Country/Region'] == 'Congo (Brazzaville)', "Country/Region"] = 'Republic of the Congo'
data_confirmed.loc[data_confirmed['Country/Region'] == 'Tanzania', "Country/Region"] = 'United Republic of Tanzania'
data_confirmed.loc[data_confirmed['Country/Region'] == 'Korea, South', "Country/Region"] = 'South Korea'

fecha_casos_m =data_confirmed.columns
fecha_casos_m= fecha_casos_m[4:]

d = data_confirmed.groupby(['Country/Region']).sum()

paises = data_confirmed['Country/Region'].drop_duplicates()
paises = sorted(paises)

data_mundo_mapa = pd.DataFrame({'Country': paises,'Casos':d[ultima_fecha_mundo]})



#casos recuperados
ultima_fecha_mundo_rec = recoveries_df.columns
ultima_fecha_mundo_rec= ultima_fecha_mundo_rec[-1]


recoveries_df.loc[recoveries_df['Country/Region'] == 'US', "Country/Region"] = 'United States of America'

recoveries_df.loc[recoveries_df['Country/Region'] == 'US', "Country/Region"] = 'United States of America'
recoveries_df.loc[recoveries_df['Country/Region'] == 'Congo (Kinshasa)', "Country/Region"] = 'Democratic Republic of the Congo'

#AGREGAR French Guiana COMO PAIS Y NO PROVICNCIA DE FRANCIA PERO SE SUMAR A EL TOTAL DE FRANCIA IGUAL
recoveries_df = recoveries_df.append({'Country/Region':'French Guiana',ultima_fecha_mundo_rec: int(data_confirmed[data_confirmed['Province/State']=='French Guiana'][ultima_fecha_mundo_rec])}, ignore_index=True)

recoveries_df.loc[recoveries_df['Country/Region'] == "Cote d'Ivoire", "Country/Region"] = 'Ivory Coast'
recoveries_df.loc[recoveries_df['Country/Region'] == 'Congo (Brazzaville)', "Country/Region"] = 'Republic of the Congo'
recoveries_df.loc[recoveries_df['Country/Region'] == 'Tanzania', "Country/Region"] = 'United Republic of Tanzania'
recoveries_df.loc[recoveries_df['Country/Region'] == 'Korea, South', "Country/Region"] = 'South Korea'


fecha_rec_m =recoveries_df.columns
fecha_rec_m= fecha_rec_m[4:]

d2 = recoveries_df.groupby(['Country/Region']).sum()

paises = recoveries_df['Country/Region'].drop_duplicates()
paises = sorted(paises)
v = d2[ultima_fecha_mundo_rec].apply(str)
data_mundo_mapa_rec = pd.DataFrame({'Country': paises,'Recuperados':v})

#casos fallecidos
ultima_fecha_fall_mundo = deaths_data.columns
ultima_fecha_fall_mundo= ultima_fecha_fall_mundo[-1]


deaths_data.loc[deaths_data['Country/Region'] == 'US', "Country/Region"] = 'United States of America'

deaths_data.loc[deaths_data['Country/Region'] == 'US', "Country/Region"] = 'United States of America'
deaths_data.loc[deaths_data['Country/Region'] == 'Congo (Kinshasa)', "Country/Region"] = 'Democratic Republic of the Congo'

#AGREGAR French Guiana COMO PAIS Y NO PROVICNCIA DE FRANCIA PERO SE SUMAR A EL TOTAL DE FRANCIA IGUAL
deaths_data = deaths_data.append({'Country/Region':'French Guiana',ultima_fecha_fall_mundo: int(data_confirmed[data_confirmed['Province/State']=='French Guiana'][ultima_fecha_fall_mundo])}, ignore_index=True)

deaths_data.loc[deaths_data['Country/Region'] == "Cote d'Ivoire", "Country/Region"] = 'Ivory Coast'
deaths_data.loc[deaths_data['Country/Region'] == 'Congo (Brazzaville)', "Country/Region"] = 'Republic of the Congo'
deaths_data.loc[deaths_data['Country/Region'] == 'Tanzania', "Country/Region"] = 'United Republic of Tanzania'
deaths_data.loc[deaths_data['Country/Region'] == 'Korea, South', "Country/Region"] = 'South Korea'
d2 = deaths_data.groupby(['Country/Region']).sum()


fecha_fall_m =deaths_data.columns
fecha_fall_m= fecha_fall_m[4:]

paises = deaths_data['Country/Region'].drop_duplicates()
paises = sorted(paises)

data_mundo_mapa_death = pd.DataFrame({'Country': paises,'Fallecidos':d2[ultima_fecha_fall_mundo]})

data_cd = pd.merge(data_mundo_mapa, data_mundo_mapa_death, on='Country')
data_cdr =  pd.merge(data_cd, data_mundo_mapa_rec, on='Country')



#grupo fallecidos

grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
fecha_grupo_fallecidos=grupo_fallecidos.columns[-1]

fecha_ge = grupo_fallecidos.columns[1:]

#figuras:


fig3 = px.pie(grupo_fallecidos, values=fecha_grupo_fallecidos, names='Grupo de edad')
fig3.update_traces(textposition='inside')
fig3.update_layout(uniformtext_minsize=9, uniformtext_mode='hide',clickmode ='event+select')

#grafico de barra grupo de edad
fig2 = go.Figure(go.Bar(
            x=grupo_fallecidos[fecha_grupo_fallecidos].values,
            y= grupo_fallecidos['Grupo de edad'],
            orientation='h'))
fig2.update_layout(clickmode ='event+select')


available_indicators = ['Regiones','Comunas','Pacientes COVID-19 en UCI por región','Mundo entero']


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}


colors2 = {
    'text': '#000000'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

     html.H1(
        children='Dash COVID-19 en Chile',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

 html.Div(children='Desarrollado por Rodrigo Ramirez', style={
        'textAlign': 'center',
        'color': colors2['text']
    }),
 html.Div(children='Contacto: ra.ramirez1993@gmail.com', style={
        'textAlign': 'center',
        'color': colors2['text']
    }),

    html.Div(children='Tipos de Busqueda', style={
        'color': colors['text'],
        'textAlign': 'center',
        'width': '49%','float': 'right', 'display': 'inline-block',  'padding': '0px 20px 20px 20px'
    }
),


      html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Regiones'
            ),
          
        ],style={'width': '49%','float': 'right', 'display': 'inline-block',  'padding': '0px 20px 20px 20px'}
      ),


    html.Div([
        dcc.Graph(
            id='basic-interactions',
            clickData={'points': [{'location': 'Chile'}]}
        )
    ], style={'width': '49%','float': 'left', 'display': 'inline-block', 'padding': '0 20'}),


    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
        dcc.Graph(id='z-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),



   html.H3(
        children='Personas fallecidas por grupos de edad',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'width': '49%', 'padding-top': '30px'

        }
    ),

    html.Div([
        dcc.Graph(id='grupo-time-series'),
    ], style={'display': 'inline-block','width': '49%', 'float': 'right'}),


    html.Div([
        dcc.Graph(id='grafic-bar-grupo-falle',
                 figure = fig2,
                 clickData={'points': [{'label': '<=39 '}]}
                 ),

    ],style={'display': 'inline-block', 'width': '49%'}),


   
])



#casos diarios
def create_time_series(dff,title,caso):
    if(dff.empty):
        return {
       
    }
    else:

        fecha =dff.fecha.iloc[-1]
        if(caso=='c'):
            color="#33CFA5"
        elif(caso=='f'):
            color="#F11013"
        else:
            color="#10CBF1"
        return {
            'data': [dict(
                x=dff.fecha,
                y=dff.casos,
                mode='lines+markers',
                line=dict(color=color)
            )],
            'layout': {
                'height': 225,
                'margin': {'l': 60, 'b': 30, 'r': 10, 't': 10},
                'annotations': [{
                    'x': 0, 'y': 0.90, 'xanchor': 'left', 'yanchor': 'bottom',
                    'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                    'align': 'left', 'bgcolor': '#33CFA5',
                     'text': title+' Actualizado: '+fecha

                }],

             

            }
        }



#grupos de edad

def create_time_series_grupo_edad(dff,title):
    if(dff.empty):
        return {
       
    }
    
    return {
            'data': [dict(
                x=dff.fecha,
                y=dff.casos,
                mode='lines+markers',
                line=dict(color='#F11013')
            )],
            'layout': {
                'height': 300,
                'margin': {'l': 50, 'b': 20, 'r': 30, 't': 100},
                'annotations': [{
                    'x': 0, 'y': 0.90, 'xanchor': 'left', 'yanchor': 'bottom',
                    'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                    'align': 'left', 'bgcolor': '#33CFA5',
                     'text': title+' Actualizado:'

                }],

             

            }

        }



@app.callback(
    dash.dependencies.Output('basic-interactions', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),])
def update_graph(value):

    if(value=='Comunas'):
        fig = go.Figure(go.Choroplethmapbox(geojson=geo_comunas, locations=data_comunas.Comuna, z=data_comunas.Casos,
                                    colorscale="Viridis", zmin=0, zmax=1000,
                                    featureidkey="properties.NOM_COM",
                                    colorbar = dict(thickness=20, ticklen=3),
                                    marker_opacity=0.2, marker_line_width=0, text=data_comunas['Poblacion'],
                                    hovertemplate = '<b>Región</b>: <b>'+data_comunas['Region']+'</b>'+
                                            '<br><b>Comuna </b>: %{properties.NOM_COM}<br>'+
                                            '<b>Población: </b>:%{text}<br>'+
                                            '<b>Casos </b>: %{z}<br>'
                                    
                                       
                                   ))
        fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=3,height=700,mapbox_center = {"lat": -30.0000000, "lon": -71.0000000},clickmode ='event+select')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    elif(value=='Mundo entero'):
        fig = go.Figure(go.Choroplethmapbox(geojson=geo_mundo, locations=data_cdr.Country, z=data_cdr.Casos,
                                    colorscale="Viridis", zmin=0, zmax=200000,
                                    featureidkey="properties.name",
                                    colorbar = dict(thickness=20, ticklen=3),
                                    marker_opacity=0.2, marker_line_width=0,  
                                    text=data_cdr['Fallecidos'],
                                      hovertemplate = '<b>País</b>: <b>'+data_cdr['Country']+'</b>'+
                                            '<br><b>Casos </b>: %{z}<br>'+
                                            '<b>Fallecidos: </b>:%{text}<br>'+
                                            '<b>Recuperados</b>: <b>'+data_cdr['Recuperados'] 
                                   
                                        ))


        fig.update_layout(mapbox_style="carto-positron",
                                mapbox_zoom=1,height=700,mapbox_center = {"lat": 0, "lon": 0},clickmode ='event+select')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    else:

        fig = go.Figure(go.Choroplethmapbox(geojson= geo_region   , locations=data_region.Region, z=data_region.Casos,
                                    colorscale="Viridis", zmin=0, zmax=6000,
                                    featureidkey="properties.NOM_REG",
                                    marker_opacity=0.2, marker_line_width=0))
        fig.update_layout(mapbox_style="carto-positron",
                          mapbox_zoom=3,height=700,mapbox_center = {"lat": -30.0000000, "lon": -71.0000000},clickmode ='event+select')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})




    return fig


#actualizacion graficos de linea

@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('basic-interactions', 'clickData'),
    dash.dependencies.Input('crossfilter-xaxis-column', 'value')])
def update_y_timeseries(clickData,value):
    casos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                     "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos totales'].iloc[0,1:].values})
    title='Casos Acumulados: Chile'
    caso='c'

    if(value=='Regiones'):
        country_name = clickData['points'][0]['location']
        prueba = casos_por_dia[casos_por_dia['Region']==country_name]

        if(prueba.empty):
            casos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                     "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos totales'].iloc[0,1:].values})
            title='Casos Acumulados: Chile'
            caso='c'
        else:
             casos_diarios_df = pd.DataFrame({"fecha": fecha_cd, "casos": casos_por_dia[casos_por_dia['Region']==country_name].iloc[0,1:].values})
             title='Casos Diarios: '+country_name
             caso='c'

    elif(value=='Comunas'):

        country_name = clickData['points'][0]['location']
   
        prueba2 = data_casos_por_comuna[data_casos_por_comuna['Comuna']==country_name]

        if(prueba2.empty):
            casos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                     "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos totales'].iloc[0,1:].values})
            title='Casos Acumulados: Chile'
            caso='c'
        else:
            casos_diarios_df = pd.DataFrame({"fecha": fecha_casos_comuna, "casos": data_casos_por_comuna[data_casos_por_comuna['Comuna']==country_name].iloc[0,5:].values})
            casos_diarios_df = casos_diarios_df.drop(casos_diarios_df.index[len(casos_diarios_df)-1])
            title='Casos Acumulados: '+country_name
    elif(value=='Chile'):
        casos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                     "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos totales'].iloc[0,1:].values})
        title='Casos Acumulados: Chile'
        caso='c'
    elif(value=='Pacientes COVID-19 en UCI por región'):
        country_name = clickData['points'][0]['location']
        prueba2 = hosp_region[hosp_region['Region']==country_name]

        if(prueba2.empty):
            casos_diarios_df = pd.DataFrame()
            title=[]
            caso=[]
        else:
            country_name = clickData['points'][0]['location']
            casos_diarios_df = pd.DataFrame({"fecha": fecha_hosp_region, 
                                         "casos": hosp_region[hosp_region['Region']==country_name].iloc[0,3:].values})
            title=' Pacientes COVID-19 en UCI: '+country_name
            caso='c'
    elif(value=='Mundo entero'):
        country_name = clickData['points'][0]['location']
        prueba2 = data_confirmed[data_confirmed['Country/Region']==country_name]
        if(prueba2.empty):
            casos_diarios_df = pd.DataFrame()
            title=[]
            caso=[]
        else:
            country_name = clickData['points'][0]['location']
            casos_diarios_df = pd.DataFrame({"fecha": fecha_casos_m, 
                                         "casos": data_confirmed[data_confirmed['Country/Region']==country_name].iloc[0,4:].values})
            title='Casos Acumulados: '+country_name
            caso='c'



    return create_time_series(casos_diarios_df,title,caso)



@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('basic-interactions', 'clickData'),
    dash.dependencies.Input('crossfilter-xaxis-column', 'value')])
def update_y_timeseries(clickData,value):
    fallecidos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                          "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Fallecidos'].iloc[0,1:].values})
    title='Fallecidos Acumulados: Chile'
    caso='f'

    if(value=='Regiones'):
        country_name = clickData['points'][0]['location']
        prueba = fallecidos_por_dia[fallecidos_por_dia['Region']==country_name]

        if(prueba.empty):
            fallecidos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                                  "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Fallecidos'].iloc[0,1:].values})
            title='Fallecidos Acumulados: Chile'
            caso='f'
        else:
            country_name = clickData['points'][0]['location']
            fallecidos_diarios_df = pd.DataFrame({"fecha": fecha_fd, "casos": fallecidos_por_dia[fallecidos_por_dia['Region']==country_name].iloc[0,1:].values})

            title='Fallecidos Diarios: '+country_name
            caso='f'

    elif(value=='Comunas'):
        country_name = clickData['points'][0]['location']
        prueba = data_fallecidos_por_comuna[data_fallecidos_por_comuna['Comuna']==country_name]
        if(prueba.empty):
            fallecidos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                          "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Fallecidos'].iloc[0,1:].values})
            title='Fallecidos Acumulados: Chile'
            caso='f'
        else:
            country_name = clickData['points'][0]['location']
            fallecidos_diarios_df = pd.DataFrame({"fecha": fecha_fallecidos_comuna, "casos": data_fallecidos_por_comuna[data_fallecidos_por_comuna['Comuna']==country_name].iloc[0,5:].values})
            title='Fallecidos Acumulados: '+country_name
            caso='f'
    elif(value=='Chile'):
        fallecidos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                          "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Fallecidos'].iloc[0,1:].values})
        title='Fallecidos Acumulados: Chile'
        caso='f'

    elif(value=='Pacientes COVID-19 en UCI por región'):
        fallecidos_diarios_df = pd.DataFrame()
        title=[]
        caso=[]

    elif(value=='Mundo entero'):
        country_name = clickData['points'][0]['location']
        prueba2 = data_confirmed[data_confirmed['Country/Region']==country_name]
        if(prueba2.empty):
            fallecidos_diarios_df = pd.DataFrame()
            title=[]
            caso=[]
        else:
            country_name = clickData['points'][0]['location']
            fallecidos_diarios_df = pd.DataFrame({"fecha": fecha_fall_m, 
                                         "casos": deaths_data[deaths_data['Country/Region']==country_name].iloc[0,4:].values})
            title='Fallecidos Acumulados: '+country_name
            caso='f'


    return create_time_series(fallecidos_diarios_df,title,caso)

@app.callback(
    dash.dependencies.Output('z-time-series', 'figure'),
    [dash.dependencies.Input('basic-interactions', 'clickData'),
    dash.dependencies.Input('crossfilter-xaxis-column', 'value')])
def update_y_timeseries(clickData,value):
    activos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                         "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos activos'].iloc[0,1:].values})
    caso='uci'
    title='Casos Activos Acumulados: Chile'

    if(value=='Regiones'):
        country_name = clickData['points'][0]['location']
        prueba = data_activos_region[data_activos_region['Region']==country_name]
        if(prueba.empty):
            activos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                         "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos activos'].iloc[0,1:].values})
            caso='uci'
            title='Casos Activos Acumulados: Chile'
        else:
            country_name = clickData['points'][0]['location']
            activos_diarios_df = pd.DataFrame({"fecha": fecha_activos_region, "casos": data_activos_region[data_activos_region['Region']==country_name].iloc[0,5:].values})

            #UCI_diarios_df = pd.DataFrame({"fecha": fecha_uci, "casos": grupo_uci_reg[grupo_uci_reg['Region']==country_name].iloc[0,3:].values})
            caso='uci'
            title='Casos Activos: '+country_name
    elif(value=='Comunas'):
        country_name = clickData['points'][0]['location']
        prueba = data_activos_por_comuna[data_activos_por_comuna['Comuna']==country_name]
        if(prueba.empty):
            activos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                         "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos activos'].iloc[0,1:].values})
            caso='uci'
            title='Casos Activos Acumulados: Chile'

        else:
            country_name = clickData['points'][0]['location']
            activos_diarios_df = pd.DataFrame({"fecha": fecha_activos_comuna, "casos": data_activos_por_comuna[data_activos_por_comuna['Comuna']==country_name].iloc[0,5:].values})
            caso='uci'
            title='Casos Activos: '+country_name
    elif(value=='Chile'):
        activos_diarios_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                         "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos activos'].iloc[0,1:].values})
        caso='uci'
        title='Casos Activos: Chile'

    elif(value=='Pacientes COVID-19 en UCI por región'):
        activos_diarios_df = pd.DataFrame()
        title=[]
        caso=[]
    elif(value=='Mundo entero'):
        country_name = clickData['points'][0]['location']
        prueba2 = data_confirmed[data_confirmed['Country/Region']==country_name]
        if(prueba2.empty):
            activos_diarios_df = pd.DataFrame()
            title=[]
            caso=[]
        else:
            country_name = clickData['points'][0]['location']
            activos_diarios_df = pd.DataFrame({"fecha": fecha_rec_m, 
                                         "casos": recoveries_df[recoveries_df['Country/Region']==country_name].iloc[0,4:].values})
            title='Recuperados Acumulados: '+country_name
            caso='uci'

    return create_time_series(activos_diarios_df,title,caso)


#GRUPOS DE EDAD


@app.callback(
    dash.dependencies.Output('grupo-time-series', 'figure'),
    [dash.dependencies.Input('grafic-bar-grupo-falle', 'clickData'),])
def update_y_timeseries_grupo_edad(clickData):
    grupo_edad = clickData['points'][0]['label']
    print(grupo_edad)
    prueba = grupo_fallecidos[grupo_fallecidos['Grupo de edad']==grupo_edad]
    if(prueba.empty):
        grupo_fallecidos_df = pd.DataFrame()
        title=[]
    else:
        grupo_edad = clickData['points'][0]['label']
        grupo_fallecidos_df = pd.DataFrame({"fecha": fecha_ge, 
                                         "casos": grupo_fallecidos[grupo_fallecidos['Grupo de edad']==grupo_edad].iloc[0,1:].values})
        title='Evolución de Casos de Fallecidos Grupo de Edad: '+grupo_edad
    return create_time_series_grupo_edad(grupo_fallecidos_df,title)



if __name__ == '__main__':
    app.run_server(debug=True)

#creado:rodrigo ramirez 
#contacto:ra.ramirez1993@gmail.com
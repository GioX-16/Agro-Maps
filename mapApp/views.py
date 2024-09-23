
import folium
import pandas as pd
from folium.plugins import MiniMap, HeatMap
from django.shortcuts import render

limites = {
    'managua': [[12.1364, -86.2514], [12.1464, -86.2714], [12.1664, -86.2314], [12.1364, -86.2514]],
    'masaya': [[11.9736, -86.0940], [11.9836, -86.1140], [11.9936, -86.0740], [11.9736, -86.0940]]
}

def obtener_datos_estudios():
    # Estudios por área/polígono
    estudios_limites = [
        {
            'limite': [[12.1364, -86.2514], [12.1464, -86.2714], [12.1664, -86.2314], [12.1364, -86.2514]],
            'ph': 6.5,
            'taxonomia': 'Franco Arenoso',
            'textura': 'Arenosa',
            'fecha': '2023-06-01',
            'ciudad': 'managua',
            'descripcion': 'Este suelo es principalmente arenoso, con buen drenaje pero baja retención de agua.',
            'recomendaciones': 'Agregar materia orgánica para mejorar la retención de humedad.'
        },
        {
            'limite': [[11.9736, -86.0940], [11.9836, -86.1140], [11.9936, -86.0740], [11.9736, -86.0940]],
            'ph': 7.2,
            'taxonomia': 'Arcilloso',
            'textura': 'Media',
            'fecha': '2023-06-15',
            'ciudad': 'masaya',
            'descripcion': 'Este suelo tiene un alto contenido de arcilla, lo que favorece la retención de agua.',
            'recomendaciones': 'Añadir compost para mejorar la aireación y estructura del suelo.'
        }
    ]
    return estudios_limites

def crear_mapa(ciudad):
    tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'
    atributos = 'Google Maps'
    m = folium.Map(location=[12.1, -86.2], zoom_start=14, tiles=tiles, attr=atributos)

    estudios_limites = obtener_datos_estudios()
    # Calcular los límites para ajustar el mapa según los estudios de la ciudad
    all_latitudes = []
    all_longitudes = []

    for estudio in estudios_limites:
        if estudio['ciudad'] == ciudad:  # Filtrar por ciudad
            for lat, lon in estudio['limite']:
                all_latitudes.append(lat)
                all_longitudes.append(lon)

    if all_latitudes and all_longitudes:
        bounds = [[min(all_latitudes), min(all_longitudes)],
                  [max(all_latitudes), max(all_longitudes)]]
        m.fit_bounds(bounds)

    return m


def color_por_ph(ph):
    if ph < 5.5:
        return 'red'
    elif 5.5 <= ph <= 6.5:
        return 'orange'
    elif 6.5 <= ph <= 7.5:
        return 'yellow'
    else:
        return 'green'

def agregar_estudios_limites(mapa, estudios_limites):

    for estudio in estudios_limites:
        limite = estudio['limite']
        color = color_por_ph(estudio['ph'])
        popup_content = f'''
        <h4>Estudio de Suelo (Límite)</h4>
        <b>pH:</b> {estudio['ph']}<br>
        <b>Taxonomía:</b> {estudio['taxonomia']}<br>
        <b>Textura:</b> {estudio['textura']}<br>
        <b>Fecha:</b> {estudio['fecha']}<br>
        '''
        folium.Polygon(limite, color=color, fill=True, fill_opacity=0.5, popup=popup_content).add_to(mapa)



def agregar_minimap(mapa):
    minimap = MiniMap(width=200, height=200, toggle_display=True)
    minimap.add_to(mapa)

def agregar_leyenda(mapa):
    legend_html = '''
     <div style="
     position: fixed; 
     bottom: 270px; right: 10px; width: 200px; height: 200px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px;
     border-radius: 10px;">
     <b>Niveles de pH del Suelo</b><br>
     <i style="background:red;color:white;">&nbsp;&nbsp;&nbsp;&nbsp;</i> Suelo muy ácido (pH < 5.5)<br>
     <i style="background:orange;color:white;">&nbsp;&nbsp;&nbsp;&nbsp;</i> Suelo moderadamente ácido (pH 5.5 - 6.5)<br>
     <i style="background:yellow;color:black;">&nbsp;&nbsp;&nbsp;&nbsp;</i> Suelo neutro (pH 6.5 - 7.5)<br>
     <i style="background:green;color:white;">&nbsp;&nbsp;&nbsp;&nbsp;</i> Suelo alcalino (pH > 7.5)<br>
     </div>
     '''
    mapa.get_root().html.add_child(folium.Element(legend_html))

def mapApp(request):
    ciudad = request.GET.get('ciudad', 'managua')
    fecha = request.GET.get('fecha', None)
    estudios_limites = obtener_datos_estudios()

    # Filtrar por ciudad
    estudios_limites_ciudad = [estudio for estudio in estudios_limites if estudio['ciudad'] == ciudad]

    # Si hay fecha, filtrar por fecha
    if fecha:
        estudios_limites_ciudad = [estudio for estudio in estudios_limites_ciudad if estudio['fecha'] == fecha]

    mapa = crear_mapa(ciudad)
    agregar_estudios_limites(mapa, estudios_limites_ciudad)
    agregar_minimap(mapa)
    agregar_leyenda(mapa)

    # Generar el array para el panel lateral
    datos_suelo = []
    for estudio in estudios_limites_ciudad:
        datos_suelo.append({
            'ph': estudio['ph'],
            'taxonomia': estudio['taxonomia'],
            'textura': estudio['textura'],
            'fecha': estudio['fecha'],
            'descripcion': estudio['descripcion'],
            'recomendaciones': estudio['recomendaciones']
        })

    map_html = mapa._repr_html_()

    return render(request, 'mostrarmapa.html', {'mapa': map_html, 'ciudad': ciudad, 'datos_suelo': datos_suelo})

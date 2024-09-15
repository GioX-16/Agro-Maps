import folium
from django.shortcuts import render

# Coordenadas para los límites de ejemplo de Managua y Masaya
limites_managua = [[12.1364, -86.2514], [12.1464, -86.2714], [12.1664, -86.2314], [12.1364, -86.2514]]
limites_masaya = [[11.9736, -86.0940], [11.9836, -86.1140], [11.9936, -86.0740], [11.9736, -86.0940]]

def mapApp(request):
    # Obtener la selección del usuario (Managua o Masaya)
    ciudad = request.GET.get('ciudad', 'managua')

    # Crear el mapa centrado en Nicaragua
    m = folium.Map(location=[12.1, -86.2], zoom_start=10)

    # Agregar el polígono correspondiente
    if ciudad == 'managua':
        folium.Polygon(limites_managua, color='blue', fill=True, fill_color='blue', fill_opacity=0.4).add_to(m)
    elif ciudad == 'masaya':
        folium.Polygon(limites_masaya, color='green', fill=True, fill_color='green', fill_opacity=0.4).add_to(m)

    # Convertir el mapa a HTML
    map_html = m._repr_html_()

    return render(request, 'mostrarmapa.html', {'mapa': map_html, 'ciudad': ciudad})

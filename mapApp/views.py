import folium
from django.shortcuts import render
from .models import SoilFertility

def mapa_fertilidad_view(request):
    # Crear un mapa centrado en Nicaragua
    m = folium.Map(location=[12.865416, -85.207229], zoom_start=7)

    # Extraer los datos de fertilidad del suelo desde la base de datos
    suelos = SoilFertility.objects.all()

    # Agregar cada punto al mapa
    for suelo in suelos:
        # Crear un popup con la información de fertilidad
        popup_content = f"""
        
        <strong>Nitrógeno (N):</strong> {suelo.macronutrients.nitrogen} mg/kg<br>
        <strong>Fósforo (P):</strong> {suelo.macronutrients.phosphorus} mg/kg<br>
        <strong>Potasio (K):</strong> {suelo.macronutrients.potassium} mg/kg<br>
        <strong>pH:</strong> {suelo.ph_level.ph_value}<br>
        <strong>Materia Orgánica:</strong> {suelo.organic_matter.percentage}%<br>
        """
        
        # Obtener la latitud y longitud
        latitud = suelo.location.latitude
        longitud = suelo.location.longitude
        
        # Añadir marcador al mapa
        folium.Marker(
            location=[latitud, longitud],  # Latitud y longitud
            popup=popup_content,
            icon=folium.Icon(color="green" if suelo.organic_matter.percentage > 3 else "red"),  # Color según nivel de materia orgánica
        ).add_to(m)

    # Convertir el mapa a HTML
    map_html = m._repr_html_()

    # Renderizar el mapa en la plantilla
    return render(request, 'mapa_fertilidad.html', {'mapa': map_html})

import folium
from django.shortcuts import render
from .models import SoilFertility

def mapa_fertilidad_view(request):
    # Crear un mapa centrado en Nicaragua
    m = folium.Map(location=[12.865416, -85.207229], zoom_start=7)

    # Crear grupos de capas para cada categoría
    macronutrientes_group = folium.FeatureGroup(name="Macronutrientes")
    micronutrientes_group = folium.FeatureGroup(name="Micronutrientes")
    physical_properties_group = folium.FeatureGroup(name="Propiedades físicas del suelo")
    ph_group = folium.FeatureGroup(name="pH del suelo")
    organic_matter_group = folium.FeatureGroup(name="Materia orgánica")

    # Extraer los datos de fertilidad del suelo desde la base de datos
    suelos = SoilFertility.objects.all()

    for suelo in suelos:
        # Crear contenido de popup para macronutrientes y micronutrientes
        nutrient_popup = f"""
        <strong>Macronutrientes:</strong><br>
        Nitrógeno (N): {suelo.macronutrients.nitrogen} mg/kg<br>
        Fósforo (P): {suelo.macronutrients.phosphorus} mg/kg<br>
        Potasio (K): {suelo.macronutrients.potassium} mg/kg<br><br>
        <strong>Micronutrientes:</strong><br>
        Hierro (Fe): {suelo.micronutrients.iron} mg/kg<br>
        Manganeso (Mn): {suelo.micronutrients.manganese} mg/kg<br>
        Zinc (Zn): {suelo.micronutrients.zinc} mg/kg
        """

        # Crear popups para propiedades físicas
        physical_popup = f"""
        <strong>Propiedades físicas del suelo:</strong><br>
        Textura: {suelo.physical_properties.texture}<br>
        Permeabilidad: {suelo.physical_properties.permeability} mm/h<br>
        Retención de agua: {suelo.physical_properties.water_retention} %<br>
        Drenaje: {suelo.physical_properties.drainage}
        """

        # pH del suelo (se mostrará al pasar el mouse sobre los marcadores)
        ph_popup = f"pH: {suelo.ph_level.ph_value}"

        # Materia orgánica
        organic_matter_popup = f"Materia Orgánica: {suelo.organic_matter.percentage}%"

        # Coordenadas del suelo
        latitud = suelo.location.latitude
        longitud = suelo.location.longitude

        # Marcadores para macronutrientes y micronutrientes
        folium.Marker(
            location=[latitud, longitud],
            popup=nutrient_popup,
            icon=folium.Icon(color="green", icon="leaf"),
        ).add_to(macronutrientes_group)

        # Marcadores para propiedades físicas
        folium.Marker(
            location=[latitud, longitud],
            popup=physical_popup,
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(physical_properties_group)

        # Marcadores para pH (aparecen al pasar el mouse)
        folium.CircleMarker(
            location=[latitud, longitud],
            radius=10,
            popup=ph_popup,
            color="purple",
            fill=True,
            fill_color="purple",
            fill_opacity=0.6
        ).add_to(ph_group)

        # Materia orgánica (como otra capa del mapa)
        folium.CircleMarker(
            location=[latitud, longitud],
            radius=8,
            popup=organic_matter_popup,
            color="brown",
            fill=True,
            fill_color="brown",
            fill_opacity=0.6
        ).add_to(organic_matter_group)

    # Agregar capas al mapa
    macronutrientes_group.add_to(m)
    physical_properties_group.add_to(m)
    ph_group.add_to(m)
    organic_matter_group.add_to(m)

    # Añadir control de capas para alternar entre ellas
    folium.LayerControl().add_to(m)

    # Convertir el mapa a HTML
    map_html = m._repr_html_()

    # Renderizar el mapa en la plantilla
    return render(request, 'mapa_fertilidad.html', {'mapa': map_html})

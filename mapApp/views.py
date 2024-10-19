import folium
from django.shortcuts import get_object_or_404, redirect, render
from .models import SoilFertility
from folium.plugins import MiniMap
from .forms import SoilFertilityForm, LocationForm

def register_soil_study(request):
    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        soil_form = SoilFertilityForm(request.POST)
        
        if location_form.is_valid() and soil_form.is_valid():
            location = location_form.save()
            soil_study = soil_form.save(commit=False)
            soil_study.location = location
            soil_study.registered_by = request.user  
            soil_study.save()
            return redirect('study') 
    
    else:
        location_form = LocationForm()
        soil_form = SoilFertilityForm()
    
    return render(request, 'form_study.html', {
        'location_form': location_form,
        'soil_form': soil_form
    })


def dashboard_view(request):
    return render(request, 'dashboard.html')

def study_view(request):
    estudios = SoilFertility.objects.all()
    return render(request, 'study.html',{'estudios':estudios})

def form_study_view(request):
    return render(request, 'form_study.html')


def mapa_fertilidad_view(request):
    # Crear un mapa centrado en Nicaragua
    mapa = folium.Map(location=[12.865416, -85.207229], zoom_start=7)

    # Crear grupos de capas para cada categoría
    grupoNutrientes = folium.FeatureGroup(name="Nutrientes")
    grupoPropiedadesFisicas = folium.FeatureGroup(name="Propiedades físicas del suelo")
    grupoPh = folium.FeatureGroup(name="pH del suelo")
    grupoMateriaOrganica = folium.FeatureGroup(name="Materia orgánica")

    # Extraer los datos de la base de datos
    bdRegistros = SoilFertility.objects.all()

    # Para cada registro dentro de la base de datos
    for bdRegistro in bdRegistros:

        #Almacenando el id del estudio
        idEstudio = f"""<h6 id='estudio-id' style= 'position: absolute;opacity: 0;'> {bdRegistro.id} </h6>"""

        # Almacenar Coordenadas del suelo del estudio
        latitud = bdRegistro.location.latitude
        longitud = bdRegistro.location.longitude

        ### Información básica de la parcela y región
        info_basica = f"""
        <strong>{bdRegistro.name}</strong><br>
        Región: {bdRegistro.region}<br>
        Fecha del estudio: {bdRegistro.date_of_study}<br><br>
        """

        ### Procesamiento de Nutrientes (Macronutrientes y Micronutrientes)

        # Almacenar y dar formato de Macronutrientes
        macronutrientesInfo = ""
        if hasattr(bdRegistro, 'macronutrients'):
            macronutrientesInfo = f"""
            <strong>Macronutrientes:</strong><br>
            Nitrógeno (N): {bdRegistro.macronutrients.nitrogen} mg/kg<br>
            Fósforo (P): {bdRegistro.macronutrients.phosphorus} mg/kg<br>
            Potasio (K): {bdRegistro.macronutrients.potassium} mg/kg<br>
            Calcio (Ca): {bdRegistro.macronutrients.calcium} mg/kg<br>
            Magnesio (Mg): {bdRegistro.macronutrients.magnesium} mg/kg<br>
            Azufre (S): {bdRegistro.macronutrients.sulfur} mg/kg<br><br>
            """

        # Almacenar y dar formato de Micronutrientes
        micronutrientesInfo = ""
        if hasattr(bdRegistro, 'micronutrients'):
            micronutrientesInfo = f"""
            <strong>Micronutrientes:</strong><br>
            Hierro (Fe): {bdRegistro.micronutrients.iron} mg/kg<br>
            Manganeso (Mn): {bdRegistro.micronutrients.manganese} mg/kg<br>
            Zinc (Zn): {bdRegistro.micronutrients.zinc} mg/kg<br>
            Cobre (Cu): {bdRegistro.micronutrients.copper} mg/kg<br>
            Boro (B): {bdRegistro.micronutrients.boron} mg/kg<br>
            Molibdeno (Mo): {bdRegistro.micronutrients.molybdenum} mg/kg<br>
            Cloro (Cl): {bdRegistro.micronutrients.chlorine} mg/kg<br>
            Níquel (Ni): {bdRegistro.micronutrients.nickel} mg/kg<br><br>
            """

        # Crear marcador con popup dinámico para Macronutrientes y Micronutrientes
        folium.Marker(
            location=[latitud, longitud],
            popup=folium.Popup(f'<a onclick="window.parent.printinfo(`{info_basica + macronutrientesInfo + micronutrientesInfo + idEstudio }`)">{info_basica + macronutrientesInfo + micronutrientesInfo } Ver más!</a>', max_width=200),
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(grupoNutrientes)

        
        ### Procesamiento de Propiedades Físicas del suelo

        # Almacenar y dar formato de las Propiedades Físicas del Suelo
        propiedadesFisicasInfo = ""
        if hasattr(bdRegistro, 'physical_properties'):
            propiedadesFisicasInfo = f"""
            <strong>Propiedades físicas del suelo:</strong><br>
            Textura: {bdRegistro.physical_properties.texture}<br>
            Estructura: {bdRegistro.physical_properties.structure}<br>
            Permeabilidad: {bdRegistro.physical_properties.permeability} mm/h<br>
            Retención de agua: {bdRegistro.physical_properties.water_retention}%<br>
            Densidad aparente: {bdRegistro.physical_properties.bulk_density} g/cm³<br>
            Drenaje: {bdRegistro.physical_properties.drainage}<br><br>
            """

        # Crear marcador con popup dinámico para Propiedades Físicas
        folium.Marker(
            location=[latitud, longitud],
            popup=folium.Popup(f'<a onclick="window.parent.printinfo(`{info_basica + propiedadesFisicasInfo + idEstudio }`)">{info_basica + propiedadesFisicasInfo} Ver más! </a>', max_width=200),
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(grupoPropiedadesFisicas)

        ### Procesamiento de pH del suelo
        phInfo = ""
        if hasattr(bdRegistro, 'phlevel'):
            phInfo = f"""
            <strong>pH del suelo:</strong><br>
            Valor de pH: {bdRegistro.phlevel.ph_value}<br><br>
            """

        # Crear marcador con popup dinámico para pH
        folium.Marker(
            location=[latitud, longitud],
            popup=folium.Popup(f'<a onclick="window.parent.printinfo(`{info_basica + phInfo + idEstudio }`)">{info_basica + phInfo} Ver más!</a>', max_width=200),
            icon=folium.Icon(color="purple", icon="info-sign")
        ).add_to(grupoPh)

        ### Procesamiento de Materia Orgánica

        materiaOrganicaInfo = ""
        if hasattr(bdRegistro, 'organic_matter'):
            materiaOrganicaInfo = f"""
            <strong>Materia orgánica:</strong><br>
            Porcentaje: {bdRegistro.organic_matter.percentage}%<br><br>
            """

        # Crear marcador con popup dinámico para Materia Orgánica
        folium.Marker(
            location=[latitud, longitud],
            popup=folium.Popup(f'<a onclick="window.parent.printinfo(`{info_basica + materiaOrganicaInfo + idEstudio }`)">{info_basica + materiaOrganicaInfo} Ver más!</a>', max_width=200),
            icon=folium.Icon(color="brown", icon="info-sign")
        ).add_to(grupoMateriaOrganica)

    # Añadir los grupos de capas al mapa
    grupoNutrientes.add_to(mapa)
    grupoPropiedadesFisicas.add_to(mapa)
    grupoPh.add_to(mapa)
    grupoMateriaOrganica.add_to(mapa)

    # Añadir control de capas para que el usuario pueda alternar entre ellas
    folium.LayerControl().add_to(mapa)

    # Añadir agregar minimapa
    minimap = MiniMap(width=200, height=200, toggle_display=True)
    minimap.add_to(mapa)

    # Convertir el mapa a HTML
    mapa_html = mapa._repr_html_()

    # Pasar el mapa a la plantilla
    return render(request, 'mapa.html', {'mapa': mapa_html})


def detalle_estudio(request, id):
    # Obtener el estudio por su ID
    estudio = get_object_or_404(SoilFertility, id=id)
    
    # Renderizar una plantilla con los detalles del estudio
    return render(request, 'chatbot.html', {'estudio': estudio})



def detalle_estudio(request, id):
    # Obtener el objeto SoilFertility por ID o devolver un error 404 si no existe
    soil_fertility = get_object_or_404(SoilFertility, id=id)

    contexto = {
        'soil_fertility': soil_fertility,
    }

    return render(request, 'chatbot.html', contexto)


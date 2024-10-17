from datetime import date
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agroMaps.settings')  
django.setup()

from django.contrib.auth.models import User
from mapApp.models import Location, SoilFertility, Macronutrients, Micronutrients, PhysicalProperties, OrganicMatter, PhLevel, SoilProfile, SoilSampling, AuthorizedUsers, ValidationLog

def fill_models():
    # Crear un usuario 
    user, created = User.objects.get_or_create(username='usuario_test', password='contraseña')

    location = Location.objects.create(
        latitude=12.34,
        longitude=56.78,
        geojson={"type": "Point", "coordinates": [56.78, 12.34]},
        properties={"description": "Ubicación de prueba"}
    )

    soil_fertility = SoilFertility.objects.create(
        name='Estudio de Suelo 1',
        date_of_study='2023-10-17',
        location=location,
        registered_by=user,
        soil_depth=30.0,
        relief='Plano',
        farm_name='Granja Ejemplo',
        crop_type='Trigo'
    )

    # Crear macronutrientes
    macronutrients = Macronutrients.objects.create(
        soil_fertility=soil_fertility,
        nitrogen=15.0,
        phosphorus=10.0,
        potassium=12.0,
        calcium=20.0,
        magnesium=5.0,
        sulfur=8.0
    )

    # Crear micronutrientes
    micronutrients = Micronutrients.objects.create(
        soil_fertility=soil_fertility,
        iron=3.0,
        manganese=1.0,
        zinc=0.5,
        copper=0.3,
        boron=0.1,
        molybdenum=0.02,
        chlorine=0.01,
        nickel=0.005
    )

    # Crear propiedades físicas
    physical_properties = PhysicalProperties.objects.create(
        soil_fertility=soil_fertility,
        texture='Arenoso',
        structure='Granulado',
        permeability=0.5,
        water_retention=0.4,
        bulk_density=1.2
    )

    # Crear materia orgánica
    organic_matter = OrganicMatter.objects.create(
        soil_fertility=soil_fertility,
        percentage=3.5
    )

    # Crear niveles de pH
    ph_level = PhLevel.objects.create(
        soil_fertility=soil_fertility,
        ph_value=6.5
    )

    # Crear un perfil de suelo
    soil_profile = SoilProfile.objects.create(
        soil_fertility=soil_fertility,
        horizon='A',
        depth_range='0-15 cm',
        texture='Arenoso',
        structure='Granulado',
        bulk_density=1.1
    )

    # Crear muestreo de suelo
    soil_sampling = SoilSampling.objects.create(
        soil_fertility=soil_fertility,
        date_of_sampling='2023-10-15',
        weather_conditions='Soleado',  
        sampling_pattern='Aleatorio',
        sample_type='Superficie',
        sub_samples_count=5,
        previous_soil_use='Cultivos anteriores',
        phone='1234567890', 
        reception_date=date.today()  
    )

    print("Modelos llenados correctamente.")

    if __name__ == '__main__':
        fill_models()
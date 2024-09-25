import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agroMaps.settings')
django.setup()

from mapApp.models import Location, SoilFertility, Macronutrients, Micronutrients, PhysicalProperties, OrganicMatter, PhLevel

def run():
    # Insertar datos en la tabla Location
    location = Location.objects.create(latitude=12.865416, longitude=-85.207229)

    # Insertar datos en la tabla SoilFertility
    soil_fertility = SoilFertility.objects.create(
        name="Parcela 1",
        region="Región Norte",
        date_of_study="2024-09-25",
        location=location
    )

    # Insertar datos en la tabla Macronutrients
    macronutrients = Macronutrients.objects.create(
        soil_fertility=soil_fertility,
        nitrogen=10.5,
        phosphorus=20.0,
        potassium=30.5,
        calcium=15.0,
        magnesium=5.0,
        sulfur=3.0
    )

    # Insertar datos en la tabla Micronutrients
    micronutrients = Micronutrients.objects.create(
        soil_fertility=soil_fertility,
        iron=0.5,
        manganese=0.3,
        zinc=0.2,
        copper=0.1,
        boron=0.05,
        molybdenum=0.01,
        chlorine=0.02,
        nickel=0.003
    )

    # Insertar datos en la tabla PhysicalProperties
    physical_properties = PhysicalProperties.objects.create(
        soil_fertility=soil_fertility,
        texture="Arenoso",
        structure="Granular",
        permeability=5.0,
        water_retention=30.0,
        bulk_density=1.2,
        drainage='well'
    )

    # Insertar datos en la tabla OrganicMatter
    organic_matter = OrganicMatter.objects.create(
        soil_fertility=soil_fertility,
        percentage=3.5
    )

    # Insertar datos en la tabla PhLevel
    ph_level = PhLevel.objects.create(
        soil_fertility=soil_fertility,
        ph_value=6.5
    )

    # Verificar que los datos se hayan guardado
    print("Datos insertados con éxito:")
    print("Location:", location)
    print("Soil Fertility:", soil_fertility)
    print("Macronutrients:", macronutrients)
    print("Micronutrients:", micronutrients)
    print("Physical Properties:", physical_properties)
    print("Organic Matter:", organic_matter)
    print("pH Level:", ph_level)

if __name__ == "__main__":
    run()

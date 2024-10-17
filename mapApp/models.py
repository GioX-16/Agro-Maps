from django.db import models
from django.contrib.auth.models import User  

class Location(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    latitude = models.FloatField()  # Latitud para punto
    longitude = models.FloatField()  # Longitud para punto
    geojson = models.JSONField(null=True, blank=True)  # Campo JSON para GeoJSON
    type = models.CharField(max_length=50, default='Point')  # Tipo de geometría
    properties = models.JSONField(null=True, blank=True)  # Propiedades adicionales

    def __str__(self):
        return f"Location ({self.latitude}, {self.longitude})"

class SoilFertility(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_of_study = models.DateField()
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    validated = models.BooleanField(default=False)
    soil_depth = models.FloatField(null=True, blank=True)
    relief = models.CharField(max_length=50, null=True, blank=True)
    soil_use = models.CharField(max_length=100, null=True, blank=True)
    sample_conditions = models.TextField(null=True, blank=True)
    number_of_subsamples = models.IntegerField(null=True, blank=True)
    sampling_type = models.CharField(max_length=50, null=True, blank=True)
    sampling_pattern = models.CharField(max_length=100, null=True, blank=True)
    farm_name = models.CharField(max_length=100, null=True, blank=True)
    lot_number = models.CharField(max_length=50, null=True, blank=True)
    establishment = models.CharField(max_length=100, null=True, blank=True)
    area = models.FloatField(null=True, blank=True)
    crop_type = models.CharField(max_length=100, null=True, blank=True)
    fertilization_history = models.TextField(null=True, blank=True)
    total_samples = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    # Características del suelo
    topography = models.CharField(max_length=50, null=True, blank=True)
    drainage = models.CharField(max_length=50, null=True, blank=True)

    # Análisis requeridos
    nitrogen_done = models.BooleanField(default=False)
    phosphorus_done = models.BooleanField(default=False)
    potassium_done = models.BooleanField(default=False)
    ph_done = models.BooleanField(default=False)
    cic_done = models.BooleanField(default=False)
    bases_done = models.BooleanField(default=False)
    micronutrients_done = models.BooleanField(default=False)

    # Análisis previos
    previous_analysis_url = models.URLField(max_length=255, null=True, blank=True)
    previous_comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Macronutrients(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.OneToOneField(SoilFertility, on_delete=models.CASCADE)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    calcium = models.FloatField()
    magnesium = models.FloatField()
    sulfur = models.FloatField()
    cation_exchange_capacity = models.FloatField(null=True, blank=True)
    carbonates = models.FloatField(null=True, blank=True)
    conductividad_electrica = models.FloatField(null=True, blank=True)  # Nuevo campo
    analysis_method = models.CharField(max_length=100, null=True, blank=True)

class Micronutrients(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.OneToOneField(SoilFertility, on_delete=models.CASCADE)
    iron = models.FloatField()
    manganese = models.FloatField()
    zinc = models.FloatField()
    copper = models.FloatField()
    boron = models.FloatField()
    molybdenum = models.FloatField()
    chlorine = models.FloatField()
    nickel = models.FloatField()
    analysis_method = models.CharField(max_length=100, null=True, blank=True)

class PhysicalProperties(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.OneToOneField(SoilFertility, on_delete=models.CASCADE)
    texture = models.CharField(max_length=50)
    structure = models.CharField(max_length=50)
    permeability = models.FloatField()
    water_retention = models.FloatField()
    bulk_density = models.FloatField()  # Densidad aparente
    real_density = models.FloatField(null=True, blank=True)  # Densidad real
    drainage = models.CharField(max_length=50, choices=[('very_poor', 'Very Poor'), ('poor', 'Poor'), ('moderate', 'Moderate'), ('well', 'Well')])
    carbonates = models.FloatField(null=True, blank=True)

class OrganicMatter(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.OneToOneField(SoilFertility, on_delete=models.CASCADE)
    percentage = models.FloatField()
    analysis_method = models.CharField(max_length=100, null=True, blank=True)

class PhLevel(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.OneToOneField(SoilFertility, on_delete=models.CASCADE)
    ph_value = models.FloatField()  # pH en agua destilada
    ph_kcl = models.FloatField(null=True, blank=True)  # pH en solución de KCl
    analysis_method = models.CharField(max_length=100, null=True, blank=True)

class SoilProfile(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.ForeignKey(SoilFertility, on_delete=models.CASCADE)
    horizon = models.CharField(max_length=5)
    depth_range = models.CharField(max_length=50)
    texture = models.CharField(max_length=50)
    structure = models.CharField(max_length=50)
    bulk_density = models.FloatField()  # Densidad aparente
    carbonates = models.FloatField(null=True, blank=True)
    activity_biological = models.CharField(max_length=50)

class SoilSampling(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.ForeignKey(SoilFertility, on_delete=models.CASCADE)
    date_of_sampling = models.DateField()
    weather_conditions = models.CharField(max_length=50, null=True, blank=True)
    sampling_pattern = models.CharField(max_length=100)
    sample_type = models.CharField(max_length=100)
    sub_samples_count = models.IntegerField()
    previous_soil_use = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    reception_date = models.DateField()

class AuthorizedUsers(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)

class ValidationLog(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.ForeignKey(SoilFertility, on_delete=models.CASCADE)
    authorized_user = models.ForeignKey(AuthorizedUsers, on_delete=models.CASCADE)
    validation_date = models.DateTimeField(auto_now_add=True)

class MiModelo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
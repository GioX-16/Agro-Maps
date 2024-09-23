from django.db import models

class Location(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Lat: {self.latitude}, Long: {self.longitude}"

class SoilFertility(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    name = models.CharField(max_length=100)  # Nombre del área o parcela
    region = models.CharField(max_length=100)  # Región del país (opcional)
    date_added = models.DateTimeField(auto_now_add=True)  # Fecha de ingreso al sistema
    date_of_study = models.DateField()  # Fecha del estudio de suelo
    location = models.OneToOneField(Location, on_delete=models.CASCADE)  # Relación uno a uno con Location

    def __str__(self):
        return self.name

class Macronutrients(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.OneToOneField(SoilFertility, on_delete=models.CASCADE, related_name='macronutrients')
    nitrogen = models.FloatField()  # Nitrógeno (N)
    phosphorus = models.FloatField()  # Fósforo (P)
    potassium = models.FloatField()  # Potasio (K)
    calcium = models.FloatField()  # Calcio (Ca)
    magnesium = models.FloatField()  # Magnesio (Mg)
    sulfur = models.FloatField()  # Azufre (S)

class Micronutrients(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.OneToOneField(SoilFertility, on_delete=models.CASCADE, related_name='micronutrients')
    iron = models.FloatField()  # Hierro (Fe)
    manganese = models.FloatField()  # Manganeso (Mn)
    zinc = models.FloatField()  # Zinc (Zn)
    copper = models.FloatField()  # Cobre (Cu)
    boron = models.FloatField()  # Boro (B)
    molybdenum = models.FloatField()  # Molibdeno (Mo)
    chlorine = models.FloatField()  # Cloro (Cl)
    nickel = models.FloatField()  # Níquel (Ni)

class PhysicalProperties(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.OneToOneField(SoilFertility, on_delete=models.CASCADE, related_name='physical_properties')
    texture = models.CharField(max_length=50)  # Textura del suelo
    structure = models.CharField(max_length=50)  # Estructura del suelo
    permeability = models.FloatField()  # Permeabilidad (en mm/hora)
    water_retention = models.FloatField()  # Capacidad de retención de agua (en porcentaje)
    bulk_density = models.FloatField()  # Densidad aparente del suelo
    drainage = models.CharField(max_length=50, choices=[
        ('very_poor', 'Muy pobremente drenado'),
        ('poor', 'Pobremente drenado'),
        ('moderate', 'Moderadamente drenado'),
        ('well', 'Bien drenado'),
    ])  # Drenaje del suelo

class OrganicMatter(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.OneToOneField(SoilFertility, on_delete=models.CASCADE, related_name='organic_matter')
    percentage = models.FloatField()  # Porcentaje de materia orgánica

class PhLevel(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    soil_fertility = models.OneToOneField(SoilFertility, on_delete=models.CASCADE, related_name='ph_level')
    ph_value = models.FloatField()  # Nivel de pH
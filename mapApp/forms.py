# forms.py
from django import forms
from .models import SoilFertility, Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'geojson', 'type', 'properties']

class SoilFertilityForm(forms.ModelForm):
    class Meta:
        model = SoilFertility
        fields = [
            'name', 'region', 'date_of_study', 'soil_depth', 'relief', 'soil_use',
            'sample_conditions', 'number_of_subsamples', 'sampling_type', 'sampling_pattern',
            'farm_name', 'lot_number', 'establishment', 'area', 'crop_type', 'fertilization_history',
            'total_samples', 'notes', 'topography', 'drainage', 'nitrogen_done', 'phosphorus_done',
            'potassium_done', 'ph_done', 'cic_done', 'bases_done', 'micronutrients_done',
            'previous_analysis_url', 'previous_comments'
        ]

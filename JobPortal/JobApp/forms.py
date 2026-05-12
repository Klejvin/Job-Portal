from django import forms
from .models import Job
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        # Shtuam 'category' në lista nëse e ke në model
        fields = [
            'title', 
            'company', 
            'category',  # Sigurohu që kjo fushë është në modelin tënd
            'salary', 
            'conditions', 
            'location', 
            'location_link', 
            'description'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pozicioni i punës'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emri i biznesit'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Psh. 60,000 lekë'}),
            'conditions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Psh. Full-time'}),
            'location_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Linku nga Google Maps'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Përshkruani detyrat dhe kërkesat...'}),
            
            # NDRYSHIMI KYÇ: Përdorim Select në vend të TextInput
            'location': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
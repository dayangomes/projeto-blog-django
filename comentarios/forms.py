from django import forms
from django.forms import ModelForm
from .models import Comentario
from django.forms.widgets import ClearableFileInput

class FormComentario(ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['comentario'].widget.attrs.update({'id': 'comentario-id'}) # Adiciona um id ao campo 'comentario' do formulário de comentários.

    def clean(self): # O clean é usado para validar os dados do formulário e retornar um erro caso necessário.
        data = self.cleaned_data

        nome = data.get('nome_comentario')
        email = data.get('email_comentario')
        comentario = data.get('comentario')

        if len(nome)<3:
            self.add_error(
                'nome_comentario', 
                'Nome precisa ter mais que 2 caracteres',
        )

        print(data) 

    class Meta:
        model = Comentario
        fields = ['nome_comentario', 'email_comentario', 'comentario']

        widgets = {
            'nome_comentario': forms.TextInput(attrs={
                'style': 'background-color: #f9f9f9; border: 3px solid #ddd; border-radius: 8px; border-color: #6d4a76;',
                'placeholder': 'Digite seu nome',
                'class': 'form-control',
            }),
            'email_comentario': forms.TextInput(attrs={
                'style': 'background-color: #f9f9f9; border: 3px solid #ddd; border-radius: 8px; border-color: #6d4a76;',
                'placeholder': 'Digite seu e-mail',
                'class': 'form-control',
            }),
            'comentario': forms.Textarea(attrs={
                'style': 'background-color: #f9f9f9; border: 3px solid #ddd; border-radius: 10px; border-color: #6d4a76;',
                'placeholder': 'Digite seu cometário',
                'class': 'form-control',
            }),
        }
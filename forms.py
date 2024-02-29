from wtforms import Form
from wtforms import StringField, EmailField, IntegerField, FloatField
from wtforms import validators

class UserForm(Form):
    id= IntegerField('id',[
                     validators.number_range(min=1, max=20, message='valor no valido')
    ])

    nombre = StringField('nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message='ingresa nombre valido')
    ])

    direccion = StringField('direccion', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message='ingresa direccion valido')
    ])

    telefono = StringField('telefono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message='ingresa telefono valido')
    ])

    email = EmailField('correo', [validators.Email(message='Ingrese un correo valido')])

    sueldo = FloatField('sueldo', [validators.number_range(min=1, max=20, message='valor no valido')])
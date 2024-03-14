from wtforms import Form
from wtforms import StringField, EmailField, IntegerField, FloatField, RadioField, SelectMultipleField
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

class UserForm2(Form):
    id= IntegerField('id',[
        validators.number_range(min=1, max=20, message='valor no valido')
    ])

    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message='ingresa nombre valido')
    ])

    direccion = StringField('Direccion', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message='ingresa direccion valido')
    ])

    telefono = StringField('Telefono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message='ingresa telefono valido')
    ])

    tamanio_pizza = RadioField('Tamano Pizza', choices=[('Chica', 'Chica $40'), 
                                                       ('Mediana', 'Mediana $80'), 
                                                       ('Grande', 'Grande $120')])
    
    ingredientes = SelectMultipleField('Ingredientes', choices=[('Jamon', 'Jamon $10'), 
                                                                ('Piña', 'Piña $10'), 
                                                                ('Champiñones', 'Champiñones $10')])
    
    cantidad = IntegerField('Cantidad',[
        validators.number_range(min=1, max=20, message='valor no valido')
    ])

    fecha = StringField('Fecha', [
        validators.DataRequired(message='El campo es requerido')
    ])

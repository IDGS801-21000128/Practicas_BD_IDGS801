from flask import Flask, render_template, request, flash, jsonify
import forms
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
from models import db
from models import Empleados, Cliente, DetalleCompra
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import extract

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

#@app.route("/")
#def index():
#    return render_template("index.html")

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    alumno_clase = forms.UserForm(request.form)
    nom = ""
    apa = ""
    ama = ""
    edad = None
    if request.method=='POST' and alumno_clase.validate():
        nom=alumno_clase.nombre.data
        
        apa=alumno_clase.apaterno.data
        ama=alumno_clase.amaterno.data
        edad=alumno_clase.edad.data
        print('Nombre: {}'.format(nom))
        print('apaterno: {}'.format(apa))
        print('amaterno: {}'.format(ama))

        mensaje = 'Bienvenido {}'.format(nom)
        flash(mensaje)
    return render_template("alumnos.html", form=alumno_clase, nom=nom, apa=apa, ama=ama, edad=edad)

@app.route('/index', methods=['GET', 'POST'])
def index():
    create_forms=forms.UserForm(request.form)
    if request.method=='POST':
        emp=Empleados(nombre=create_forms.nombre.data,
        direccion=create_forms.direccion.data,
        telefono=create_forms.telefono.data,
        email=create_forms.email.data,
        sueldo=create_forms.sueldo.data)
        
        db.session.add(emp)
        db.session.commit()
    return render_template('index.html', form=create_forms)

@app.route("/ABC_Completo", methods=["GET","POST"])
def ABCompleto():
    emp_form = forms.UserForm(request.form)
    empleado = Empleados.query.all()
    return render_template("ABC_Completo.html", empleado=empleado)

@app.route('/pizzeria', methods=['GET', 'POST'])
def pizzeria():
    create_forms=forms.UserForm2(request.form)
    return render_template('pizzeria.html', form=create_forms)

def traducir_dia(dia):
    dias_semana = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    return dias_semana.get(dia, "Día no válido")

@app.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    data = request.json  
    nombre = data['nombre']
    direccion = data['direccion']
    telefono = data['telefono']
    pedidos = data['pedidos']
    fecha = data['fecha']
    dia_semana = datetime.strptime(fecha, '%Y-%m-%d')
    dia_semana = dia_semana.strftime('%A')
    dia_semana = traducir_dia(dia_semana)
    cliente = Cliente(nombre=nombre, 
                    direccion=direccion, 
                    telefono=telefono)
    db.session.add(cliente)
    db.session.commit()

    id_cliente = cliente.idCliente

    for pedido in pedidos:
        detalle_compra = DetalleCompra(tamanio=pedido['tamaño'],
                                    ingredientes=pedido['ingredientes'],
                                    cantidad=pedido['cantidad'],
                                    subtotal=pedido['subtotal'],
                                    idCliente=id_cliente,
                                    fechaCompra = fecha,
                                    diaCompra = dia_semana)
        db.session.add(detalle_compra)
    db.session.commit()


@app.route('/get_mes', methods=['GET'])
def get_mes():
    numero_mes = int(request.args.get('mes'))

    fecha_str = '2023-03-13'
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
    # Obtener el día de la semana
    dia_semana = fecha.strftime('%A')
    print(dia_semana)

    resultados = db.session.query(
        Cliente.nombre,
        func.sum(DetalleCompra.subtotal).label('total')
    ).join(DetalleCompra).filter(
        extract('month', DetalleCompra.fechaCompra) == numero_mes
    ).group_by(Cliente.idCliente, Cliente.nombre).all()

    # Convertir resultados a una lista de diccionarios
    resultados_dict = [{'nombre': row.nombre, 'total': row.total} for row in resultados]
    print(resultados_dict[0])

    return jsonify(resultados_dict)

@app.route('/get_dia', methods=['GET'])
def get_dia():
    dia_semana = request.args.get('dia')

    resultados = db.session.query(
        Cliente.nombre,
        func.sum(DetalleCompra.subtotal).label('total')
    ).join(DetalleCompra).filter(
        DetalleCompra.diaCompra == dia_semana
    ).group_by(Cliente.idCliente, Cliente.nombre).all()

    resultados_dict = [{'nombre': row.nombre, 'total': row.total} for row in resultados]
    print(resultados_dict[0])

    return jsonify(resultados_dict)

if __name__ == "__main__":
    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run()     

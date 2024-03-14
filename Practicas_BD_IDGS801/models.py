from flask_sqlalchemy import SQLAlchemy

import datetime

db=SQLAlchemy()

class Empleados(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key = True)
    nombre=db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    telefono= db.Column(db.String(20))
    email=db.Column(db.String(50))
    sueldo=db.Column(db.Float)


class Cliente(db.Model):
    __tablename__ = 'cliente'
    idCliente = db.Column(db.Integer, primary_key = True)
    nombre=db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    telefono= db.Column(db.String(20))
    detalles_compra = db.relationship('DetalleCompra', backref='cliente', lazy=True)

class DetalleCompra(db.Model):
    __tablename__ = 'detalleCompra'
    idDetalleCompra = db.Column(db.Integer, primary_key = True)
    tamanio=db.Column(db.String(50))
    ingredientes=db.Column(db.String(50))
    cantidad= db.Column(db.String(20))
    subtotal= db.Column(db.Float)
    idCliente = db.Column(db.Integer, db.ForeignKey('cliente.idCliente'))
    fechaCompra=db.Column(db.String(20))
    diaCompra = db.Column(db.String(20))
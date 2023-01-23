#these are the routes we use to pass the information into the database

from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}


@api.route('/contacts', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    name = request.json['name'] # All of these are the key for the key-value pair dictionary
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Contact(name, email, phone_number, address, user_token = user_token) #'Contacts' comes from modules.py

    db.session.add(contact) #This is how we start the session to add the contact to our database
    db.session.commit() #This works like Github push, and to send the data we need to commit it

    response = contact_schema.dump(contact)
    return jsonify(response)
    #The last two lines of code will return the information that was just stored in the database. .dump and schema are part of 
    #marshmallow. Remember the contact_schema comes from 'models.py (vehicle_schema = VehicleSchema()
    #vehicles_schema = VehicleSchema(many = True)) This will show in insomnia and help us testing our API

@api.route('/contacts', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)

# Get single contact or endpoint
@api.route('/contacts/<id>', methods = ['GET']) #<id> . anything you put inisde the braces is a variable that we can call 
@token_required
def get_single_contact(current_user_token, id): #here we are passing the 'id' variable referenced in line 45
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)

# Update endpoint
@api.route('/contacts/<id>', methods = ['POST', 'PUT']) #Because it is an update we neewd to PUT and POST
@token_required
def update_contact(current_user_token, id): #here we are passing the 'id' variable referenced in line 53
    contact = Contact.query.get(id)
    contact.name = request.json['name']
    contact.email = request.json['email']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

# Delete Method or endpoint
@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)


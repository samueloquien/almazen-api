from flask import request, abort
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import api, db
from app.models.users import Users
from app.models.languages import Languages
from app.models.user_roles import UserRoles
from datetime import datetime
from http import HTTPStatus
import json

model_user = api.model('ModelUser', {
    'email': fields.String(attribute='user_email'),
    'password': fields.String(attribute=lambda x: x.user_password[:15]+'...'),
    'first_name': fields.String(attribute='user_first_name'),
    'last_name': fields.String(attribute='user_last_name'),
    'address': fields.String(attribute='user_address'),
    'country': fields.String(attribute='user_country'),
    'city': fields.String(attribute='user_city'),
    'language': fields.String(attribute=lambda x: Languages.query.filter_by(language_id=x.user_language_id).one().language_lang),
    })



@api.route('/user')
class UserEP(Resource):

    @api.marshal_with(model_user, envelope='user_profile')
    @jwt_required
    def get(self, *args, **kwargs):
        user_id = get_jwt_identity()
        try:
            u = Users.query.get(user_id)
            return u
        except:
            api.abort(message='No user found', code=HTTPStatus.FORBIDDEN)

    @jwt_required
    def delete(self, *args, **kwargs):
        user_id = get_jwt_identity()
        try:
            u = Users.query.get(user_id)
            db.session.delete(u)
            db.session.commit()
        except:
            api.abort(message='No user found', code=HTTPStatus.FORBIDDEN)
        return {'users': [{'id': u.user_id,'email':u.user_email} for u in Users.query.all()] }

    def post(self, *args, **kwargs):
        email = request.json.get('email')
        password = request.json.get('password')
        if email is None or password is None:
            api.abort(message='Missing email and/or password. Both required.', code=HTTPStatus.FORBIDDEN)
        if Users.query.filter_by(user_email=email).first() is not None:
            api.abort(message='User already exists.', code=HTTPStatus.FORBIDDEN)
        lang_id = db.session().query(Languages).filter(Languages.language_lang=='en-US').one().language_id
        role = UserRoles.query.filter_by(user_role='user').one().user_role_id
        user = Users(user_email=email, user_language_id=lang_id, user_create_datetime=datetime.now(), user_role=role)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        #return jsonify({ 'email': user.user_email }), 200#, {'Location': url_for('get_user', id = user.id, _external = True)}
        return { 'email': user.user_email }, 201

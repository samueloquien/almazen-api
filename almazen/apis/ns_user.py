from flask import request, abort
from flask_restx import Namespace, Resource, fields
from datetime import datetime
from http import HTTPStatus
import json
from flask_jwt_extended import jwt_required, jwt_optional, get_raw_jwt, get_jwt_identity, create_access_token

from almazen.models import Users, Languages, UserRoles
from almazen.db import db

api = Namespace('user', description='Endpoint for user management')

model_user = api.model('ModelUser', {
    'email': fields.String(attribute='user_email'),
    'password': fields.String(attribute=lambda x: x.user_password[:15]+'...'),
    'first_name': fields.String(attribute='user_first_name'),
    'last_name': fields.String(attribute='user_last_name'),
    'address': fields.String(attribute='user_address'),
    'country': fields.String(attribute='user_country'),
    'city': fields.String(attribute='user_city'),
    'language': fields.String(attribute=lambda x: Languages.query.filter_by(language_id=x.user_language_id).one().language_lang),
    'role': fields.String(attribute=lambda x: UserRoles.query.filter_by(user_role_id=x.user_role_id).one().user_role)
    })


@api.route('/user')
class UserEP(Resource):

    # Get user profile
    @jwt_required
    @api.marshal_with(model_user, envelope='user_profile')
    def get(self, *args, **kwargs):
        user_id = get_jwt_identity()
        u = Users.query.get(user_id)
        if u is None:
            api.abort(message='No user found', code=HTTPStatus.FORBIDDEN)
        api.logger.info('email:'+u.user_email)
        return u

    # Delete user
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

    # Create user
    @jwt_optional
    def post(self, *args, **kwargs):
        email = request.json.get('email')
        password = request.json.get('password')
        if email is None or password is None:
            api.abort(message='Missing email and/or password. Both required.', code=HTTPStatus.FORBIDDEN)
        if Users.query.filter_by(user_email=email).first() is not None:
            api.abort(message='User already exists.', code=HTTPStatus.FORBIDDEN)
        lang_id = db.session().query(Languages).filter(Languages.language_lang=='en-US').one().language_id

        # Set the role of the new user. It will be 'user' by default and can only be explicitly set
        # if the caller is an authenticated admin.
        role = 'user'
        try:
            if get_jwt_identity() is not None and get_jwt_claims()['role'] == 'admin':
                if request.json.get('role') is not None:
                    role = request.json.get('role')
        except:
            role = 'user'
        role_id = UserRoles.query.filter_by(user_role=role).one().user_role_id

        user = Users(user_email=email, user_language_id=lang_id, user_create_datetime=datetime.now(), user_role_id=role_id)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return {'access_token': create_access_token(user.user_id)}, 201

    '''
    Edit any user profile parameter. Request body may contain any subgroup
    of this list: [email, password, first_name, last_name, address, country,
    city, language, role] (or all of them). Some verification is performed
    before writing to the DB, though:
    - If editing password, the old password must be provided.
    - If editing language or role, the values must be among those defined
      in the languages and user_roles tables, respectively.
    If any of these verifications fail, nothing is writen to the DB and the
    request is aborted.
    '''
    @api.marshal_with(model_user, envelope='user_profile')
    @jwt_required
    def patch(self, *args, **kwargs):
        try:
            api.logger.info('Editing user profile')


            props = '''email password first_name last_name 
            address country city language role'''
            props = props.split()
            new_props = {}
            for prop in props:
                new_val = request.json.get(prop)
                if new_val is not None:
                    new_props[prop] = new_val
            api.logger.info('props:' + str(props))
            api.logger.info('new_props:' + str(new_props))
            api.logger.info('request.json:' + str(request.json))

            user_id = get_jwt_identity()
            u = Users.query.get(user_id)

            # Validate password update
            if 'password' in new_props:
                old_password = request.json.get('old_password')
                if old_password is not None:
                    if not user.verify_password(old_password):
                        api.abort(message='Invalid old password.', code=HTTPStatus.UNAUTHORIZED)
            # Validate language
            if 'language' in new_props:
                lang_id = Languages.query.filter_by(language_lang=new_props['language']).one().language_id
                if lang_id is None:
                    api.abort(message='Invalid new language.', code=HTTPStatus.FORBIDDEN)
            # Validate user role
            if 'role' in new_props:
                role_id = UserRoles.query.filter_by(user_role=new_props['role']).one().user_role_id
                if role_id is None:
                    api.abort(message='Invalid new user role.', code=HTTPStatus.FORBIDDEN)

            # Set values
            if 'email' in new_props:
                u.user_email = new_props['email']
            if 'password' in new_props:
                u.hash_password(new_props['password'])
            if 'first_name' in new_props:
                u.user_first_name = new_props['first_name']
            if 'last_name' in new_props:
                u.user_last_name = new_props['last_name']
            if 'address' in new_props:
                u.user_address = new_props['address']
            if 'country' in new_props:
                u.user_country = new_props['country']
            if 'city' in new_props:
                u.user_city = new_props['city']
            if 'language' in new_props:
                u.user_language_id = lang_id
            if 'role' in new_props:
                u.user_role_id = role_id

            db.session.commit()

            return u
        except:
            print('Unhandled exception during call to patch')
            return None


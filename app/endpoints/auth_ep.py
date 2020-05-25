from flask import request, abort
from flask_restx import Resource, fields
from flask_jwt_extended import create_access_token
from app import app, api, db
from app.models.users import Users
from app.models.languages import Languages
from datetime import datetime
from http import HTTPStatus
import json

model_login = api.model('ModelLogin', {
    'access_token': fields.String(),
    })


@api.route('/auth/login')
class AuthLoginEP(Resource):

    @api.marshal_with(model_login)
    def post(self, *args, **kwargs):
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            api.abort(message='Missing username and/or password. Both required.', code=HTTPStatus.UNAUTHORIZED)
        user = Users.query.filter_by(user_email=username).first()
        if user is None:
            api.abort(message='Username doesn\'t exist.', code=HTTPStatus.UNAUTHORIZED)
        if not user.verify_password(password):
            api.abort(message='Invalid username/password.', code=HTTPStatus.UNAUTHORIZED)
        return {'access_token': create_access_token(user.user_id)}

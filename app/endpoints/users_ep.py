from flask import request, abort
from flask_restx import Resource, fields
from app import api, db
from app.models.users import Users
from app.models.languages import Languages
from datetime import datetime
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
    def get(self, *args, **kwargs):
        user_email = request.args.get('email')
        try:
            u = Users.query.filter_by(user_email=user_email).one()
            return u
        except:
            api.logger.warn("no user found with email"+user_email)
            abort(404)

    def delete(self, *args, **kwargs):
        email = request.json.get('email')
        u = Users.query.filter_by(user_email=email).one()
        db.session.delete(u)
        db.session.commit()
        return {'users': [u.user_email for u in Users.query.all()] }

    def post(self, *args, **kwargs):
        email = request.json.get('email')
        password = request.json.get('password')
        if email is None or password is None:
            abort(404)#Response('Missing arguments email and password')) # missing arguments
        if Users.query.filter_by(user_email=email).first() is not None:
            abort(404)#Response('User {} already exists.'.format(email))) # existing user
        lang_id = db.session().query(Languages).filter(Languages.language_lang=='en-US').one().language_id
        user = Users(user_email=email, user_language_id=lang_id, user_create_datetime=datetime.now())
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        #return jsonify({ 'email': user.user_email }), 200#, {'Location': url_for('get_user', id = user.id, _external = True)}
        return { 'email': user.user_email }

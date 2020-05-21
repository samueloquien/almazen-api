from flask import request, abort
from flask_restx import Resource
from app import api, db
from app.models.users import Users
from app.models.languages import Languages
from datetime import datetime
import json

@api.route('/users')
class UsersEP(Resource):

    def get(self, *args, **kwargs):
        users = db.session().query(Users).all()
        if not users:
            return 'No users defined'
        return ', '.join( [u.user_email for u in users] )

    def delete(self, *args, **kwargs):
        email = request.json.get('email')
        u = Users.query.filter_by(user_email=email).one()
        db.session.delete(u)
        db.session.commit()
        return ', '.join( [u.user_email for u in Users.query.all()] )

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
        return json.dumps({ 'email': user.user_email })

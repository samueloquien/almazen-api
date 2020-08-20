from flask_jwt_extended import JWTManager #, jwt_optional, jwt_required, get_jwt_identity, create_access_token, get_jwt_claims
from almazen.models import Users, UserRoles

jwt = JWTManager()

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    role_id = Users.query.get(identity).user_role_id
    role = UserRoles.query.get(role_id).user_role
    return {'role': role}

# # from app import db, ma
# from app.models import User 


# class UserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#        fields = ("id", "email", "name", "role")
#        load_only = ("password",)

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)
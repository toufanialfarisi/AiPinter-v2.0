from aipinter.models import User
from werkzeug.security import check_password_hash

user = User.query.filter_by(username='toufani1515').first()
print(user)
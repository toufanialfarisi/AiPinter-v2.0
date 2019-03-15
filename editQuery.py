from aipinter.models import User, ImageFile
from werkzeug.security import check_password_hash
from aipinter import db

user = User.query.filter_by(username='toufani1515').first()
print(user)

# img = db.session.query(ImageFile.id)
# for i in img:
#     u = ImageFile.query.get(i)
#     db.session.delete(u)
#     db.session.commit()

img = ImageFile.query.filter_by(id=1).first()
a = img.image_file
print(a.split('/')[-2:])


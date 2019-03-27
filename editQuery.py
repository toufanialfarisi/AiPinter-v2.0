from aipinter.models import User, ImageFile, Forecasting
from werkzeug.security import check_password_hash
from aipinter import db

# user = User.query.filter_by(username='toufani1515').first()
# print(user)

# img = db.session.query(ImageFile.id)
# for i in img:
#     u = ImageFile.query.get(i)
#     db.session.delete(u)
#     db.session.commit()

# img = ImageFile.query.filter_by(id=1).first()
# a = img.image_file
# print(a.split('/')[-2:])

# fcast = Forecasting(23.2 ,23.3, 32.3, 32., 23.4, 42.3, 12.4, 42.3, 34.3, 21.3)
# try:
#     db.session.add(fcast)
#     db.session.commit()
# except Exception as e:
#     print('error broo !!')

a = '2'
print(float(a), 'type : ', type(a))

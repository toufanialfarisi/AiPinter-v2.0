from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField, SubmitField, FloatField
from flask_wtf import FlaskForm
import wtforms


class ForecastingForm(FlaskForm, wtforms.Form):
    suhu_minimum  = wtforms.FloatField('Suhu Minimum', validators=[DataRequired()])
    suhu_maksimum = wtforms.FloatField('Suhu Maksimum', validators=[DataRequired()])
    suhu_rata_rata = wtforms.FloatField('Suhu rata-rata', validators=[DataRequired()])
    kelembapan_rata2x = wtforms.FloatField('Kelembapan rata-rata', validators=[DataRequired()])
    curah_hujan = wtforms.FloatField('Curah hujan', validators=[DataRequired()])
    lama_penyinaran = wtforms.FloatField('Lama Penyinaran', validators=[DataRequired()])
    kecepatan_angin_rata2x = wtforms.FloatField('Kecepatan angin rata-rata', validators=[DataRequired()])
    arah_angin_terbanyak = wtforms.FloatField('Arah angin terbanyak', validators=[DataRequired()])
    kecepatan_angin_terbesar = wtforms.FloatField('Kecepatan angin terbesar', validators=[DataRequired()])
    arah_angin_saat_max = wtforms.FloatField('Arah angin saat kecepatan maksimum', validators=[DataRequired()])
    # submit = SubmitField('Predict')

    def save(self, data):
        self.populate_obj(data)
        
    
    # def __repr__(self):
    #     return f'{self.save(data)} data is added'
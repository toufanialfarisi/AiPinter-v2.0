# forecasting/views.py
# dataset_path = 'dataset/data_konsul_3.csv

from flask import Blueprint, request, render_template, redirect, flash, url_for
from aipinter.forecasting.forms import ForecastingForm
from aipinter.models import Forecasting
from aipinter import db 
from sklearn.tree import DecisionTreeClassifier
import pickle
import numpy as np 

forecasting = Blueprint('forecasting', __name__)

def printkan(data):
    print(data)

@forecasting.route('/forecasting', methods=['GET', 'POST'])
def fcasting():
    form = ForecastingForm()
    if request.method == 'POST' and form.validate():
        model = Forecasting()
        # form.save(model)
        form.populate_obj(model)
        db.session.add(model)
        db.session.commit()

        suhuMinimum = form.suhu_minimum.data
        # suhuMinimum = float(suhuMinimum)

        suhuMaksimum = form.suhu_maksimum.data
        # suhuMaksimum = float(suhuMaksimum)

        suhuRataRata = form.suhu_rata_rata.data
        # suhuRataRata = float(suhuRataRata)

        kelembaparanRata2 = form.kelembapan_rata2x.data
        # kelembaparanRata2 = float(kelembaparanRata2)

        curahHujan = form.curah_hujan.data
        # curahHujan = float(curahHujan)

        lamaPenyinaran = form.lama_penyinaran.data
        # lamaPenyinaran = float(lamaPenyinaran)

        kecepatanAngin = form.kecepatan_angin_rata2x.data
        kecepatanAngin_ = int(kecepatanAngin)
        # kecepatanAngin = float(kecepatanAngin)

        arahAnginTerbanyak = form.arah_angin_terbanyak.data
        arahAnginTerbanyak_ = int(arahAnginTerbanyak)
        arahAnginTerbanyak = float(arahAnginTerbanyak)

        kecepatanAnginTerbesar = form.kecepatan_angin_terbesar.data
        kecepatanAnginTerbesar_ = int(kecepatanAnginTerbesar)
        # kecepatanAngin = float(kecepatanAngin)

        arahAnginMax = form.arah_angin_saat_max.data
        arahAnginMax_ = int(arahAnginMax)
        arahAnginMax = float(arahAnginMax)

        pred_con = [suhuMinimum, suhuMaksimum, suhuRataRata,
        kelembaparanRata2, curahHujan, lamaPenyinaran, kecepatanAngin,
        arahAnginTerbanyak, kecepatanAnginTerbesar, arahAnginMax]

        # db.session.add(fcast)
        # db.session.commit()

        # try:
        model_path = 'aipinter/dataset/model_tree.ckp'
        model = DecisionTreeClassifier()
        model = pickle.load(open(model_path, 'rb'))
        
        val = np.array(pred_con)
        val = np.expand_dims(val, 0)
        pred = model.predict(val)[0]
        if pred == 0:
            res = 'Not Flooding'
        elif pred == 1:
            res = 'Flooding'
        else :
            res  = ''
        
        flash('Prediction: {} ({})'.format(res, pred), 'success')

        # except Exception as e:
        #     print('engine error')



        
        # return redirect(url_for('forecasting.fcasting'))
    return render_template('forecasting.html', form=form)


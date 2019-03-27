# forecasting/views.py
# dataset_path = 'dataset/data_konsul_3.csv

from flask import Blueprint, request, render_template, redirect, flash, url_for, jsonify
from aipinter.forecasting.forms import ForecastingForm
from aipinter.models import Forecasting
from aipinter import db 
from aipinter.schema import ForecastingSchema
from flask_login import login_required
from sklearn.tree import DecisionTreeClassifier
import pickle
import numpy as np 

forecasting = Blueprint('forecasting', __name__)

def printkan(data):
    print(data)

@forecasting.route('/forecasting', methods=['GET', 'POST'])
@login_required
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



        view = Forecasting.query.all()
        return redirect(url_for('forecasting.forecasting_list'))
    return render_template('forecasting.html', form=form)

@forecasting.route('/forecasting/list')
@login_required
def forecasting_list():
    view = Forecasting.query.all()
    try:
        view_one = Forecasting.query.first()
        return render_template('list_forecasting.html', container=view.id)
    except:
        flash('No Data available', 'danger')
        return render_template('list_forecasting.html', container='')
    # return render_template('list_forecasting.html', container=view)

@forecasting.route('/forecasting/delete/<int:id>')
@login_required
def fcast_delete(id):

    del_ocr = Forecasting.query.filter_by(id=id).first()
    db.session.delete(del_ocr)
    db.session.commit()
    return redirect(url_for('forecasting.forecasting_list'))



@forecasting.route('/forecasting/api', methods=['POST', 'GET'])
@login_required
def api():
    fcast = Forecasting.query.all()
    fcast_schema = ForecastingSchema(many=True)
    output = fcast_schema.dump(fcast).data
    return jsonify(output)


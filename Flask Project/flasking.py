# cmd den 
# pip install flask
# pip install suds-jurko


from flask import *
from functools import wraps
from datetime import datetime
from suds.client import Client
import time
import sqlite3 as sql

WSDL_URL="https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL"
client=Client(WSDL_URL)

def tcKimlikDogrula(params):
    try:
        return  client.service.TCKimlikNoDogrula(**params)
    except Exception as e:
        return False

# {{url_for('static', filename='newindex.css')}}
# <form action="." method="POST"></form>

app = Flask(__name__)

app.secret_key = '_5#y2L"F4Q8z'

def login_required(wrp):
    @wraps(wrp)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return wrp(*args, **kwargs)
        else:
            flash('You need to login first!',category='error')
            return redirect(url_for('login_form'))
    return wrap

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out','info')
    time.sleep(0.5)
    return redirect (url_for('login_form'))

@app.route('/')
def my_form():
    return redirect(url_for("login_form"))

@app.route('/login')
def login_form():
    return render_template("ilk.html")

@app.route('/config')
@login_required
def config_form():
    return render_template("son.html")


@app.route('/login', methods=['GET','POST'])
def login_form_post():
    if (request.method == 'POST'):
        tcid = request.form['TC_ID']
        name = request.form['name']
        surname = request.form['surname']
        yob = request.form['yob']

        name.upper()
        surname.upper()

        x = datetime.now()
        
        args={
            "TCKimlikNo":tcid,
            "Ad":name,
            "Soyad":surname,
            "DogumYili":yob,
        }

        if tcKimlikDogrula(args):

            session['logged_in'] = True
            giris = "DOĞRU"
            f = open ("log.txt", "a")
            f.write("TC: {}\n".format(tcid))
            f.write("isim: {}\n".format(name))
            f.write("soyisim: {}\n".format(surname))
            f.write("yıl: {}\n".format(yob))
            f.write(f"Giriş Bilgileri: {giris}, Giriş Saati: {x}\n")
            f.write("\n-\n\n")
            f.close()
            giris = "boş"
            flash('Logged In',category='error')
            return redirect(url_for("config_form"))
        else:

            f = open ("log.txt", "a")
            giris = "YANLIŞ"
            f.write("TC: {}\n".format(tcid))
            f.write("isim: {}\n".format(name))
            f.write("soyisim: {}\n".format(surname))
            f.write("yıl: {}\n".format(yob))
            f.write(f"Giriş Bilgileri: {giris}, Giriş Saati: {x}\n")
            f.write("\n-\n\n")
            f.close()
            giris = "boş"
            flash('Wrong credentials!',category='error')
            return redirect(url_for("login_form"))
            

@app.route('/config', methods=['POST'])
def config_form_post():

    if request.form['butonsave'] == 'save':
        subnet = request.form['subnet']
        netmask = request.form['netmask']
        gateway = request.form['gateway']
        dnsserver = request.form['dnsserver']
        startip = request.form['startip']
        endip = request.form['endip']
        
        f = open("config.conf", "w")
        f.write("subnet: {}\n".format(subnet))
        f.write("netmask: {}\n".format(netmask))
        f.write("gateway: {}\n".format(gateway))
        f.write("dnsserver: {}\n".format(dnsserver))
        f.write("startip: {}\n".format(startip))
        f.write("endip: {}\n".format(endip))
        f.close()

        flash ('Configuration Success!',category='success')
        return redirect(url_for("config_form"))

    elif request.form['butonsave'] == 'logout':

        return redirect(url_for("logout"))



if __name__ == '__main__':
    app.run(host="localhost", port=5172, debug=True)

    # host="localhost", port=5130, debug=True
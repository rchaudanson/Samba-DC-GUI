from flask import Flask, render_template, request, redirect, url_for, flash
from flask_table import Table, Col
from bs4 import BeautifulSoup
import getpass
import ldb
import os
import csv
from samba.auth import system_session
from samba.credentials import Credentials
from samba.dcerpc import security
from samba.dcerpc.security import dom_sid
from samba.ndr import ndr_pack, ndr_unpack
from samba.param import LoadParm
from samba.samdb import SamDB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JSkjhdde45fr5LKSlKJSDd45ef4frgj54E10'


UPLOAD_FOLDER = 'Upload/'


lp = LoadParm()
creds = Credentials()
creds.guess(lp)
samdb = SamDB(url='/var/lib/samba/private/sam.ldb', session_info=system_session(),credentials=creds, lp=lp)


#ROUTE FLASK

#Route index
@app.route('/')
def index():
    return render_template('index.html')
    
#Route import ( importation CSV )    
@app.route('/import', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        filename = (file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        with open(os.path.join(UPLOAD_FOLDER, filename)) as fichier_csv:
           reader = csv.reader(fichier_csv, delimiter=',')
           for ligne in reader:
              #print(ligne[1])
              samdb.newuser(username=(ligne[0]),password=(ligne[1]),force_password_change_at_next_login_req=True,mailaddress=(ligne[2]))
              
           return redirect(url_for('liste'))
    return redirect(url_for('liste'))


#Route delete
@app.route('/delete')
def test():
    if request.method == 'GET':
        login1 = request.args.get('login')
        

        if not login1:
            flash('Title is required!')
        else:
            samdb.deleteuser(username=request.args.get('login'))
            return redirect(url_for('liste'))

    return render_template('delete.html')


#Route create
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['Nom']
        content = request.form['Prenom']

        if not title:
            flash('Title is required!')
        else:
            samdb.newuser(username=request.form['Nom'],password=request.form['Prenom'],force_password_change_at_next_login_req=True,mailaddress="test@free.fr")
            return redirect(url_for('liste'))

    return render_template('create.html', variable='12345')
    

#Route liste ( liste des utilisateurs )    
@app.route('/liste')
def liste():
    
    strTable = " "

    query = "(|(objectclass=user))"
    result = samdb.search('DC=isis,DC=local', expression=query, scope=ldb.SCOPE_SUBTREE)
    
    for item in result:
    	if 'sAMAccountName' in item:
    		
        	#print(item['mail'])
        	#print(item['sAMAccountName'])
        	
        	if str(item['sAMAccountName']) != "DESKTOP-VA3I87F$" and str(item['sAMAccountName']) != "Administrator" and str(item['sAMAccountName']) != "Guest" and str(item['sAMAccountName']) != "DC1$" and str(item['sAMAccountName']) != "krbtgt":
        	   strTable = strTable+"<tr><td>"+str(item['sAMAccountName'])+ "</td><td>"+str(item['mail'])+ "</td><td>"+"<a href='delete?login="+str(item['sAMAccountName'])+"'>"+"<img src='/static/images/delete.png'></a>"+"</td></tr>"
        	
    file = open("templates/table.html","w")
    file.write(strTable)
    file.close()
    
    #return strTable
    return render_template('liste.html', users=strTable)



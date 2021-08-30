from flask import Flask, render_template, request, redirect, url_for, flash
from flask_table import Table, Col
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

#Clé pour les échanges de données chiffrées
app.config['SECRET_KEY'] = 'JSkjhdde45fr5LKSlKJSDd45ef4frgj54E10'

#Variable avec le chemin du dossier "upload"
UPLOAD_FOLDER = 'Upload/'

#Ouverture d’une connexion en direct sur la base LDB 
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
       file = request.files['file']
       if file.filename == '':
          return """
             <h1 style='color: red;'>Aucun fichier sélectionné!</h1>
             <button onclick="window.location.href='create'">Retour</button>

             """
            
       file = request.files['file']            
       filename = (file.filename)
       file.save(os.path.join(UPLOAD_FOLDER, filename))
       with open(os.path.join(UPLOAD_FOLDER, filename)) as fichier_csv:
          reader = csv.reader(fichier_csv, delimiter=',')
          #Boucle for, récuperation des informations sur chaque ligne du fichier CSV, ajout de l'utilisateur.
          for ligne in reader:
             #print(ligne[1])
             samdb.newuser(username=ligne[0],password=ligne[1],force_password_change_at_next_login_req=int(request.form['customSwitch1']),setpassword=int(request.form['customSwitch2']),userou="OU="+request.form['service'],mailaddress=ligne[4],telephonenumber=ligne[5],surname=ligne[3],givenname=ligne[2],scriptpath="C:\test.bat")
          
             
                
              
       return redirect(url_for('liste'))
    return redirect(url_for('liste'))



#Route delete
@app.route('/delete')
def test():
    if request.method == 'GET':
        login1 = request.args.get('login')
        

        if login1 == '':
           return """
             <h1 style='color: red;'>Aucun utilisateur sélectionné!</h1>
             <button onclick="window.location.href='create'">Retour</button>

             """
        else:
            samdb.deleteuser(username=request.args.get('login'))
            return redirect(url_for('liste'))

    return render_template('delete.html')



#Route create
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
       samdb.newuser(username=request.form['login'],password=request.form['password'],force_password_change_at_next_login_req=int(request.form['customSwitch3']),setpassword=int(request.form['customSwitch4']),userou="OU="+request.form['service'],mailaddress=request.form['email'],telephonenumber=request.form['phone'],surname=request.form['Nom'],givenname=request.form['Prenom'],scriptpath="C:\test.bat")
            
       return redirect(url_for('liste'))

    return render_template('create.html', variable='12345')
    


#Route liste ( liste des utilisateurs )    
@app.route('/liste')
def liste():
    
    strTable = " "
    
    #Récupération des utilisateurs dans la base samba.
    query = "(|(objectclass=user))"
    result = samdb.search('DC=isis,DC=local', expression=query, scope=ldb.SCOPE_SUBTREE)
    
    #Boucle for, creation du tableau HTML dans la variable strTable
    for item in result:
    	if 'sAMAccountName' in item:

        	
        	if str(item['sAMAccountName']) != "DESKTOP-VA3I87F$" and str(item['sAMAccountName']) != "Administrator" and str(item['sAMAccountName']) != "Guest" and str(item['sAMAccountName']) != "DC1$" and str(item['sAMAccountName']) != "krbtgt":
        	   strTable = strTable+"<tr><td>"+str(item['sAMAccountName'])+ "</td><td>"+str(item['mail'])+ "</td><td>"+"<a href='delete?login="+str(item['sAMAccountName'])+"'>"+"<img src='/static/images/delete.png'></a>"+"</td></tr>"
        	   
    #Enregistrement de la variable "strTable" vers "table.html"    	
    file = open("templates/table.html","w")
    file.write(strTable)
    file.close()
    
    #return strTable
    return render_template('liste.html', users=strTable)



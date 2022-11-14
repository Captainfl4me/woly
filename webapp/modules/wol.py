from flask_login import current_user
from flask import Blueprint, request, redirect, url_for, flash
from wakeonlan import send_magic_packet

from webapp.models import RemotePC
from webapp.app import db
import re

wol = Blueprint('wol', __name__, url_prefix='/wol')

@wol.route('', methods=['GET'])
def GetPCsListStr():
    return str(GetPCsList())

def GetPCsList():
    pcsQuery = RemotePC.query.all()
    
    pcsList = []
    for pc in pcsQuery:
        pcsList.append(pc.__dict__)
        
    return pcsList

@wol.route('', methods=['POST'])
def PostPCList():
    #Get request body infos
    name = request.form.get("name")
    macaddr = request.form.get("macaddr")
    
    if current_user.is_authenticated and not (name == None) and not (macaddr == None):
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macaddr.lower()):         
            #Create new PC object
            pc = RemotePC(name=name, macaddr=macaddr)
            #Push new PC object to database
            db.session.add(pc)
            db.session.commit()
            
            print("Add pc: " + name + " | " + macaddr);
        else:
            flash('Mac adress format is not valid.')
        return redirect(url_for('main.profile'))
    else:
        return 'Request not supported!'
    
@wol.route('/<id>', methods=['DELETE'])
def deletePC(id):
    if current_user.is_authenticated:
        RemotePC.query.filter_by(id=id).delete()
        db.session.commit()
        
        return redirect(url_for('main.profile'))
    
    return 'Not allowed!'
        
@wol.route('/wake', methods=['POST'])
def wakePc():
    if current_user.is_authenticated:
        id = request.form.get("id")
        remotePC = RemotePC.query.filter_by(id=id).first()
                
        print("wake: " + remotePC.macaddr) 
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", remotePC.macaddr.lower()):
            send_magic_packet(remotePC.macaddr)
            return '1'

    return '0'
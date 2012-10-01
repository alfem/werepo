# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

def index():

    if session.distro_id:
        session.flash = 'Using '+session.distro_description
    else:
        response.flash = "Choose one Distribution"
    return dict(distros=db(db.distros).select())

def select():        
# select a distro 
    session.distro_id=request.args[0]
    session.distro_description=db.distros[session.distro_id].name+" "+db.distros[session.distro_id].version
    redirect(URL('werepo','packages','index'))
   

def new():
    crud.messages.submit_button = 'Create'
    form = crud.create(db.distros)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

def edit():    
    crud.messages.submit_button = 'Change'
    crud.settings.update_next = URL('index')
    form = crud.update(db.distros, request.args[0],deletable=True)
    return dict(form=form)

def error():
    return dict()

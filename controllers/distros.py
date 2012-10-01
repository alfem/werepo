# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def index():
    """
    Index of Distros
    User must choose a device or create a new one.
    """
    if session.telefam_id:
        session.flash = 'Using '+session.telefam_description
    else:
        response.flash = "Choose one of yours Telefams"
    return dict(items=db(db.distros).select())


def select():        
# select a valid telefam 
# check if a nasty user is changing params in url
    check=db((db.users_telefams.user_id==auth.user_id) & (db.users_telefams.telefam_id==request.args[0]))
    if check.select():
      session.telefam_id=request.args[0]
      session.telefam_description=db.telefams[session.telefam_id].description
    redirect(URL('telefam','messages','index'))
      

def new():
    form = crud.create(db.distros)
    if form.process().accepted:
        redirect(URL('index'))
    else:
      return dict(message=T('Add a new Distribution'), form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)

@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

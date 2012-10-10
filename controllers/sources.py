# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
import datetime
import urllib2
from debian import deb822

@auth.requires_login()
def index():
    if session.distro_id:
        query=db((db.sources.distro_id==session.distro_id))
        return dict(sources=query.select())
    else:
        response.flash = "Choose one Distribution"
        redirect(URL('werepo','default','index'))


   
@auth.requires_login()
def new():
    crud.messages.submit_button = 'Create'
    form = crud.create(db.sources)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def edit():    
    crud.messages.submit_button = 'Save changes'
    crud.settings.update_next = URL('index')
    form = crud.update(db.sources, request.args[0],deletable=True)
    return dict(form=form)

@auth.requires_login()
def load():    
# Deletes all the references in a source, from packages to pool.
# Then, download a Packages index file and creates the corresponding rows again 
# in packages and pool tables
    source_id=request.args[0]
    
    item=db(db.sources.id==source_id).select()

    if len(item) != 1:
        return dict(message="Error",new=0,updated=0)
    
    
    db(db.packages.source_id == source_id).delete()
 
    new=0
    updated=0

    for section in item[0].sections:
        url="%s/dists/%s/%s/binary-i386/Packages" % (item[0].url, item[0].component, section)


        remote_file_handler=urllib2.urlopen(url)
        package_list=remote_file_handler.readlines()
        remote_file_handler.close()

        for pkg in deb822.Packages.iter_paragraphs(package_list):
            pool_item=db((db.pool.package==pkg['package']) & (db.pool.version==pkg['version'])).select()
            if len(pool_item) > 0:
                pool_id=pool_item[0]['id']
                updated+=1
            else:
                pool_id=db.pool.insert(package=pkg['package'],description=pkg['description'],version=pkg['version'],size=pkg['size'])
                new+=1
            db.packages.insert(source_id=source_id,pool_id=pool_id,section=section)

        db.commit()

    return dict(message="Successful!",new=new,updated=updated)



def error():
    return dict()

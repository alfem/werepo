# coding: utf8

import datetime
import urllib2
from debian import deb822

def call():
    """
    Returns services
    """
    session.forget()
    return service()

@service.run
def load_packages(sources_id):
# Deletes all the references to pool in table packages, from a source
# Then, download a Packages index file and creates the corresponding rows again 
# in packages and pool tables

    item=db(db.sources.id==sources_id).select()

    if len(item) != 1:
        return "ERROR"
    
    url="%s/dists/%s/%s/binary-i386/Packages" % (item[0].url, item[0].component, item[0].section)
    remote_file_handler=urllib2.urlopen(url)
    package_list=remote_file_handler.readlines()
    remote_file_handler.close()

    new=0
    updated=0

    db(db.packages.source_id == item[0].id).delete()

    for pkg in deb822.Packages.iter_paragraphs(package_list):
        pool_item=db((db.pool.package==pkg['package']) & (db.pool.version==pkg['version'])).select()
        if len(item) > 0:
            pool_id=pool_item[0]['id']
            updated+=1
        else:
            pool_id=db.pool.insert(package=pkg['package'],description=pkg['description'],version=pkg['version'],size=pkg['size'])
            new+=1
        db.packages.insert(source_id=item[0].id,pool_id=pool_id)

    return new,updated


@service.run
def clean_packages(sources_id):
# Deletes packages references from a source
    item=db(db.sources.id==sources_id).select()

    if len(item) != 1:
        return "ERROR"

#    db(db.pool.id != db.packages.pool_id).delete()

    ok=0;
    deleted=0;
    for row in db(db.pool.id > 0).select():
        if row.package.id > 0:     
          ok+=1
        else:
          deleted+=1
 
    return ok, deleted

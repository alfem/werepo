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
def load_packages(source_id):
# Deletes all the references to pool in table packages, from a source
# Then, download a Packages index file and creates the corresponding rows again 
# in packages and pool tables

    item=db(db.sources.id==source_id).select()

    if len(item) != 1:
        return "ERROR"
  
    db(db.packages.source_id == source_id).delete()

    new=0
    updated=0

    for section in item[0].sections:
        url="%s/dists/%s/%s/binary-i386/Packages" % (item[0].url, item[0].component, section)

        try:
          message="Downloading Packages..."
          remote_file_handler=urllib2.urlopen(url)
        except IOError as e:
          remote_file_handler=False
          message+='Oops, file does no exists. '

        if not remote_file_handler:
            try:
               message+="Trying Packages.gz..."
               compressed_file_handler=urllib2.urlopen(url+".gz")
               compressed_file = StringIO.StringIO(compressed_file_handler.read())
               remote_file_handler = gzip.GzipFile(fileobj=compressed_file)
            except IOError as e:
               message='Oops, file does not exists. '
               return 0,0,message

        message+="...OK. Loading..."

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
    
    message+="...success!"
    return new,updated,message




@service.run
def clean_packages(sources_id):
# FIX
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


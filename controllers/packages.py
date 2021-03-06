# coding: utf8


def index():
    """
    Index of Packages
    Paginated list of packages in a distribution
    """

    linesperpage = 10       # number of records per page

    if len(request.args):
       page=int(request.args[0])
    else: 
       page=0

    if request.vars.search:
       search=request.vars.search
       where=request.vars.where
       if where == 'names':
           searchfield=db.pool.package    
       else:
           searchfield=db.pool.description    
       query=db((db.distros.id==session.distro_id) & (db.sources.distro_id == db.distros.id) & (db.packages.source_id == db.sources.id) & (db.packages.pool_id==db.pool.id) & (searchfield.contains(search)) )

    else:
#       query=db((db.packages.pool_id==db.pool.id))
       query=db((db.distros.id==session.distro_id) & (db.sources.distro_id == db.distros.id) & (db.packages.source_id == db.sources.id) & (db.packages.pool_id==db.pool.id))

    rows=query.select(orderby=db.pool.package,limitby=(page,page+linesperpage))
    totalrecs=query.count()

    backward=A('<< previous',_href=URL(r=request,args=[page - linesperpage], vars=request.vars)) if page else '<< previous'
    forward=A('next >>',_href=URL(r=request,args=[page + linesperpage], vars=request.vars)) if totalrecs>page+linesperpage else 'next >>'

    nav= "Showing %d to %d out of %d records"  % (page + 1, page + len(rows), totalrecs)

    searchform=crud.search(db.pool)

    return dict(rows=rows,backward=backward,forward=forward, nav=nav, searchform=searchform)







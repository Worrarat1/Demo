import falcon

from contents import Resource
from contents import Home
from contents import Delete
from contents import Edit
from contents import Commit
from contents import Login


api = falcon.API()

contents = Resource(storage_path='.')
home = Home()
delete = Delete()
edit = Edit()
commit = Commit()
login = Login()

api.add_route('/contents', contents)

api.req_options.auto_parse_form_urlencoded = True
api.add_route('/home',home)

api.req_options.auto_parse_form_urlencoded = True
api.add_route('/home/del',delete)

api.req_options.auto_parse_form_urlencoded = True
api.add_route('/home/edit',edit)

api.req_options.auto_parse_form_urlencoded = True
api.add_route('/change',commit)

api.req_options.auto_parse_form_urlencoded = True
api.add_route('/',login)

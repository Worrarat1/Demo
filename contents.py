import json
import falcon
from bs4 import BeautifulSoup
from pymongo import MongoClient
import jwt
from datetime import datetime
from datetime import timedelta


####### secret key ######
secretkey = 'demokey'

######  JWT Duration before expire (seconds) ######
expireTime = 30


##### MongoDB Host ###
client = MongoClient('localhost', 27017)

##### MongoDB Database ###
db = client.testDB


##### MongoDB collection ###
collection = db.testCol


def TokenCheck(req, resp, resource, params):
    try: 
        reqtoken = Login.deToken 
    except:
        reqtoken = None
        
    if not reqtoken:
        msg = 'Token is missing!'
        raise falcon.HTTPBadRequest('Message', msg)
    try: 
        jwt.decode(reqtoken, secretkey)
    except:
        msg = 'Signature is Expire!'
        raise falcon.HTTPBadRequest('Message', msg)
    


    
def ShowData(location):
    with open(location, 'r') as f:
        html = f.read()
        
    soup = BeautifulSoup(html,'html.parser')
        
    tableTag = soup.find(id="showData")
    
    dataMongo = []
    for post in collection.find():
        dataMongo.append(post)
    
    for i in range(len(dataMongo)):

        
        new_tr = soup.new_tag("tr")
        tableTag.append(new_tr)
        
        del_form = soup.new_tag("form",action="http://localhost:8000/home/del?{}".format(i),method="post")
        new_tr.append(del_form)
        
        del_td = soup.new_tag("td")
        del_form.append(del_td)
        
        del_bt = soup.new_tag("button")
        delVal="Delete"
        del_bt.string = delVal
        del_td.append(del_bt)    
        
        edit_form = soup.new_tag("form",action="http://localhost:8000/home/edit?{}".format(i),method="post")
        new_tr.append(edit_form)
        
        edit_td = soup.new_tag("td")
        edit_form.append(edit_td)
        
        edit_bt = soup.new_tag("button")
        editVal="Edit"
        edit_bt.string = editVal
        edit_td.append(edit_bt)    
        
        
        for j in range(1,len(dataMongo[0])): 
            inVal = dataMongo[i][list(dataMongo[0].keys())[j]]
            new_td = soup.new_tag("td")
            new_td.string = inVal
            new_tr.append(new_td)

    return soup

class Resource(object):
    
    _CHUNK_SIZE_BYTES = 4096
    def __init__(self, storage_path):
        self._storage_path = storage_path

    def on_get(self, req, resp):
        
        showMongo = []
        for post in collection.find():
            del post['_id']
            showMongo.append(post)
            
        doc = showMongo
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
       
@falcon.before(TokenCheck)
class Home(object):
    

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML
        
        soup = ShowData('F:/Works/Test/static/index.html')
        resp.body = soup
        
    
    def on_post(self, req, resp):

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML
        
        # inseart new data
        post = {"Name": req.params['name'],
                "Age": req.params['age'],
                "Country": req.params['country']}
        
        collection.insert(post)
        
        soup = ShowData('F:/Works/Test/static/index.html')
        resp.body = soup


@falcon.before(TokenCheck)  
class Delete(object):     
    
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML

        getDel = req.url
        sepDel = getDel.split('?')
        seDel = int(sepDel[1])
        
        dataMongo = []
        for post in collection.find():
            dataMongo.append(post)

        collection.delete_one({'_id': dataMongo[seDel]['_id']})
        collection.count({'_id': dataMongo[seDel]['_id']})
        
        soup = ShowData('F:/Works/Test/static/index.html')
        resp.body = soup


@falcon.before(TokenCheck)  
class Edit(object):
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML
        
        Edit.getEdit = req.url
        Edit.sepEdit = Edit.getEdit.split('?')
        Edit.seEdit = int(Edit.sepEdit[1])
        
        dataMongo = []
        for post in collection.find():
            dataMongo.append(post)
       
        soup = ShowData('F:/Works/Test/static/edit.html')
        resp.body = soup
        
        fName = soup.find(id='name')
        fName['value'] = dataMongo[Edit.seEdit]['Name']
        
        fAge = soup.find(id='age')
        fAge['value'] = dataMongo[Edit.seEdit]['Age']
        
        fCountry = soup.find(id='country')
        fCountry['value'] = dataMongo[Edit.seEdit]['Country']
        
        return Edit.seEdit
 
@falcon.before(TokenCheck)           
class Commit(Edit):
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML
        
        dataMongo = []
        for post in collection.find():
            dataMongo.append(post)
            
        collection.replace_one({"_id" : dataMongo[Edit.seEdit]['_id']},{"Name": req.params['name'],
                "Age": req.params['age'],
                "Country": req.params['country']})
            
        
        soup = ShowData('F:/Works/Test/static/index.html')
        resp.body = soup

        

class Login():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML
        
        with open('F:/Works/Test/static/login.html', 'r') as f:
            html = f.read()
            
        resp.body = html
        
    
    def on_post(self, req, resp):
            
        if req.params["psw"] == '1234':
            
            token = jwt.encode({'user':req.params['username'],'exp': datetime.utcnow() + timedelta(seconds=expireTime)},secretkey)

            Login.deToken = token.decode('UTF-8')
            
#            Login.jsonToken = json.dumps({"Token" : Login.deToken})

            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_HTML
            
#            soup = ShowData('F:/Works/Test/static/index.html')
#            resp.body = soup
            
            resp.set_header('Content-Type', 'text/html;')
            resp.body = '<html><head><meta http-equiv="refresh" content="0; url=http://localhost:8000/home"></head><body></body></html>'

            return Login.deToken
        else:
             resp.body = 'Wrong Password'
        
        
            

        
      

  



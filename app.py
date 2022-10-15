
from flask import Flask, make_response, request
import dbhelpers as dh
import apihelper as a
import json
import dbcreds as d

app = Flask(__name__)
# show the whole list of candy, no argument
@app.get('/api/candy')
def show_all_candy():
    result=dh.run_statement('CALL show_all_candy()')
    if(type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

# provide 3 values for the argument and returns the id of the candy that's added
@app.post('/api/candy')
def add_candy():
    valid_check = a.check_endpoint_info(request.json, ['name', 'img_url', 'description'])
    if(type(valid_check) != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result =dh.run_statement('CALL add_candy(?,?,?)', [request.json.get('name'), request.json.get('img_url'), request.json.get('description')])
    if (type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

@app.delete('/api/candy')

def delete_candy():
    valid_check = a.check_endpoint_info(request.json, ['id'])
    if(type(valid_check) != None):
        return make_response(json.dumps(valid_check, default=str), 400)
    
    result=dh.run_statement('CALL delete_candy(?)', [request.json('id')])

    if (type(result) == list):
        return make_response(json.dumps( result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)


    





if(d.production_mode == True):
    print("Running in Production Mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)
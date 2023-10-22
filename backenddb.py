import os
import pymongo
import json
import random
import time
import requests

import openai


openai.api_key = "REDACTED"




def getcurated(prompt):
    prempt = "Can you send me advice for a student moving from a home to a shelter ?"
    
    prempt += "\n\n"
    
    prempt += prompt


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": prempt},
            ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    print(result)
    
    print ("******************")
    
    ##process
    
    rjson = {}
    
    
    rdata = []
    

    rjson['data'] = rdata
        
    
    return result, rjson




def sendsms(tonum, message):


    url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/sendsms"

    payload = json.dumps({
    "receiver": tonum,
    "message": message,
    "token": "REDACTED"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)



def dummy(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    }

    mongostr = os.environ.get('MONGOSTR')
    client = pymongo.MongoClient(mongostr)
    db = client["tadhacks2023"]

    request_json = request.get_json()

    retjson = {}

    action = request_json['action']


    if action == "getschools":
        col = db.schools
        schools = []
        for x in col.find():
            sch = {}
            sch['name'] = x['name']
            sch['id'] = x['id']
            sch['type'] = x['type']
            sch['address'] = x['address']
            schools.append(sch)
        

        retjson['status'] = "retrieved"
        retjson['schools'] = schools

        return json.dumps(retjson)



    if action == "getgrades":
        col = db.schedules
        schools = []
        for x in col.find():
            sch = {}
            sch['studentid'] = x['studentid']
            sch['id'] = x['id']
            sch['date'] = x['date']
            sch['grades'] = x['grades']
            schools.append(sch)
        

        retjson['status'] = "retrieved"
        retjson['allgrades'] = schools

        return json.dumps(retjson)


    if action == "getagrade":
        col = db.schedules
        sch = {}
        for x in col.find():
            if x['studentid'] != request_json['studentid']:
                continue
            sch['studentid'] = x['studentid']
            sch['id'] = x['id']
            sch['date'] = x['date']
            sch['grades'] = x['grades']

            break

        
        retjson['status'] = "retrieved"
        retjson['grades'] = sch

        return json.dumps(retjson)



    if action == "getstudents":
        col = db.students
        schools = []
        for x in col.find():
            sch = {}
            sch['name'] = x['name']
            sch['id'] = x['id']
            sch['address'] = x['address']
            sch['lname'] = x['lname']
            sch['age'] = x['age']
            sch['dob'] = x['dob']
            sch['race'] = x['race']
            sch['ethnicity'] = x['ethnicity']
            sch['gender'] = x['gender']
            sch['grade'] = x['grade']
            sch['schoolid'] = x['schoolid']
            sch['exschoolid'] = x['exschoolid']
            sch['shelterid'] = x['shelterid']

            schools.append(sch)
        

        retjson['status'] = "retrieved"
        retjson['students'] = schools

        return json.dumps(retjson)




    if action == "getastudent":
        col = db.students
        sch = {}
        for x in col.find():
            if x['id'] != request_json['id']:
                continue
            sch['name'] = x['name']
            sch['id'] = x['id']
            sch['address'] = x['address']
            sch['lname'] = x['lname']
            sch['age'] = x['age']
            sch['dob'] = x['dob']
            sch['race'] = x['race']
            sch['ethnicity'] = x['ethnicity']
            sch['gender'] = x['gender']
            sch['grade'] = x['grade']
            sch['schoolid'] = x['schoolid']
            sch['exschoolid'] = x['exschoolid']
            sch['shelterid'] = x['shelterid']
            break

        
        retjson['status'] = "retrieved"
        retjson['student'] = sch

        return json.dumps(retjson)




    if action == "addstudent" :


        col = db.students
        id =0
        for x in col.find():
            id +=1

        reading = {}
        reading['id'] = str(id+1)
        reading['name'] = request_json['name']
        reading['lname'] = request_json['lname']
        reading['age'] = request_json['age']
        reading['dob'] = request_json['dob']
        reading['race'] = request_json['race']
        reading['ethnicity'] = request_json['ethnicity']
        reading['address'] = request_json['address']
        reading['gender'] = request_json['gender']
        reading['grade'] = request_json['grade']
        reading['shelterid'] = "-1"
        reading['schoolid'] = "-1"
        reading['exschoolid'] = "-1"
        

        result=col.insert_one(reading)

        # pid = add_readings(conn, name, ownerid, value, time)

        retjson['status'] = "successfully added"
        retjson['id'] = id

        return json.dumps(retjson)



    if action == "addgrades" :


        col = db.schedules
        id =1
        found = 0
        for x in col.find():
            id +=1
            if x['studentid'] == request_json['studentid']:
                found = 1
                break

        if found == 0:

            reading = {}
            reading['id'] = str(id)
            reading['studentid'] = request_json['studentid']
            reading['date'] = request_json['date']
            reading['grades'] = request_json['grades']

            result=col.insert_one(reading)
        
        else:
            col.update_one({"id": str(id)}, {"$set":{"date":request_json['date']}})
            col.update_one({"id": str(id)}, {"$set":{"grades":request_json['grades']}})


        # pid = add_readings(conn, name, ownerid, value, time)

        retjson['status'] = "successfully added"
        retjson['id'] = id

        return json.dumps(retjson)


    if action == "addschool" :


        col = db.schools
        id =0
        for x in col.find():
            id +=1

        reading = {}
        reading['id'] = str(id+1)
        reading['name'] = request_json['name']
        reading['type'] = request_json['type']
        reading['address'] = request_json['address']

        result=col.insert_one(reading)

        # pid = add_readings(conn, name, ownerid, value, time)

        retjson['status'] = "successfully added"
        retjson['id'] = id

        return json.dumps(retjson)


    if action == "addshelter" :


        col = db.shelters
        id =0
        for x in col.find():
            id +=1

        reading = {}
        reading['id'] = str(id+1)
        reading['name'] = request_json['name']
        reading['capacity'] = request_json['capacity']
        reading['enrolled'] = request_json['enrolled']
        reading['address'] = request_json['address']
        reading['eschoolid'] = request_json['eschoolid']
        reading['mschoolid'] = request_json['mschoolid']
        reading['hschoolid'] = request_json['hschoolid']

        result=col.insert_one(reading)

        # pid = add_readings(conn, name, ownerid, value, time)

        retjson['status'] = "successfully added"
        retjson['id'] = id

        return json.dumps(retjson)


    if action == "addstudenttoshelter":
        col = db.students
        col2 = db.shelters

        found = 0
        count = 0
        id = "0" ##can change this

        id = request_json['studentid']
        sid = request_json['shelterid']
        grade = -1
        nschoolid = "-1"
        cschoolid = "-1"

        for x in col.find():
            if x['id'] == id:
                found = 1
                id = x['id']
                grade = int(x['grade'])
                cschoolid = x['schoolid']
                break

        if found != 1:
            retjson['status'] = "unknown student id"

            return json.dumps(retjson)

        enr = 0
        for x in col2.find():
            if x['id'] == sid:
                found = 2
                enr = x['enrolled']

                if grade >8:
                    nschoolid = x['hschoolid']
                    break
                if grade <= 8 and grade > 5:
                    nschoolid = x['mschoolid']
                    break
                if grade <=5:
                    nschoolid = x['eschoolid']
                    break
                
        if found != 2:
            retjson['status'] = "unknown shelter id"

            return json.dumps(retjson)
        

        col.update_one({"id": id}, {"$set":{"shelterid":sid}})
        col.update_one({"id": id}, {"$set":{"schoolid":nschoolid}})
        col.update_one({"id": id}, {"$set":{"exschoolid":cschoolid}})
        col2.update_one({"id": sid}, {"$set":{"enrolled":enr+1}})

        ##notify old school to send grades for student

        retjson['status'] = "records updated"

        return json.dumps(retjson)

    if action == "gpt":
        prompt = request_json['prompt']
        token = request_json['token']

        result, rjson = getcurated(prompt)
        

        return json.dumps(rjson)



    retstr = "action not done"

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return retstr

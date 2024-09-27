from utils import *
from flask import Flask,request,jsonify,json,stream_with_context
from flask_cors import CORS, cross_origin
import os
from termcolor import colored
import shutil
import re
from flask import request
import getlogs

app = Flask(__name__)
CORS(app,resource={
    r"http://localhost:3000/*":{
        "origins":"*"
    }
})

@app.route('/file_save',methods=['POST'])
@cross_origin()
def File_Save():
    # shutil.rmtree('Data', ignore_errors=True)
    # for i in os.listdir('Data'):
    #     os.remove(os.path.join('Data',i))
    content = request.files
    a = 'File Not Uploaded'
    temp = []
    if content:
        for file in content:
            filelist = content.getlist(f'{file}')
            for file1 in filelist:
                filename = os.path.basename(file1.filename)
                file1.save(os.path.join('Data',filename))
                a = 'File Uploaded'
                unsupported_types = ['docx','xlsx','pptx']
                pattern = r'\.(.*)$'
                match = re.search(pattern, filename)
                if  match.group(1) in unsupported_types:
                    return "FILE NOT SUPPORTED"

    return jsonify({'status':a})

@app.route('/agent_query',methods=['POST'])
@cross_origin()
def Agent_Query():
    rev_bot = cyberbot()
    data = json.loads(request.data.decode())
    print(data['prompt'])
    res = rev_bot.main_agent(proompt=data["prompt"])
    print("MAIN AGENT DONE")
    return jsonify({'response':res})

@app.route('/converttocsv',methods=['POST'])
@cross_origin()
def ConverttoCSV():
    rev_bot = cyberbot()
    data = json.loads(request.data.decode())
    res = rev_bot.unstruct_to_csv(data['data'])
    file_path = f"Data\{data['filename']}.csv"
    f = open(file_path,'x')
    f.write(res)
    f.close()
    status = {'status':'Not Converted Please Try again later'}
    if os.path.exists(f"Data\{data['filename']}.csv"):
        status = {'status':'Converted to CSV successfully'}
    return jsonify(status)

@app.route('/create_logs',methods=['GET','POST'])
@cross_origin()
def Create_logs():
    if request.data:
        data = json.loads(request.data.decode())
        getlogs.main(max_count=int(data['max_count']),time_interval=int(data['time_interval']))
    else:
        getlogs.main()
    response = {}
    response['status'] = "NO FILE FOUND, ERRROR"
    response['filename'] = False
    response['data'] = False
    if os.path.exists('Data\cybersecurity_logs_structured.csv'):
        with open('Data\cybersecurity_logs_structured.csv','r') as f:
            res = f.read()
        response['status'] = 'File Created'
        response['filename'] = 'Data\cybersecurity_logs_structured.csv'
        response['data'] = res
    return jsonify(response)

@app.route('/master_agent',methods=['POST'])
@cross_origin()
def MasterAgent():
    data = request.data.decode()
    data = json.loads(data)
    rev_bot = cyberbot()
    res = rev_bot.master_agent(data['query'])
    return jsonify({'master_reponse':res})

if __name__ == '__main__':
    app.run(port=8080,debug=True)

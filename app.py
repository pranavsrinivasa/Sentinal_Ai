from utils import *
from flask import Flask,request,jsonify,json,stream_with_context
from flask_cors import CORS, cross_origin
import os
from termcolor import colored
import shutil
import re
from flask import request

app = Flask(__name__)
CORS(app,resource={
    r"http://localhost:3000/*":{
        "origins":"*"
    }
})

@app.route('/file_save',methods=['POST'])
@cross_origin()
def File_Save():
    shutil.rmtree('Data', ignore_errors=True)
    for i in os.listdir('Data'):
        os.remove(os.path.join('Data',i))
    ls = os.listdir('Data')
    ls1 = os.path.exists('../data')
    print(colored(f'\n\n**-Files in database,data cache are cleared-**\n**-Contents of database is :{[i for i in ls]}-**\n**--Contents of data is {ls1}**--\n\n','red',attrs=['bold']))
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

if __name__ == '__main__':
    app.run(port=8080,debug=True)

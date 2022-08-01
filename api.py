from flask import Flask, jsonify, request
import os, sys
from docxtpl import DocxTemplate
import string
from mega import Mega
from dotenv import load_dotenv

load_dotenv('.env')

email = os.environ.get("email")
password = os.environ.get("password")


os.chdir(sys.path[0])

app = Flask(__name__)

class Generate_Docs():
    def __init__(self, data):
        
        mega  = Mega()
        self.name = data["NAME"]
        
        self.filename1 = f'{self.name} affidavit format 1.docx'
        self.filename2 = f'{self.name} affidavit format 2.docx'
        
        self.user = mega.login(email, password)

        self.doc = DocxTemplate('FormatOne.docx')
        self.doc2 = DocxTemplate('FormatTwo.docx')
        

        self.context = {
            "NAME": self.name,
            "RELATION_NAME": data["RELATION_NAME"],
            "RELATION": data["RELATION"],
            "BLOCK": data["BLOCK"],
            "PLACE": data["PLACE"],
            "PLACE_NAME": data["PLACE_NAME"],
            "POST_OFFICE": data["POST_OFFICE"],
            "POLICE_STATION": data["POLICE_STATION"],
            "DISTRICT": data["DISTRICT"],
            "DATE": data["DATE"],
            "RELIGION": data["RELIGION"]
        }


    def generateDocument(self):

        self.doc.render(self.context)
        self.doc2.render(self.context)
        
        self.doc.save(f'{self.name} affidavit format 1.docx')
        self.doc2.save(f'{self.name} affidavit format 2.docx')
        
    
    def uploadMEGA(self):
        
        self.user.create_folder(f'DOCS_TESTREPORT/{self.name}')
        
        folder = self.user.find(self.name, exclude_deleted=True)
        
        file1 = self.user.upload(self.filename1, folder[0])
        file2 = self.user.upload(self.filename2, folder[0])
        
        link1 = self.user.get_upload_link(file1)
        link2 = self.user.get_upload_link(file2)
        
        files = [self.filename1, self.filename2]
        
        for file in files:
            os.remove(file)
        
        links = [link1, link2]
        
        return links
        
        

#Dummy data for test
        
# helo = {
#     "NAME": "HELLOW",
#     "RELATION_NAME": "DAD",
#     "RELATION": "BAD",
#     "BLOCK": "SAD",
#     "PLACE": "MAD",
#     "PLACE_NAME": "CAT",
#     "POST_OFFICE":"RAT",
#     "POLICE_STATION": "SAT",
#     "DISTRICT": "JET",
#     "DATE": "NET",
#     "RELIGION": "HOLY"
#     }
    




@app.route("/")
def hello_world():
    return "<p>Test Report Generator</p>"


@app.route("/add", methods=["POST"])
def get_data():
    data = request.json
    
    docins = Generate_Docs(data)

    docins.generateDocument()
    links = docins.uploadMEGA()
    
    processed_data = {
        "Link-1": links[0],
        "Link-2": links[1]
        
    }
    
    return jsonify(processed_data)
    
    
    


if __name__ == "__main__":
    app.run(debug=True)
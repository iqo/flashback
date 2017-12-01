from flask import Flask
from flask_restful import Resource, Api
from minio import Minio
from minio.error import ResponseError

app = Flask(__name__)

api = Api(app)
#minioClient = Minio('127.0.0.1:9000',
 #                   access_key='IW6X2CGYU7GPK3W0CSX9',
 #                   secret_key='Dmb3tAH6V6ub8NsVa+kv5rQWQ2I3DHbz7xCUu9jFT',
  #                  secure=False)
minioClient = Minio('155.4.193.120:9000',
                    access_key='M432WQDCN0SKMW0LS961',
                    secret_key='MVQdFH7kiea8g4UFxSE5xEMoWfShXz7Sh2lv8AT9',
                    secure=False)
class Hello(Resource):
    def get(self):
        return "Hello"

class UploadFolder(Resource):
    def get(self, dirname):
        try:
            return minioClient.bucket_exists(dirname)
        except ResponseError as err:
            print(err)


api.add_resource(Hello, '/hello') # Route_1
api.add_resource(UploadFolder,'/uploadfolder/<dirname>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

    
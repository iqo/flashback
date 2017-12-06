from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api
from minio import Minio
from minio.error import ResponseError
from datetime import timedelta

app = Flask(__name__)

api = Api(app)
#minioClient = Minio('localhost:9000',
#                    access_key='IW6X2CGYU7GPK3W0CSX9',
#                    secret_key='Dmb3tAH6V6b8NsVa+kv5rQWQ2I3DHbz7xCUu9jFT',
#                    secure=False)

minioClient = Minio('155.4.193.120:9000',
                    access_key='M432WQDCN0SKMW0LS961',
                    secret_key='MVQdFH7kiea8g4UFxSE5xEMoWfShXz7Sh2lv8AT9',
                    secure=False)

class Hello(Resource):
    def get(self):
        return "kul"

class FolderExists(Resource):
    def get(self, dirname):
        try:
            return minioClient.bucket_exists(dirname)
        except ResponseError as err:
            print(err)

class GetBucket(Resource):
    def get(self, dirname, objectname):
        try:
            url = minioClient.presigned_get_object(dirname, objectname, expires=timedelta(hours=1))
            return (url)
        # Response error is still possible since internally presigned does get bucket location.
        except ResponseError as err:
            print(err)

class ListBuckets(Resource):
    def get(self):
        try:
            buckets = minioClient.list_buckets()
            bucketslist = []
            for bucket in buckets:
                bucketslist.append(bucket.name)
            
            return jsonify(bucketslist)
        except ResponseError as err:
            print(err)


api.add_resource(Hello, '/hello') # Route_1
api.add_resource(FolderExists,'/exists/<dirname>')
api.add_resource(GetBucket, '/getobject/<dirname>/<objectname>')
api.add_resource(ListBuckets, '/listbuckets')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

    
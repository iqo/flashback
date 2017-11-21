import os
import sys
import argparse
from minio import Minio
from minio.error import ResponseError


def getClient():
    minioClient = Minio('127.0.0.1:9000',
                    access_key='IW6X2CGYU7GPK3W0CSX9',
                    secret_key='Dmb3tAH6V6b8NsVa+kv5rQWQ2I3DHbz7xCUu9jFT',
                    secure=False)
    return minioClient


def uploadfolder(dirname):
    client = getClient()
    try:
        if(not(client.bucket_exists(dirname))): 
            client.make_bucket(dirname)
        for filename in os.listdir(dirname):
            file_stat = os.stat(dirname+'/'+filename)   
            file_data = open(dirname+'/'+filename, 'rb')
            client.put_object(dirname, filename, file_data, file_stat.st_size)
    except ResponseError as err:
        print(err)

def deletefolder(dirname):
    client = getClient()
    try:
        if(client.bucket_exists(dirname)):
            objects = client.list_objects(dirname)
            for obj in objects:
                client.remove_object(dirname, obj.object_name)
            client.remove_bucket(dirname)
    except ResponseError as err:
        print(err)


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    print(sys.argv)
    if(sys.argv[1] == 'uploadfolder'):
        uploadfolder(sys.argv[2])
    elif(sys.argv[1] == 'deletefolder'):
        deletefolder(sys.argv[2])
    else:
        print("Damn son its broken")
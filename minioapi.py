import os
import sys
import shutil
import urllib2
from minio import Minio
from minio.error import ResponseError
from multiprocessing import Queue


def getClient():
    #minioClient = Minio('127.0.0.1:9000',
    #                access_key='IW6X2CGYU7GPK3W0CSX9',
    #                secret_key='Dmb3tAH6V6b8NsVa+kv5rQWQ2I3DHbz7xCUu9jFT',
    #                secure=False)
    minioClient = Minio('155.4.193.120:9000',
                    access_key='M432WQDCN0SKMW0LS961',
                    secret_key='MVQdFH7kiea8g4UFxSE5xEMoWfShXz7Sh2lv8AT9',
                    secure=False)
    return minioClient


def uploaddir(path, dirname):
    client = getClient()
    try:
        if(not(client.bucket_exists(dirname))): 
            client.make_bucket(dirname)
        for filename in os.listdir(path+dirname):
            file_stat = os.stat(path+dirname+'/'+filename)   
            file_data = open(path+dirname+'/'+filename, 'rb')
            client.put_object(dirname, filename, file_data, file_stat.st_size)
    except ResponseError as err:
        print(err)

def deletedir(dirname):
    client = getClient()
    try:
        if(client.bucket_exists(dirname)):
            objects = client.list_objects(dirname)
            for obj in objects:
                client.remove_object(dirname, obj.object_name)
            client.remove_bucket(dirname)
    except ResponseError as err:
        print(err)

def downloadfile(dirname, filename):
    client = getClient()
    try:
        data = client.get_object(dirname, filename)
        with open('my-testfile', 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)
    except ResponseError as err:
        print(err)

def downloaddir(dirname):
    client = getClient()
    path = 'downloads/'+dirname
    try: 
        if(client.bucket_exists(dirname)):
            if not os.path.exists(path):
                os.makedirs(path)
            objects = client.list_objects(dirname)
            for obj in objects:
                data = client.get_object(dirname, obj.object_name)
                with open(path+'/'+obj.object_name, 'wb') as file_data:
                    for d in data.stream(32*1024):
                        file_data.write(d)

    except ResponseError as err:
        print(err)

def deletelocaldir(dirname):
    shutil.rmtree(dirname)

def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False

def uploadAndPurge(queue):
    queue.put("started upload")
    if not internet_on():
        return
    pictures = os.listdir("pictures")
    print(os.listdir("pictures"))
    for dirname in pictures:
        print(dirname)
        uploaddir("pictures/", dirname)
        deletelocaldir("pictures/" + dirname)

def purgeOnlineStorage(queue):
    queue.put("started purge of storage")
    client = getClient()
    buckets = client.list_buckets()
    for bucket in buckets:
        deletedir(bucket.name)


if __name__ == '__main__':
    try:
        queue = Queue()
        if(sys.argv[1] == 'test'):
            purgeOnlineStorage()
        elif(sys.argv[1] == 'uploaddir'):
            uploaddir(sys.argv[2]+"/", sys.argv[3])
        elif(sys.argv[1] == 'deletedir'):
            deletedir(sys.argv[2])
        elif(sys.argv[1] == 'downloadfile'):
            downloadfile(sys.argv[2], sys.argv[3])
        elif(sys.argv[1] == 'downloaddir'):
            downloaddir(sys.argv[2])
        elif(sys.argv[1] == 'deletelocal'):
            deletelocaldir(sys.argv[2])
        elif(sys.argv[1] == "uploadandpurge"):
            uploadAndPurge(queue)
        elif(sys.argv[1] == "purgeRemote"):
            purgeOnlineStorage(queue)
        else:
            print("Non-existing function")
    except IndexError:
        print("Index error")

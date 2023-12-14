from datetime import datetime
from azure.storage.fileshare import ShareFileClient
import xtarfile as tarfile
import shutil
import os
import sys

#TODO: move these into a web.config file

STORAGE=os.environ['STORAGE']


def current_time():
  now = datetime.now()
  return now.strftime("%H:%M:%S") 

def getCDB(path):
    file_client = ShareFileClient.from_connection_string(conn_str=STORAGE, share_name="cdb", file_path="fam.faiss.tar")    
    try:
     shutil.rmtree(path) 
    except FileNotFoundError:
     #file not there
     print (f"{current_time()}  FAISS Directory not found assume clean install")
    with open("fam.faiss.tar", "wb") as file_handle:
        data = file_client.download_file()
        data.readinto(file_handle)
        print (f"{current_time()}download complete")
    my_tar = tarfile.open('fam.faiss.tar','r')
    my_tar.extractall(path) 
    my_tar.close()
    try:
     os.remove('fam.faiss.tar')
    except FileNotFoundError:
     # if it fails here, it means it didn't download and app should fail
     print(f"{current_time()}  Unable to Retreive Chrome Data Base from Storage")
     sys.exit()


 
import time
import urllib.request
import threading
import datetime
import json
import os
from subprocess import call


bucket_name = "dotcams3"

# load cam.json from current directory 
with open('cam.json') as f:
    file = json.load(f)


##################### Functions ##################
def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts)]


def download_dot_files(id, url):
    
    folder = "dotcam"
    dirname = id 
    
    # current time
    now = datetime.datetime.now()
   
    # check if specified directory exists if not create one   
    if not os.path.exists(folder+"/"+dirname):
        os.makedirs(folder+"/"+dirname)
    try:
        # retrieve image from specified url and save it to given path
        urllib.request.urlretrieve(url, folder+"/"+dirname+"/"+dirname+"_"+str(now)+".png")
       
    except IOError:
        print("Error while accessing url..")

    

# retrieve every id and url from loaded cam.json and pass them to download_dot_files 
def save_images(id,url):
    download_dot_files(id,url)
        
def uploadToS3():
    call("sudo aws s3 sync dotcam/ s3://"+ bucket_name +"/", shell=True)

 
def removeFromLocal():
    call("sudo rm -rf dotcam/", shell=True)


# ########################## Main Program ###########################

thread_list = []

for i in split_list(file["Camera"], wanted_parts=20):
    for j in i:
       
        t = threading.Thread(target=save_images, name = "thread{}".format(i), args=(j["locId"],j["url"]))
        thread_list.append(t)
        t.start()

for t in thread_list:
    t.join()
    

t = threading.Thread(target=uploadToS3, name = "s3Upload")
t.start()
t.join()

t = threading.Thread(target=removeFromLocal, name = "rmoveFromLocal".format(i))
t.start()
t.join()
    

print("Finished")




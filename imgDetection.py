from imageai.Detection import ObjectDetection
import os
from subprocess import call
from datetime import datetime
import boto3
from decimal import *
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("Image_analysis")

observationNum = 1

path = "/home/ubuntu/Cam/"
img = ["ID_529","ID_932","ID_1116","ID_1161"]
camId = []
timestamp = []

dtime = []
image = []



analyzedImg = ["ID_529_a","ID_932_a","ID_1116_a","ID_1161_a"]

for ai in analyzedImg:
        if not os.path.exists("AnalyzedImage/"+ai):
            os.makedirs("AnalyzedImage/"+ai)  

for i in img :
    image.append(os.listdir(path+i)[0])
    camId.append(os.listdir(path+i)[0].split("_")[1])
    timestamp.append(int(os.listdir(path+i)[0].split("_")[2][0:-4])/1000)
    dtime.append(datetime.utcfromtimestamp(int(os.listdir(path+i)[0].split("_")[2][0:-4])/1000).strftime('%Y-%m-%d %H:%M:%S'))




execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()


detections1 = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "Cam/ID_529/" , image[0]),
    output_image_path=os.path.join(execution_path , "AnalyzedImage/ID_529_a/"+analyzedImg[0]+"_"+dtime[0]))
detections2 = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "Cam/ID_932/" , image[1]),  
    output_image_path=os.path.join(execution_path , "AnalyzedImage/ID_932_a/"+analyzedImg[1]+"_"+dtime[1]))
detections3 = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "Cam/ID_1116/" , image[2]),  
    output_image_path=os.path.join(execution_path , "AnalyzedImage/ID_1116_a/"+analyzedImg[2]+"_"+dtime[2]))
detections4 = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "Cam/ID_1161/" , image[3]), 
    output_image_path=os.path.join(execution_path , "AnalyzedImage/ID_1161_a/"+analyzedImg[3]+"_"+dtime[3]))



    

        
for eachObject in detections1:
    
    table.put_item(
    Item={
        'ObservationNum':observationNum,
        'CamId':camId[0],
        'Image-date-time':dtime[0],
        'Catogery':eachObject["name"],
        'Probability':Decimal(eachObject["percentage_probability"]),
    }
        )
    observationNum += 1

    

for eachObject in detections2:
    
    table.put_item(
    Item={
        'ObservationNum':observationNum,
        'CamId':camId[1],
        'Image-date-time':dtime[1],
        'Catogery':eachObject["name"],
        'Probability':Decimal(eachObject["percentage_probability"]),
    }
        )
    observationNum += 1
        
for eachObject in detections3:
    
    table.put_item(
    Item={
        'ObservationNum':observationNum,
        'CamId':camId[2],
        'Image-date-time':dtime[2],
        'Catogery':eachObject["name"],
        'Probability':Decimal(eachObject["percentage_probability"]),
    }
        )
    observationNum += 1    

for eachObject in detections4:
    
    table.put_item(
    Item={
        'ObservationNum':observationNum,
        'CamId':camId[3],
        'Image-date-time':dtime[3],
        'Catogery':eachObject["name"],
        'Probability':Decimal(eachObject["percentage_probability"]),
    }
        )
    observationNum += 1       
 

    
for i in img :    
    call("sudo rm -rf " +path+i , shell=True)

 
#analyzedImg = os.listdir("/home/ubuntu/AnalyzedImage")

for i in analyzedImg:
    call("sudo aws s3 sync AnalyzedImage/" + i +"/ s3://dotcam/"+i, shell=True)
    call("sudo rm -rf AnalyzedImage/" + i, shell=True)

print("done!")
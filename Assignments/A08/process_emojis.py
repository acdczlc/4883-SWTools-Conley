#Zac Conley
# A08-Mosaic-process_emojis.py
#This program processes all emojis in a given folder
import os
import sys
import cv2
from PIL import Image,ImageMath
import json
import numpy as np
import requests
from sklearn.cluster import KMeans

if __name__=='__main__':
    print("\nZac Conley")
    print("A08-Mosaic-process_emojis.py")
    print("This program processes all emojis in a given folder \n")
    args = {}
    for arg in sys.argv[1:]: #split command line arguments
        f_type,values = arg.split('=')
        args[f_type] = values
        if(f_type=='folder'):
            emoji_folder=values
    try:
        if(os.path.isdir(emoji_folder)): #checks if emoji folder is a directory
            l = os.listdir(emoji_folder) 
            num_files=len(l) #gets length of emoji folder
            image_vals={}
            counter=0 #shows user which file is being processed
            for name in l: # for each emoji in folder
                counter+=1 #increment counter
                print("Processing "+name+" file "+str(counter)+" of "+str(num_files))
                img=(emoji_folder+'/'+name) #get current emoji
                img = cv2.imread(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = img.reshape((img.shape[0] * img.shape[1],3))
                cluster = KMeans(n_clusters=3) #cluster emoji
                cluster.fit(img)
                lab = np.arange(0, len(np.unique(cluster.labels_)) + 1)
                (h_gram, _) = np.histogram(cluster.labels_, bins=lab)
                h_gram = h_gram.astype("float")
                h_gram /= h_gram.sum()
                list_colors = [] #list of main emoji colors
                for (match, color) in zip(h_gram, cluster.cluster_centers_):
                    rgb = [] #list of rgb
                    for val in color:
                        val = round(float(val))
                        rgb.append(val)
                    list_colors.append({'percent':round(float(match),2),'rgb':rgb})
                for i in range(len(list_colors)):
                    val = [] #holds clusters
                    delta = 3 
                    while len(val) < 1: #hit api to get most colors
                        emoji_color_cluster = {'r':list_colors[i]['rgb'][0], 'g':list_colors[i]['rgb'][1], 'b':list_colors[i]['rgb'][2],'d':delta}
                        r = requests.get('http://cs.mwsu.edu/~griffin/color-api/', params=emoji_color_cluster)
                        val=r.json() #save colors
                        delta += 3 
                    list_colors[i]['named_data'] = val #save colors
                p=list_colors[0]["percent"]
                dist=1
                for color in list_colors[0]["named_data"]["result"]: #get names of colors and percentages
                    if(color["dist"]<dist):
                        dist=color["dist"]
                        c_name=color["name"]
                image_vals[name]=[]
                image_vals[name].append({c_name:p})
                p1=list_colors[1]["percent"]
                dist=1
                for color in list_colors[1]["named_data"]["result"]: #get names of colors and percentages
                    if(color["dist"]<dist):
                        dist=color["dist"]
                        c_name=color["name"]
                if(p>p1):
                    image_vals[name].insert(1,{c_name:p1})
                else:
                    image_vals[name].insert(0,{c_name:p1})
                p2=list_colors[2]["percent"]
                dist=1
                for color in list_colors[2]["named_data"]["result"]: #get names of colors and percentages
                    if(color["dist"]<dist):
                        dist=color["dist"]
                        c_name=color["name"]
                if(p>p2 and p1>p2):
                    image_vals[name].insert(2,{c_name:p2})
                elif(p2>p and p2>p1):
                    image_vals[name].insert(0,{c_name:p2})
                else:
                    image_vals[name].insert(1,{c_name:p2})
            f=open("processed_emojis.json",'w') #open new file to write dict to
            f.write(json.dumps(image_vals)) #write dict to
            f.close() 
            print("All emojis have been processed!") #success message    
            print("A new file has been created with all the info.")                    
    except: # error message
        print("An error has occured, check my GitHub documentation for command line specifications")

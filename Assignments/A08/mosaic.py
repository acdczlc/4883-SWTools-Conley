#Zac Conley
# A08-Mosaic-Mosaic.py
#This program creates a mosaic of a pic using emojis
import os
import sys
import requests #hits api
import json
from difflib import SequenceMatcher #used to guess best color
from PIL import Image, ImageDraw, ImageFont, ImageFilter

#finds the closest emoji to the current color
#accepts a color json file and the input folder name
#returns path to an emoji
def find_emoji(color):
    emoji="" #matched emoji
    match=0 
    emoji2="" #matched emoji
    match2=0
    color1=""
    dist1=100 #distance between colors
    color2=""
    dist2=100
    bestguess="" #guess based on string matching
    guess_color=1 
    with open('processed_emojis.json') as f:
        data = json.load(f)
    for result in color["result"]:
        if(result["dist"]<dist1):
            dist2=dist1 #saves distance to second color before overwriting with new
            color2=color1 #closer color
            dist1=result["dist"] #overwrite
            color1=result["name"]
        elif(result["dist"]<dist2):
            dist2=result["dist"]
            color2=result["name"]
    for image,values in data.items():
        for item in values:
            for colors,value in item.items():
                if(colors == color1 and value>match): #emoji contains closer match
                    emoji=image #save emoji
                    match=value #save percentage
                elif(colors == color2 and value>match2):
                    emoji2=image
                    match2=value    
                elif(emoji=="" and emoji2==""): #if there is no exact match, takes a guess based on name
                    guess_per= SequenceMatcher(None, colors, color1).ratio()
                    if(guess_per<guess_color):
                        bestguess=image
                        guess_color=guess_per
                    guess_per=SequenceMatcher(None, colors, color2).ratio()
                    if(guess_per<guess_color):
                        bestguess=image
                        guess_color=guess_per 
    if(emoji=="" and emoji2==""): #if there is no exact match, take a guess
        return bestguess
    else:
        fin_match=max(match,match2) #return exact match
        if(fin_match==match):
            return emoji
        elif(fin_match==match2):
            return emoji2

if __name__=='__main__':
    print("\nZac Conley")
    print("A08-Mosaic-Mosaic.py")
    print("This program creates a mosaic of a pic using emojis \n")
    print("This will take a while!")
    print("if you wish to speed up the process you can increase the chunk size to decrease the quality!")
    args = {}
    output="" #no output default
    image="hurricane.png" #default image
    folder="emojis" #default folder
    emoji_size=16 #default 16 emoji size
    chunk_size=4
    for arg in sys.argv[1:]: # get arguments from command line
        f_type,value = arg.split('=')
        if(f_type=="image"):
            image=value
        elif(f_type=="input_folder"):
            folder=value
        elif(f_type=="size"):
            chunk_size=int(value)
        elif(f_type=="output_folder"):
            output=value
    try:
        newimg = Image.open(image) #opens the image
        newimg=newimg.convert('RGB') #get rid of alpha channel
        width,height = newimg.size #save dimensions
        pix=list(newimg.getdata()) # list of all pixels
        newimg=newimg.convert('RGBA').resize((width*emoji_size,height*emoji_size))
        count=0 #current pixel in pic
        x=0 #width
        y=0 #height
        while(y<height):
            while(x<width):
                pixel_rgb = {'r':pix[count][0], 'g':pix[count][1], 'b':pix[count][2],'d':3} # get current pixel
                pixel_color = requests.get('http://cs.mwsu.edu/~griffin/color-api/', params=pixel_rgb) #hit api
                emoji=find_emoji(pixel_color.json()) #find closest emoji
                emoji=folder+"/"+emoji
                temp=emoji #save emoji so it can be used for whole chunk
                chunk=0 
                while(chunk<chunk_size): #foreach emoji in chunk paste the same emoji
                    emoji=Image.open(temp)
                    emoji=emoji.convert('RGBA').resize((emoji_size,emoji_size))
                    newimg.paste(emoji,(x*emoji_size,y*emoji_size),emoji) #add emoji to pic
                    if(x<width): #if using a large chunk size, this will prevent error
                        count+=1
                    x+=1 #increment width
                    chunk+=1
            x=0 #reset width
            y+=1 #increment to next row
        name,dot = image.split('.') #gets name of file and the post dot extension
        if(not(os.path.isdir(output))):
            f_name = name+"mosaic."+dot
            newimg.save(f_name)
        else:
            newimg.save(output+"/"+name+"mosaic."+dot) #save mosaic in output folder
        print("File saved!")
    except:
        print("An error has occurred with your input. Please check the github documentation")

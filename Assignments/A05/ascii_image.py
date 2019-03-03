import os.path
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

#Zac Conley
#Text image A04
#Program turns image into an image made from text

#This function converts an image into a text image
#accepts 4 arguments that give the pic,newpic,font,and font size
def textImage(**kwargs):
    Unichars = [ 'g', 'l', 'f', 'd', 'j', 'c', 'a','m', 'i', 'n', 'k'] #chars that represent chars from font
    print("Creating new image, please be patient.")
    pic = kwargs.get('image')
    newimage = kwargs.get('newimage')   
    f=kwargs.get('font') #get arguments
    fsize=kwargs.get('fsize')
    im = Image.open(pic)
    im=im.convert('RGB') #get rid of alpha channel
    im.show(title=pic) # show original pic
    w,h = im.size
    fs = ImageFont.truetype(f, fsize) #save font
    newImg = Image.new('RGB', (w*fsize//2,h*fsize//2), (255,255,255)) #make new image
    drawOnMe = ImageDraw.Draw(newImg)
    for x in range(w): #go through pixels and place colored text in new image
        for y in range(h): 
            (red,green,blue)=im.getpixel((x,y))
            Unichar=int((red+green+blue)/3)//25
            drawOnMe.text((x*fsize//2,y*fsize//2), Unichars[Unichar], font=fs, fill=(red,green,blue))
    newImg.show(title=newimage) #show and save new image
    newImg.save(newimage)

if __name__=='__main__':
    print("Zac Conley")
    print("Text image - A04")
    print("Program turns image into an image made from text")
    source = os.path.dirname(os.path.abspath(__file__)) #where this file is located
    if(len(sys.argv)==5): #if 4 arguments recieved
        image =source+sys.argv[1] #get arguments
        newimage=source+sys.argv[2]
        font=sys.argv[3]
        fsize=int(sys.argv[4])
    else: #defaults
        image=source+'/input_images/hurricane.png'
        newimage=source+'/output_images/hurricane.png'
        font=source+'/AfricanEggs.ttf'
        fsize=11
    try: #try to convert image
        textImage(image=image,newimage=newimage,font=font,fsize=fsize)
    except: 
        print("An error has occurred. Please ensure you have all files, and that you typed in the correct syntax.")

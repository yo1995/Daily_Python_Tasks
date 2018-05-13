from PIL import Image
import os
import os.path  
import sys
 
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('gbk'))
    elif os.path.isdir(dir):  
        for s in os.listdir(dir):
            #if s == "xxx":
                #continue
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)  
    return fileList

# path = os.getcwd()
fname = raw_input("Please input the dir: (example: GIF)\n")
path = '[The path of your photo album]' +  fname
lcur = len(fname) + 2

small_path = (path[:-1] if path[-1]=='/' else path) + '_m'
print small_path
if not os.path.exists(small_path):  
    os.mkdir(small_path)
for root, dirs, files in os.walk(path):  
    for f in files:  
        fp = os.path.join(root, f)
        img = Image.open(fp)
        w, h = img.size
        savepath = os.path.join(small_path, f)
        if os.path.isfile(savepath + fp[len(savepath)-1:]):
            print u'existing, not writing'
        else :
          if w>h:
              div = float(w)/h
              h = int(320/div)
              img.resize((320, h),Image.ANTIALIAS).save(os.path.join(small_path, f))
          else:
              div = float(h)/w
              w = int(320/div)
              img.resize((w,320),Image.ANTIALIAS).save(os.path.join(small_path, f))

l = len(path)
list = GetFileList(path, [])
with open ('result.txt','wb') as result:
    for e in list:
      e = e[l-lcur+1:]
      e =  '- image_title: ' + e[lcur:-4] \
      + '\r\n  image_path: "https://raw.githubusercontent.com/yo1995/page-backup/master' + e \
      +  '" \r\n  thumb_path: "https://raw.githubusercontent.com/yo1995/page-backup/master' + e[:lcur-1] + '_m/'+ e[lcur:] + '"'
      e = e.replace("\\", '/')
      result.write(e + '\r\n')

raw_input('finished ! press any key to exit')

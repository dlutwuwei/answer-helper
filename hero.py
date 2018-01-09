import urllib.request, sys,base64,json,os,time,pyperclip,baiduSearch
from PIL import Image
from os.path import isfile, join, abspath, dirname

root_path = dirname(abspath(__file__))
print(root_path)

start = time.time()
os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png") 
os.system("adb pull /sdcard/screenshot.png " + root_path)  
host = 'http://text.aliapi.hanvon.com'
path = '/rt/ws/v1/ocr/text/recg'
method = 'POST'
# appcode = '39f04e36453441bb95db5f907c07af21'
# querys = 'code=74e51a88-41ec-413e-b162-bd031fe0407e'
appcode = ''
querys = ''
bodys = {}
url = host + path + '?' + querys


im = Image.open(join(root_path,'screenshot.png'))

img_size = im.size
w = im.size[0]
h = im.size[1]
print("xx:{}".format(img_size))

region = im.crop((70,200, w-70,700))
region.save(join(root_path, 'crop_test1.png'))



f=open(join(root_path, 'crop_test1.png'),'rb')
ls_f=base64.b64encode(f.read())
f.close()
s = bytes.decode(ls_f) 

bodys[''] = "{\"uid\":\"118.12.0.12\",\"lang\":\"chns\",\"color\":\"color\",\"image\":\""+s+"\"}"
post_data = bodys['']
request = urllib.request.Request(url, str.encode(post_data))
request.add_header('Authorization', 'APPCODE ' + appcode)

request.add_header('Content-Type', 'application/json; charset=UTF-8')
request.add_header('Content-Type', 'application/octet-stream')
response = urllib.request.urlopen(request)
content = response.read()
if (content):
   
    decode_json = json.loads(content)
    print(decode_json['textResult'])


#pyperclip.copy(''.join(decode_json['textResult'].split()))

keyword = ''.join(decode_json['textResult'].split())    #识别的问题文本

convey = 'n'

if convey == 'y' or convey == 'Y':
    results = baiduSearch.search(keyword, convey=True)
elif convey == 'n' or convey == 'N' or not convey:
    results = baiduSearch.search(keyword)
else:
    print('输入错误')
    exit(0)
count = 0
for result in results:
    #print('{0} {1} {2} {3} {4}'.format(result.index, result.title, result.abstract, result.show_url, result.url))  # 此处应有格式化输出
	print('{0}'.format(result.abstract))  # 此处应有格式化输出
	count=count+1
	if(count == 2):
		break

end = time.time()
print('程序用时：'+str(end-start)+'秒')

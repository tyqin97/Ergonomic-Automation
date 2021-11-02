import win10toast
import mysql.connector
import os, requests
from PIL import Image
from pathlib import Path

# Get current working directory path
filePath = os.getcwd()

# Try checking whether file exists in the directory
# and create one if not. At last change current directory.
try:
    os.makedirs(filePath + "\Img")
except FileExistsError:
    pass
finally:
    os.chdir(filePath + '\Img')

def GetConnection():
    mydb = mysql.connector.connect(
        host="192.168.2.97",
        user="Greatech",
        password="Greatech@123",
        database="ergonomic")
    return mydb

def GetFileName(web_url):
    getFileName = web_url.split(sep="/")
    fileName = getFileName[-1:][0]
    return fileName

def CheckExist(mydb, web_url):
    fileName = GetFileName(web_url)
    cursor = mydb.cursor()

    sql = 'SELECT img_path FROM content WHERE path_url = %s'
    val = (web_url,)
    cursor.execute(sql,val)
    response = cursor.fetchall()
    checkLocal = os.path.isfile(response[0][0])

    if response[0][0] == "" or checkLocal == False:
        img_name = ImageDownload(web_url, fileName)
        img_name = (img_name)
        sql1 = 'UPDATE content SET img_path = %s WHERE path_url = %s'
        val1 = (img_name, web_url)
        cursor.execute(sql1, val1)
        mydb.commit()
        return img_name
    else:
        return response[0][0]

def CheckSequence(mydb):
    cursor = mydb.cursor()
 
    cursor.execute('SELECT last_run FROM seq_check')
    last_run = cursor.fetchone()
    number = last_run[0] + 1

    sql = 'SELECT content_id FROM sequence WHERE no = %s'
    val = (number,)
    cursor.execute(sql, val)
    content_id = cursor.fetchone()

    if content_id is None:
        value = 1
    else:
        value = content_id[0]

    
    sql1 = 'SELECT title, content, path_url FROM content WHERE id = %s'
    val1 = (value,)
    cursor.execute(sql1, val1)
    data = cursor.fetchone()
    title, content, web = data
    path = CheckExist(mydb, web)

    sql2 = 'UPDATE seq_check SET last_run = %s WHERE last_run = %s'
    val2 = (value, last_run[0])
    cursor.execute(sql2, val2)
    mydb.commit()

    Notifier(title, content, 10, path)

def IcoConvert(file_name):
    content_name = file_name.split(sep=".")
    img = Image.open(file_name)
    img.save(str(content_name[0]+'.ico'))
    os.remove(file_name)
    data = str(content_name[0]+'.ico')
    return data

def ImageDownload(web_url, img_name):
    page = requests.get(web_url)
    f_ext = os.path.splitext(web_url)[-1]

    if img_name != "*.ico":
        with open(img_name, 'wb') as f:
            f.write(page.content)
        img_name = IcoConvert(img_name)
    else:
        with open(img_name, 'wb') as f:
            f.write(page.content)
    return img_name

def Notifier(title, content, duration, icon_path):
    n = win10toast.ToastNotifier()
    n.show_toast(title, content, duration = duration, icon_path = icon_path)

try:
    CheckSequence(GetConnection())
except:
    print("ERROR IN APPS")
finally:
    pass
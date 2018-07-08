import os, re, time, memcache
from flask import Flask, render_template, request, redirect, session
from random import randint
from datetime import datetime
import sys, csv
import pymysql
from werkzeug.utils import secure_filename
#global file_name
ACCESS_KEY_ID = 'AKIAJSGMTKP4JEI7NJBA'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'shilpashree-s3'

reload(sys)
sys.setdefaultencoding('utf-8')
hostname = 'picturealbumdb.cckoj3pyomxt.us-east-2.rds.amazonaws.com'
username = 'shilpa'
password = 'admin123'
database = 'PictureAlbumDB'
myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database, autocommit = True, cursorclass=pymysql.cursors.DictCursor, local_infile=True)

print "Database Connected"

application = Flask(__name__)
app = application
app.secret_key = 'pass'


UPLOAD_FOLDER = '/home/ubuntu/flaskapp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
query= "select * from all_week limit"
@app.route("/")
def hello():#For displaying the first page
    return render_template("filehandle.html")

@app.route("/csv_upload", methods = ['POST'])
def csv_upload():#For uploading the file
	#global file_name
		csv_file = request.files['file_upload']	
		file_name=csv_file.filename
		session['file_name']=file_name
		filename = secure_filename(csv_file.filename)
		csv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		drop_query="drop table IF EXISTS "+ file_name[:-4]
		with myConnection.cursor() as cursor:
			cursor.execute(drop_query)
			myConnection.commit()
		column_name="("
		abs_filename=UPLOAD_FOLDER+file_name
		with open(abs_filename, 'r') as f:
			reader = csv.reader(f)
			for row in reader:
				line=row
				break
		for i in line:
			column_name+=i+" VARCHAR(50),"
		query="Create table if not exists " + file_name[:-4]+column_name+" sr_no INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(sr_no));"
		starttime = time.time()
		with myConnection.cursor() as cursor:
			cursor.execute(query)
			myConnection.commit()
		cursor.close()
		insert_str="""LOAD DATA LOCAL INFILE '"""+abs_filename+ """' INTO TABLE """+ file_name[:-4] +""" FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"""
		with myConnection.cursor() as cursor:
			cursor.execute(insert_str)
			myConnection.commit()
		endtime = time.time()
		count_str="SELECT count(*) FROM "+ file_name[:-4]
		with myConnection.cursor() as cursor:
			cursor.execute(count_str)
			result=cursor.fetchall()
		totalsqltime = endtime - starttime 
		return render_template("mainfile.html",count=result[0]['count(*)'],rdstime0=totalsqltime)

@app.route('/sqlrestriclatlong', methods=['POST'])
def linefocus():
    	#mc = memcache_connect()
	print "entering"
    	logi1 = request.form['val1']
    	logi2 = request.form['val2']
    	lati1 = request.form['val3']
    	lati2 = request.form['val4']
    	locquery="Select count(*), latitude, longitude from Starbucks where longitude between '-117.84' and '-118.84' and latitude between '34.03' and '35.03';"
    	starttime = time.time()
		print "before connection"
		with myConnection.cursor() as cursor:
			cursor.execute(locquery)
			for row in cursor:
				result1.append(locquery)
		x1 = [x['count(*)'] for x in result1]
		x2 = [x['latitude'] for x in result1]
		x3 = [x['longitude'] for x in result1]
		endtime = time.time()
		totalsqltime = endtime - starttime
		return render_template('lineWithFocusChart.html', count_var=x1,lat=x2,longi=x3 )

@app.route('/barplotting',methods=['POST'])
def barplotting():
    	less_than = request.form['max']

    	query1 = "select count(distinct city),state from USZipcodes group by state having count( distinct county) <"+less_than

    	result1 = []
		with myConnection.cursor() as cursor:
	    	cursor.execute(query1)
	    	for row in cursor:
	        	result1.append(row)
    	x1 = [x['count(distinct city)'] for x in result1]
    	x2 = [x['state'] for x in result1]
    	result2 = []
    	for p in x2:
        	result2.append(p)

    	print(result2)
    	return render_template("BarChart.html",x1= x1,x2=result2)
		
@app.route('/pieplotting',methods=['POST'])
def pieplot():
    	less_than = request.form['max']

    	query1 = "select count(distinct city),state from USZipcodes group by state having count( distinct county) <"+less_than

    	result1 = []
		with myConnection.cursor() as cursor:
	    	cursor.execute(query1)
	    	for row in cursor:
	        	result1.append(row)
    	x1 = [x['count(distinct city)'] for x in result1]
    	x2 = [x['state'] for x in result1]
    	result2 = []
    	for p in x2:
        	result2.append(p)

    	print(result2)
    	return render_template("PieChart.html",x1= x1,x2=result2)
		
@app.route('/multibar',methods=['POST'])
def multibar():
    	less_than = request.form['max']

    	query1 = "select count(distinct city),state from USZipcodes group by state having count( distinct county) <"+less_than

    	result1 = []
		with myConnection.cursor() as cursor:
	    	cursor.execute(query1)
	    	for row in cursor:
	        	result1.append(row)
    	x1 = [x['count(distinct city)'] for x in result1]
    	x2 = [x['state'] for x in result1]
    	result2 = []
    	print result2
    	for p in x2:
        	result2.append(p)

    	print(result2)
    	return render_template("multiBarHorizontalChart.html",x1= x1,x2=result2)

@app.route('/scatterplot', methods=['POST'])
def scatterplot():
		print "entering"
    	logi1 = request.form['val1']
    	logi2 = request.form['val2']
    	lati1 = request.form['val3']
    	lati2 = request.form['val4']
    	locquery="Select count(*), latitude, longitude from Starbucks where longitude between '-117.84' and '-118.84' and latitude between '34.03' and '35.03';"
    	starttime = time.time()
		print "before connection"
		with myConnection.cursor() as cursor:
			cursor.execute(locquery)
			for row in cursor:
				result1.append(locquery)
		x1 = [x['count(*)'] for x in result1]
		x2 = [x['latitude'] for x in result1]
		x3 = [x['longitude'] for x in result1]
		endtime = time.time()
		totalsqltime = endtime - starttime
		return render_template('scatterChart.html', count_var=x1,lat=x2,longi=x3 )
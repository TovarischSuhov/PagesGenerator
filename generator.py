from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
from os import listdir, system
import argparse
import re
import json
import time
import sys
import codecs
import zipfile
import xml.dom.minidom as xmlp

IMG_REGEX = re.compile(r'(.*)\.jpe?g',re.IGNORECASE | re.DOTALL)
DOCX_REGEX = re.compile(r'.*\.docx',re.IGNORECASE | re.DOTALL)
JSON_REGEX = re.compile(r'config\.json',re.IGNORECASE | re.DOTALL)

def RenderTemplate(contents, args):
	env = Environment()
	env.loader = FileSystemLoader('.')
	template = env.get_template(contents)
	result = template.render(args)
	return result

def ParseDocx(path, config):
	tempname = str(time.time())

	z=zipfile.ZipFile(path, 'r')
	z.extractall('/tmp/' + tempname)
	z.close()

	app_xml = xmlp.parse('/tmp/'+ tempname +'/word/document.xml')
	documents = app_xml.getElementsByTagName("w:document")
	all_array = []

	for document in documents:
    		bodies = document.getElementsByTagName("w:body")
    		for body in bodies:
        		tables = body.getElementsByTagName("w:tbl")
        		for table in tables:
            			rows = table.getElementsByTagName("w:tr")
            			for row in rows:
                			columns = row.getElementsByTagName("w:tc")
                			temp = []
                			for column in columns:
                    				paragraphs = column.getElementsByTagName("w:p")
                    				for par in paragraphs:
                        				contents = par.getElementsByTagName("w:r")
                        				for cont in contents:
                            					text = cont.getElementsByTagName("w:t")
                            					for i in text:
                                					temp.append(i.firstChild.data)
                			all_array.append(temp)
	j=0
	ls=[]
	for i in all_array:
    		if j==0:
        		head=i
    		elif i!=[]:
        		l=0
        		temp={}
        		for k in head:
				if l == config['what']: 
            				temp['what'] = i[l]
				if l == config['where']: 
					temp['where'] = i[l]
				if l == config['when']: 
					temp['when'] = i[l]
            			l+=1
        		ls.append(temp)
		j+=1
	return ls

def ParseJson(path):
	fin = codecs.open(path, "r", "utf-8")
	s=''
	text = s.join(fin.readlines())
	result = json.loads(text)
	fin.close()
	return result

def ParsePics(pics_list, path, outpath):
	pics_dir=outpath + "img/"
	result = []
	counter=0
	current_time = time.localtime()
        namebase = str(current_time.tm_year) + str(current_time.tm_mon) + str(current_time.tm_mday)
	for i in pics_list:
		temp = {}
		temp["description"] = IMG_REGEX.sub(r'\1',i)
		newname = namebase + str(counter) + ".jpg"
		temp["path"] = "img/" + newname
		system("convert " + path + '/' + i  + " -resize 2000x600 " + pics_dir + newname) #Put resize
		result.append(temp)
		counter+=1

	return result

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--path", action = "store", required = True, help = \
		"Sets path to direcotry with input data")
	parser.add_argument("-c", "--config", action = "store", default = "generator.conf",\
		help = "Sets path to config, contains archive list")
	parser.add_argument("-o", "--output", action = "store", default = "/var/www/html/",\
		help = "Sets path to write output html")
	args = parser.parse_args()
	
	pics_list = []
	path_to_docx = ''
	path_to_json = ''
	files = listdir(args.path)
	for i in files:
		if IMG_REGEX.match(i):
			pics_list.append(i)
			continue
		if DOCX_REGEX.match(i):
			path_to_docx = args.path + '/' + i
			continue
		if JSON_REGEX.match(i):
			path_to_json = args.path + '/' + i
		
	
	config = ParseJson(args.config)
	if not path_to_json or not path_to_docx:
		exit(1)
	page_args = {};
	page_args["photos"] = ParsePics(pics_list, args.path, args.output)
	temp = ParseJson(path_to_json)
	page_args["table"] = ParseDocx(path_to_docx, temp['columns'])
	page_args["day_name"] = temp["day_name"]
	page_args["facts"] = temp["facts"]
	try:
		previous_day = config.pop()
		page_args["previous_day"] = previous_day["url"]
		config.append(previous_day)
	except:
		page_args["previous_day"] = ''
	page_contents = RenderTemplate("page.j2", page_args)
	
	current_time = time.localtime()
	pagename = str(current_time.tm_year) + str(current_time.tm_mon) + str(current_time.tm_mday) + ".html"
	config.append({"url" : pagename, "description" : page_args["day_name"]})
	archive_contents = RenderTemplate("archive.j2", {"pages_list" : config})
	fout = codecs.open(args.config,"w", "utf-8")
	fout.write(json.dumps(config))
	fout.close()

	fpage = codecs.open(args.output + pagename, "w", "utf-8")
	fpage.write(page_contents)
	fpage.close()
	
	fpage = codecs.open(args.output + "archive.html", "w", "utf-8")
	fpage.write(archive_contents)
	fpage.close()

	fpage = codecs.open(args.output + "index.html", "w", "utf-8")
	fpage.write(u'<html><head><meta http-equiv="refresh" content="0; url='+ pagename +'"/></head></html>')
	fpage.close()

if __name__ == "__main__":
	sys.exit(main())

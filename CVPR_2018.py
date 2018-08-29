'''
  This script downloads the papers from CVPR 2018 and creates a CSV file with institution and the papers published by those institutions. 
'''

import PyPDF2
import urllib2
import requests
from bs4 import BeautifulSoup
import glob 
import pandas as pd 

pdf_link = []
title_link = []
url = 'http://openaccess.thecvf.com/CVPR2018.py'
folder_path = '/Users/Janjua/Desktop/CVPR_Institute/'

def parse_pdf(file):
	inst_list_ = []
	pdfReader = PyPDF2.PdfFileReader(file)
	pagenbrs = pdfReader.numPages
	pgObj = pdfReader.getPage(0)
	extracted_text = (pgObj.extractText())
	pageOne = ''
	for i in extracted_text:
		try:
			pageOne += i
		except:
			pass
	info_split = pageOne.split()
	for i in info_split:
		if 'University' in i or 'Facebook' in i or 'Google' in i or 'School' in i or 'Center' in i or 'Institute' in i or 'Tech' in i or 'Company' in i or 'Centre' in i or 'Research' in i or 'Group' in i or 'Department' in i or 'Labs' in i or 'Lab' in i:
			inst_list_.append(i)	
	return inst_list_

def get_pdf():
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	titles_ = soup.find_all('dt', attrs={'class':'ptitle'})
	pdfs_ = soup.find_all('dd')
	for i in pdfs_:
		if '[<a href' in str(i):
			link_ = str(i).split('\n')[1].split('=')[1].split(">")[0].replace('"','')
			comp_link = 'http://openaccess.thecvf.com/'+link_
			pdf_link.append(comp_link)
	for i in titles_:
		title = str(i).split('>')[3].split('<')[-2]
		title_link.append(title)

def download_file(download_url, title):
    response = urllib2.urlopen(download_url)
    file = open("{}.pdf".format(title), 'wb')
    file.write(response.read())
    file.close()
    print("Completed {}".format(title))

def bulk_download():
	get_pdf()
	assert len(pdf_link) == len(title_link)
	for xi in range(len(pdf_link)):
		download_file(pdf_link[xi], title_link[xi])
		
def enum_files():
	bulk_download()
	wr_file = open('stats_cvpr_2018.csv', 'w')
	wr_file.write('Title'+','+'Institution'+'\n')
	for i in glob.glob(folder_path+"*.pdf"):
		title = i.split('/')[-1].split('.')[0]
		parsed_info = str(parse_pdf(i)).replace('u','').replace('[', '').replace(']', '').replace("'", '')
		print(parsed_info)
		wr_file.write(title+',')
		wr_file.write(parsed_info)
		wr_file.write('\n')
	wr_file.close()
		
enum_files()

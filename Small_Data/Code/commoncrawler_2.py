#mkheraja
#vaidehia
# Reference: https://www.bellingcat.com/resources/2015/08/13/using-python-to-mine-common-crawl/
# We have used the code from the above site for domain related to our keyword "movies" and index = 2019 in order to get recent articles.
import requests
import argparse
import time
import json
import StringIO
import gzip
import csv
import codecs
import re
import string
#import textcleaner as tc
import nltk
from stop_words import get_stop_words
from nltk.corpus import stopwords
#     from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

domain4 = "imdb.com"
domain3 = "rottentomatoes.com"
domain1 = "Movies.com"
domain2 = "netflix.com"
# We have experimented with different domains to get relevant articles and stopped our search when required limit of 500 articles is reached.

# list of available indices
index_list = ["2019-04", "2019-09", "2019-13"]
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
stop_words.add('said')
stop_words.add('mr')
stop_words.add('ms')
stop_words.add('like')
stop_words.add('also')
stop_words.add('one')
stop_words.add('two')
stop_words.add('would')
stop_words.add('first')
stop_words.add('\t')
#
# Searches the Common Crawl Index for a domain.
#
def search_domain(domain):

    record_list = []
    
    print "[*] Trying target domain: %s" % domain
    
    for index in index_list:
        
        print "[*] Trying index %s" % index
#         http://index.commoncrawl.org/CC-MAIN-2015-06?url=%s&matchType=movie&output=json
        cc_url  = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s&matchType=domain&output=json" % domain
        
        response = requests.get(cc_url)
        
        if response.status_code == 200:
            
            records = response.content.splitlines()
            
            for record in records:
                record_list.append(json.loads(record))
            
            print "[*] Added %d results." % len(records)
            
    
    print "[*] Found a total of %d hits." % len(record_list)
    
    return record_list        

	
def download_page(record):

    offset, length = int(record['offset']), int(record['length'])
    offset_end = offset + length - 1

    prefix = 'https://commoncrawl.s3.amazonaws.com/'

    resp = requests.get(prefix + record['filename'], headers={'Range': 'bytes={}-{}'.format(offset, offset_end)})
    
    # The page is stored compressed (gzip) to save space
    # We can extract it using the GZIP library
    raw_data = StringIO.StringIO(resp.content)
    f = gzip.GzipFile(fileobj=raw_data)
    
    # What we have now is just the WARC response, formatted:
    data = f.read()
    
    response = ""
    
    if len(data):
        try:
            warc, header, response = data.strip().split('\r\n\r\n', 2)
        except:
            pass
            
    return response

#
# Extract links from the HTML  
#
def extract_external_links(html_content,link_list):

    parser = BeautifulSoup(html_content, features="html.parser")
        
    links = parser.find_all("a")
    
    if links:
        
        for link in links:
            href = link.attrs.get("href")
            
            if href is not None:
                
                if (domain1 not in href) or (domain2 not in href) or (domain3 not in href):
                    if href not in link_list and href.startswith("http"):
                        print "[*] Discovered external link: %s" % href
                        link_list.append(href)

    return link_list

record_list1 = search_domain(domain1)
record_list2 = search_domain(domain2)
record_list3 = search_domain(domain3)
record_list4 = search_domain(domain4)

record_list = record_list1+record_list2+record_list3+record_list4
link_list   = []
count = 1

for record in record_list:
  #print "record: "+str(record)
  #time.sleep(2)
  html_content = download_page(record)
  soup = BeautifulSoup(html_content)
  elements = soup.find_all("small")
  for element in elements:
    element.decompose()
  elements = soup.find_all("i")
  for element in elements:
    element.decompose()
  elements = soup.find_all("br")
  for element in elements:
    element.decompose()
  elements = soup.find_all("sup")
  for element in elements:
    element.decompose()
  #elements = soup.find_all("em")
  #for element in elements:
    #element.decompose()
  print "[*] Retrieved %d bytes for %s" % (len(html_content),record['url'])
  #f_raw = open('html_content_raw'+str(count)+'.txt','a+')
  #f_raw.write(html_content+"\n")
  #f_raw.close()
  while (html_content.find("<p ") != -1 or html_content.find("<p>") != -1):
    first = html_content.find("<p")
    #print "first: "+str(first)
    #print html_content[first:first+100]
    if (html_content[first+2] == ">" or html_content[first+2] == " "):
      #time.sleep(2)
      last = html_content.find("</p>")
      #print "last: "+str(last)
      #time.sleep(2)
      p_content_p = html_content[first : last+4]
      temp = p_content_p.find(">")
      #print "temp: "+str(temp)
      #time.sleep(2)
      p_content = p_content_p[temp+1 : -4]
      #print "p_content_p: "+p_content_p
      #print "p_content: "+p_content
      #time.sleep(2)
      while(p_content.find("<a") != -1):
        #print "a ref in pcontent"
        rm_1 = p_content.find("<a")
        #print "rm1: "+str(rm_1)
        rm_2 = p_content.find("</a>")
        #print "rm2: "+str(rm_2)
        rm_str = p_content[rm_1:rm_2+4]
        #print "rm_str: "+rm_str
        p_content = p_content.replace(rm_str,"")
        #print "p content after <a> removal = "+p_content
        #time.sleep(10)
      while(p_content.find("<em") != -1):
        #print "a ref in pcontent"
        rm_1 = p_content.find("<em")
        #print "rm1: "+str(rm_1)
        rm_2 = p_content.find("</em>")
        #print "rm2: "+str(rm_2)
        rm_str = p_content[rm_1:rm_2+5]
        print "rm_str: "+rm_str
        p_content = p_content.replace(rm_str,"")
        print "p content after <em> removal = "+p_content
        #time.sleep(10)
      #while (p_content.find("<br>" != -1)
             #p_content.replace("<br>","")
      #while(p_content.find("<i>") != -1):
       # #print "a ref in pcontent"
        #rm_1 = p_content.find("<i>")
        ##print "rm1: "+str(rm_1)
   #     rm_2 = p_content.find("</i>")
    #    #print "rm2: "+str(rm_2)
     #   rm_str = p_content[rm_1:rm_2+4]
      #  print "rm_str: "+rm_str
       # p_content = p_content.replace(rm_str,"")
        #print "p content after <i> removal = "+p_content
        ##time.sleep(10)
      if("movie" in p_content or "cinema" in p_content or "film" in p_content or "action" in p_content or "comedy" in p_content or "crime" in p_content or "drama" in p_content or "fantasy" in p_content or "sci-Fi" in p_content or "scifi" in p_content or "animated" in p_content or "animation" in p_content or "anime" in p_content or "horror" in p_content or "ghost" in p_content or "romance" in p_content or "social" in p_content or "thriller" in p_content):
        #print "writing "+p_content+" in html content file"
        ##if("movie" in p_content):
        #f = open('html_content_clean'+str(count)+'.txt','a+')
        inner_contents=p_content.strip().lower()
        #print "inner_contents: "+inner_contents
        #time.sleep(2)
        #actualString = inner_contents.decode("utf-8",'ignore')
        #print "actualString: "+actualString
        #time.sleep(2)
        inner_contents= " ".join(inner_contents.split())
        #print "After removing blanks: "+inner_contents
        stemmed = lemmatizer.lemmatize(inner_contents)
        #print "stemmed: "+stemmed
        #time.sleep(2)
        result=re.sub('[\W\_]',' ',stemmed) #Remove special chars
        #print "result after removing special characters: "+result
        #time.sleep(2)
        result = re.sub(" \d+", " ", result) #Remove numbers
        #print "result after removing numbers: "+result
        #time.sleep(2)
        x=result.split(" ")
        filtered_sentence = [w for w in x if not w in stop_words]
    #                         stemmed = lemmatizer.lemmatize(filtered_sentence)
    #                         porter = PorterStemmer()
    #                         stemmed = [porter.stem(word) for word in filtered_sentence]
        #print "After removing stopwords: "+filtered_sentence
        for x in filtered_sentence:
          #print "x: "+x
          #time.sleep(2)
          with open('html_content_clean_'+str(count)+'.txt','a+') as outputFile:
            if x is not '\u2713':
              outputFile.write(x)
              outputFile.write(' ')
              import os
              statinfo = os.stat('html_content_clean_'+str(count)+'.txt')
              if (statinfo.st_size > 3000):
                count = count + 1
             #time.sleep(2) 
        
        #f.write(p_content+"\n")
        #f.close()
      else:
          print "Not writing "+p_content
          #time.sleep(2)
      html_content = html_content.replace(p_content_p,"")
    else:
      #print "replacing wrong indicator <p"
      html_content = html_content.replace("<p","")
      #time.sleep(2)

  #count = count + 1
  #print "Analysis for this record completed. Now moving to next record."
  #time.sleep(3)    

print "[*] Total external links discovered: %d" % len(link_list)

with codecs.open("%s-links.csv" % domain1,"w",encoding="utf-8") as output:

    fields = ["URL"]
    
    logger = csv.DictWriter(output,fieldnames=fields)
    logger.writeheader()
    
    for link in link_list:
        logger.writerow({"URL":link})
		
with codecs.open("%s-links.csv" % domain2,"w",encoding="utf-8") as output:

    fields = ["URL"]
    
    logger = csv.DictWriter(output,fieldnames=fields)
    logger.writeheader()
    
    for link in link_list:
        logger.writerow({"URL":link})
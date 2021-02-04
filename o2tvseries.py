import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from exceptions import *
from pathlib import Path
import os

base_url = 'https://o2tvseries.co'

# Universal Dictionaries

search_results = []
results_links = {}
driver_dict = {}


def link_parser(link):
	'''
	this function takes a link and runs it online
	using the urllib's request method.
	it parses the given link, find's desired tags,
	and returns them as a list of tags
	'''


	print("\nPlease wait...\n")
	time.sleep(1)

	try:
		page = requests.get(link)
	except (ConnectionError, NewConnectionError):
		print("Please Check Your Conncection!")
	soup = BeautifulSoup(page.content, 'html.parser')
	
	try:
		results = soup.find('ul')
		targets = results.find_all('li')
		# we need a method to handle next paged items eg episodes
		paged = soup.find("ul",class_="pagination")
		paged_tags = paged.find_all('li')
		if len(paged_tags) > 0:
			for i in range(len(paged_tags))[3:]:
				new_link ="https://o2tvseries.co%s" %(paged_tags[i].find('a')['href'])
				page = requests.get(new_link)
				soup = BeautifulSoup(page.content, 'html.parser')
				results = soup.find('ul')
				add_targets = results.find_all('li')

				for l in add_targets:
					targets.append(l)
	except (NameError, AttributeError):
		pass



	return targets

def search(search_term_):
	"""
	search() takes a search term and refines it
	before running it in o2tvseries.co.
	it returns a list results.
	"""
	# converting whatever is searched to a string
	search_term=str(search_term_)
	# in case the search term is a sentence, we need to split it
	p = search_term.split(" ") # thus p is a list of wordss
	if len(p) > 1:
		long_search = search_term.replace(" ", "+")
		search_q = base_url+"/search/?q=%s" %long_search
	else:
		search_q = base_url+"/search/?q=%s" %search_term

	results = link_parser(search_q)

	if "TV" in results[0].text.strip():
		raise KeywordNotFoundError
		
	else:
		for i in results:
			search_results.append(i.text.strip())


	zipped = list(zip(range(1,len(search_results)+1), search_results)) #returns a list of tuples
	# Also check if you can use results links to generate driver_dict instead of search_results
	
	# cleaning driver_dict before use
	driver_dict.clear()
	for num, title in zipped:
		driver_dict[num]=title
	
	for n in range(len(results)):
		results_links[results[n].text.strip()]=results[n].find('a')['href']

	for key, value in driver_dict.items():
		print(key,'.', value.replace('\n',' ')) # replacing unwanted escapes
		# You must not implement replace() higher than here due to key:value check

def get_link(key, dictionary):
	"""
	when you give get_link() function a key and 
	a dictionary from which to get a link(literaly),
	it returns you a full o2tvseries link to work
	with.
	Awesome, right?
	"""


	#key should give us a value from a dictionary
	# this function returns a full link

	if key in list(dictionary.keys()):
		half_link = dictionary[key] 	# returns a value to given key, wwhixh is a half link
		return(base_url+half_link)
	else:
		print("%s not found in %s" %(key,dictionary))
		return

def populate(tags_list, dictionary):
	"""
	this function is used to populate a target 
	dictionary with a given list of tags with
	names as keys and half_links as values
	"""
	#we will get a link eg. referring to a season's page and populate sn_dict
	for n in range(len(tags_list)):
		dictionary[tags_list[n].text.strip()]=tags_list[n].find('a')['href']

def display(source_dict):
	"""
	this simply displays the contents of
	a given dictionary in more user friendly
	visible and numbered lists.
	"""

	# display will be displaying keys in a formarted manner eg season's and we will use global driver_dict
	driver_dict.clear() # emptying it before usage
	key_list=list(source_dict.keys())
	for i in range(len(key_list)):
		driver_dict[i] = key_list[i]

	for key, value in driver_dict.items():
		print(key, '.\t', value.replace('\n', ' '))

'''
def download_all(video_links):

	"""
	simple! 
	Give this a link, or list/tuple
	of links and sit back as they get downloaded!
	"""
	

	for link in video_links:
		""" iterate through all links in video_links downl them 1 by 1 """

		#obtain filename
		file_name = link.split('/')[-1]
		print("Downloading file:%s"%file_name)

		#creating response object;
		r = requests.get(link, stream=True)

		#starting download
		with open(file_name, 'wb') as f:
			for chunk in tqdm(r.iter_content(chunk_size=1024*1024)):
				if chunk:
					f.write(chunk)
				
		print("%s downloaded!\n"%file_name)
	print("All videos downloaded!\n\nThank you for your patience!!!")
	return
'''

#Alternate downl_all
path_var = []
def download_all(link):
	from internetdownloadmanager import Downloader
	
	downloader = Downloader(worker=25, part_size=1000000, resumable=True)

	while True:
		cwd = os.getcwd() # recording the current working directory
		try:
			os.makedirs("Movies/%s_%s" %(path_var[0],path_var[1]))
			os.chdir("Movies/%s_%s" %(path_var[0],path_var[1]))
			break
		except OSError:
			os.chdir("Movies/%s_%s" %(path_var[0],path_var[1]))
			break

	file_name = link.split('/')[-1]
	print("Downloading file:%s"%file_name)

	
	if not os.path.exists(file_name):
		downloader.download(link, file_name)
	elif os.path.exists(file_name+'.resumable'):
		print("resuming %s",file_name)
		downloader.resume(file_name+'.resumable')
		os.remove(file_name+'resumable') # cleaning up
		

	print("\n%s downloaded!\n"%file_name)
	os.chdir(cwd) # returning to the working directory
	
	return

def get_file(link_dict, *pilot):
	'''
	will take a link, parse it if necessary and return a file
	'''
	# Case 1: User selected all episodes
	if len(pilot) == 0:
		print("\nDownloading all...\n")
		video_links = list(link_dict.values())

		for link_ in video_links:
			link = base_url+link_
			r = requests.get(link)
			soup = BeautifulSoup(r.content, 'html.parser')
			down_tag = soup.find(id="download")
			php_link = base_url+down_tag['href']

			down_url = link_verifier(php_link)

			download_all(down_url)

		print("All videos downloaded!\n\nThank you for your patience!!!")


	
	# else, pilot tuple will have (a) number(s) that will direct us in picking links
		
	elif ',' in pilot[0]:
		pilot = pilot[0].replace(','," ").split()
	elif ' ' in pilot[0]:
		pilot = pilot[0].split()
	# elif '-' in pilot[0]:
    # 	# this implies that  a range was given
	# 	l_pilot=list(pilot[0])
	# 	l_pilot.clear()
	# 	for i in range(int(pilot[0][0]), int(pilot[0][2])+1):
    # 			l_pilot.append(i)

	# 	pilot = l_pilot

	for key in pilot:
		print("\nGrabbing selection %s...\n" %key)
		link_key = driver_dict[int(key)]
		link =base_url+link_dict[link_key]
		print("\nPlease Wait...\n")
		r = requests.get(link)
		soup = BeautifulSoup(r.content, 'html.parser')
		down_tag = soup.find(id="download")
		php_link = base_url+down_tag['href']

		down_url = link_verifier(php_link)

		download_all(down_url)

	print("All videos downloaded!\n\nThank you for your patience!!!")



	


def link_verifier(php_link):
	'''
	takes a verifyDownload.php link and does 
	the verification for you.
	it returns a real link with file needed!
	'''
	from selenium import webdriver
	from selenium.webdriver.common.by import By 
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver import Firefox
	from selenium.webdriver.firefox.options import Options
	from selenium.common.exceptions import ElementClickInterceptedException

	# Ensuring geckodriver.exe exists for windows
	if os.name != 'posix':
		webdriver_path = Path("geckodriver.exe")
		opts = Options()
		opts.set_headless()
		assert opts.set_headless	# operating in headless mode
		browser = Firefox( options=opts, executable_path=webdriver_path)
	else:
		webdriver_path = Path("geckodriver", executable_path=webdriver_path)
		opts= Options()
		opts.set_headless()
		browser = Firefox( options=opts)

	print("Generating a real link...\nPlease wait...\n")
	browser.get(php_link)
	while True:
		try:
			browser.find_element_by_name("download").click()
			break
		except (ClickInterceptedException, ElementClickInterceptedException):
			from selenium.webdriver.common.action_chains import ActionChains
			actionchains = ActionChains(browser)
			# Hoping the mouse is still at a position as above;
			actionchains.click().perform()
			
			print("Interception error... trying again...\n")
			continue
		finally:
			if 'mp4' in browser.current_url:
				new_url = browser.current_url
				break
			else:
				#browser.close()	# Closes current tab
				#new_url = browser.current_url
				continue
	
	browser.quit() # Shuts the current instance of the browser
	print("Done!\n")
	return new_url
	

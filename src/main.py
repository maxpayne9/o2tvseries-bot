#!/usr/bin/env python3

# This is the main controller for the program script
from o2tvseries import *
from exceptions import *
from termcolor import colored
from tqdm import tqdm
import time
import logging, traceback
from requests import ConnectionError

text = colored("We cannot find what you requested\nTry something else\n", 'red') 
text2 = colored("We experienced an error...\nLet's try this again...\n", 'red')





print("Welcome to the script")
time.sleep(1)
print("\t\twritten by Ismael!\n")


try:
	while True:
		while True:
			search_input = input("What series will you request today:\n:- ")
			try:
				search(search_input) # Returns list of results
				break
			except (KeywordNotFoundError, TypeError):
				print(text)
				continue
			except ConnectionError:
				print("Internet Connection Error...\n\t please fix and try again!\n\n")
				time.sleep(5)
				continue
		while True:
			try:
				selection = input("Thank you.\nPlease select a number of choice:\n:-")
			
				if int(selection) in driver_dict.keys():
					key = driver_dict[int(selection)]
					if '\n' in key:
						path_var.append(key.split('\n')[0])
					else:
						path_var.append(key)
			except ValueError:
				print("Please input a number to select an option on your screen")
				continue
			
			try:
				link = get_link(key, results_links)
				tags = link_parser(link)
				break
			except ConnectionError:
				#logging.error(traceback.format_exc())
				print(text2)
				time.sleep(1)
				continue
			

			
		while True:	
			sn_dict = {}
			populate(tags, sn_dict)
			if 'series' in list(sn_dict.values())[0]:
				print("What season will you select:\n")
				display(sn_dict)	# Remember this guy controls driver_dict
				selection = input(':- ')
				if int(selection) in driver_dict.keys():
					key = driver_dict[int(selection)]
					if '\n' in key:
						path_var.append(key.split('\n')[0])
					else:
						path_var.append(key)
				try:
					link = get_link(key, sn_dict)
					tags = link_parser(link)
					break
				except ConnectionError:
					#logging.error(traceback.format_exc())
					print(text2)
					time.sleep(1)
					continue

			else:	#Come back to this later
				print("Shall we download the movie?\n")
				selection = input('yes/No:- ')
				print("Downloading single movies is a work in progress...\n Please check a future update!")
			break

		#continuing


		ep_dict = {}
		populate(tags, ep_dict)
	
		selection=input("Press 'z' to download all episodes...\nOtherwise, press 'n' to view available episodes!\n:- ")
		if selection == 'z':
			
			
			get_file(ep_dict)
			path_var.clear()
			if os.name != 'posix':
				import winsound
				winsound.Beep(650,180)

		else:
			while True:
				display(ep_dict)
				try:
					selection = input("What episode(s) do you want to download?...\n(you can separate your selections with commas or spaces)\n:- ")
				
					get_file(ep_dict,selection)
					
				except KeyError:
					print("You probably typed both spaces and commas in the input...\nTry again...")
					continue
				except ConnectionError:
					print("Please check your internet connection!")
					check = input("\nFix your internet connection and type 'c' to try again\n:- ")
					if check == 'c':
						get_file(ep_dict,selection)
				finally:
					path_var.clear()
				print("If you want to download more episodes, type 'c' to continue...\nOtherwise type 'q'\n")
				select=input(':- ')
				if select=='c':
					continue
				elif select=='q':
					time.sleep(2)
					break
		
		print("\nDo you want to download another series?\n")
		query = input("Type 'y' for yes or 'n' for No...\n:- ")
		if query == 'y':
			if os.name == 'posix':# mac and linux
				os.system('clear')
			else: # windows
				os.system('cls')
			continue
		else:
			print("Good bye!\nExiting...")
			time.sleep(5)
			break
	exit()
except KeyboardInterrupt:
		print("\n\nQuiting...\n")
		time.sleep(3)
		print("Good Bye...")
		time.sleep(1)
		exit()











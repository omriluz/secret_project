# person needs to download gecko driver and firefox
####################################################

# validate that the messaged user does not have a full inbox , if she does go back to the main screen (Right now the workaround solution is by creating a main loop that keeps the program running even when obstacles occur)
# format with datetime the time you need to wait 
# on the first function assert that you are in the homepage else get to it
# need more validations of current url and other things to avoid exceptions
# should I replace javascript execution with something more safe? 



# selenium.common.exceptions.ElementClickInterceptedException: Message: Element <div class="navbar-link-icon-container"> is not clickable at point (115,143) because another element <div class="FullscreenOverlay-inner"> obscures it
# grab endtime with better elements^^^^^^^^^^^^^^^^^^^^^

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from IPython import embed
from random import choice
import configparser
import os

# later change this to work with expected conditions
from time import sleep
import random

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class OkCupid:
	def __init__(self):
		self.fp_path()
		self.driver.get("https://www.okcupid.com/doubletake")

		self.messages = ["אפשר להגיד לילדים שלנו שנפגשנו בטיול באירופה","מראה שחורה או משחקי הכס?",
						"בת כמה אמרת שקוראים לך?"]


		self.pause = random.randint(3,5)
			



	def is_hot(self):
		"""returns a boolean that decides if the person is hot enough to swipe right
		downloads all images and inputs them into the AI
		gets a list of ints of each image and gets the average overall hotness
		if hotness is higher or equal to hotness number given it will swipe right"""
		pass

	def fp_path(self):

		mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
		mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
		profile = configparser.ConfigParser()
		profile.read(mozilla_profile_ini)
		data_path = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))

		options = Options() 

		# UNCOMMENT THIS TO MAKE BROWSER HEADLESS
		# options.headless = True
		
		self.driver = webdriver.Firefox(data_path, options=options)


	def press_profile(self):
		if self.driver.current_url != "https://www.okcupid.com/doubletake":
			print("not on the main page...going to main page")
			self.driver.get("https://www.okcupid.com/doubletake")

		# Handle cookie notification
		# try:
		# 	self.driver.find_element_by_class_name("accept-cookie-container").click()
		# 	sleep(self.pause)
		# except ElementNotInteractableException:
		# 	pass
		# check if window pane open and blocking the profile button
		try:
			windowpane = self.driver.find_element_by_class_name('messenger-message-pane')
			exit_message_window_button = self.driver.find_element_by_class_name("messenger-user-row-close")
			exit_message_window_button.click()
			try:
				element = WebDriverWait(self.driver, 20).until(
					EC.presence_of_element_located((By.CLASS_NAME, 
						'cardsummary-profile-link')))
				element.click()
			except Exception:
				print("could not press profile (message window pane)")
		except NoSuchElementException:
			try:
				element = WebDriverWait(self.driver, 20).until(
					EC.presence_of_element_located((By.CLASS_NAME, 
						'cardsummary-profile-link')))
				element.click()
			except Exception:
				print("Could not press profile....Trying again")
				# maybe think of better code to put here!
				self.driver.find_element_by_class_name('cardsummary-profile-link').click()


	def press_like(self):

		# validate that you are on the right page here 

		# press like
		try:
			self.driver.execute_script("document.getElementById('like-button').click();")
		except:
			print("like button js failed, remove except so you know to find the exception ")				


	def message_screen(self):

		# handle cookie notification 
		sleep(self.pause)
		try:
			self.driver.find_element_by_class_name("optanon-alert-box-close").click()
			sleep(self.pause)
		except NoSuchElementException:
			pass
		except ElementNotInteractableException:
			pass

		sleep(self.pause)
		try:
			self.driver.find_element_by_class_name("accept-cookie-container").click()
			sleep(self.pause)
		except NoSuchElementException:
			pass
		except ElementNotInteractableException:
			pass

		# send message
		# IF visibility_of_element_located OF ELEMENT DOESNT WORK TRY element_to_be_clickable
		try:
			element = WebDriverWait(self.driver, 20).until(
				EC.element_to_be_clickable((By.CLASS_NAME, 
					'messenger-composer')))
			element.send_keys(choice(self.messages))
			sleep(4)
			try:
				element = WebDriverWait(self.driver, 20).until(
					EC.presence_of_element_located((By.CLASS_NAME, 
						'messenger-toolbar-send')))
				element.click()
			except TimeoutException:
				print("could not press send")
		except TimeoutException:
			print("could not a send message ")

		# pressing send too fast
		sleep(7)

		# go back to double take
		okcupid.driver.find_element_by_class_name('navbar-link-icon-container').click() 
		# if this ever breaks just use driver.get to the doubletake page

	def limit_reached(self):

		# Dont know what the fuck is wrong what the code above but this shit here works just fine
		try:
			full_screen_overlay = self.driver.find_element_by_class_name("FullscreenOverlay-inner")
			full_screen_overlay.find_element_by_class_name("dynamic-likes-cap-modal-container")
			print("1djioadjiosa")
			return True
		except NoSuchElementException:
			print("3")
			return False


	def amount_of_time_to_sleep(self, time_string):
		# INPUT: 15h 38m
		# OUTPUT: 56280

		time_list = time_string.split()
		amount_calculated = int(time_list[0][0]) * 60 * 60 + int(time_list[1][0]) * 60
		return amount_calculated


if __name__ == '__main__':
	okcupid = OkCupid()
	while True:

		okcupid.press_profile()

		okcupid.press_like()

		# needs a few seconds to load the element in limit_reached
		sleep(5.5)
		if okcupid.limit_reached() == True:
			# Close the browser and sleep the designated amount of time
			time_to_wait = okcupid.driver.find_element_by_class_name("likes-cap-breather-modal-countdown").text
			okcupid.driver.close()
			sleep(okcupid.amount_of_time_to_sleep(time_to_wait))
			print("sleeping finished")
			okcupid.driver.get("https://www.okcupid.com/doubletake")
		else:
			okcupid.message_screen()
	
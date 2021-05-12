
from selenium.common.exceptions import ElementClickInterceptedException
from urllib3.exceptions import NewConnectionError

class Error(Exception):
	""" Base class for othe rexceptions"""
	pass

class KeywordNotFoundError(Error):
	""" Raised when search term not found"""
	pass

class ClickInterceptedException(ElementClickInterceptedException):
	pass

class NewConnectionError(Error):
	pass
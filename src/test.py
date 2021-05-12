import unittest
from selenium import webdriver
from pathlib import Path
from selenium.webdriver import Firefox

class TestOne(unittest.TestCase):
	def setUp(self):
		webdriver_path = Path("geckodriver.exe")
		driver = Firefox( executable_path=webdriver_path)
		self.driver.set_window_size(1120, 550)

	def test_url(self):
		self.driver.get("https://o2tvseries.co/verifyDownload.php?id=84487")
		self.driver.find_element_by_name('download'.click())
		self.assertIn("https://files.tvncdn.com/cdn/zone1/TV_Series/Money_Heist/Season_4_Dubbed/Money_Heist_S04E08_kissTVSeries.com.mp4", self.driver.current_url)
	def tearDown(self):
		self.driver.quit()


if __name__ == '__main__':
	unittest.main()

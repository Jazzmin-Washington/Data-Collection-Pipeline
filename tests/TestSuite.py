#%%
# ASOS Unit Testing Suite
import selenium
from selenium.webdriver import Chrome
from scrapers.Data_Collection_ASOS_small_batch_for_testing import ASOS
from tests.test_cookies import TestFunction_1
from tests.test_nav_to_sale_pg import TestFunction_2
from tests.test_load_more import TestFunction_3
from tests.test_get_link import TestFunction_4
from tests.test_get_product_data import TestFunction_5
from tests.test_save_data import TestFunction_6
from tests.test_save_images import TestFunction_7
import unittest
import time
from unittest import TestSuite

suite = unittest.TestSuite
loader = unittest.TestLoader

def setSuite(suite):
    suite = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestFunction_1))
    suite.addTests(loader.loadTestsFromTestCase(TestFunction_2))
    suite.addTests(loader.loadTestsFromTestCase(TestFunction_3))
    suite.addTests(loader.loadTestsFromTestCase(TestFunction_4))
    suite.addTests(loader.loadTestsFromTestCase(TestFunction_5))
    suite.addTests(loader.loadTestsFromTestCase(TestFunction_6))
    suite.addTests(loader.loadTestsFromTestCase(TestFunction_7))

    return suite
   

          
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
    
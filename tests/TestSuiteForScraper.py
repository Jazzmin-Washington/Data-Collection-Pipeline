#%%
# ASOS Unit Testing Suite
import selenium
from selenium.webdriver import Chrome
from Data_Collection_ASOS_small_batch_for_testing import ASOS
from tests.test_cookies import TestLoadAndAcceptCookies
from tests.test_nav_to_sale_pg import TestNavToTheSalePage
from tests.test_load_more import TestLoadMoreProducts
from tests.test_get_link import TestGetLinks
from tests.test_get_product_data import TestGetProductData
from tests.test_save_data import TestSaveData
from tests.test_save_images import TestSaveImages
import unittest
from unittest import TestSuite

suite = unittest.TestSuite
loader = unittest.TestLoader

def setSuite(suite):
    suite = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestLoadAndAcceptCookies))
    suite.addTests(loader.loadTestsFromTestCase(TestNavToTheSalePage))
    suite.addTests(loader.loadTestsFromTestCase(TestLoadMoreProducts))
    suite.addTests(loader.loadTestsFromTestCase(TestGetLinks))
    suite.addTests(loader.loadTestsFromTestCase(TestGetProductData))
    suite.addTests(loader.loadTestsFromTestCase(TestSaveData))
    suite.addTests(loader.loadTestsFromTestCase(TestSaveImages))
    return suite
   

          
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
    ASOS.driver.quit()
    



# %%


# %%

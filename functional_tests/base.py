from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time,os

MAX_WAIT = 4


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument("-profile")
        options.add_argument("/home/sicheng1806/script/python/ttdweb/firefox_config")
        #options.add_argument('--headless')
        self.brower = webdriver.Firefox(options=options)
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = "http://" + staging_server
    def tearDown(self) -> None:
        self.brower.quit()
    
    def wait_for(self,fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e 
                time.sleep(0.5)

    def wait_for_row_in_list_table(self,row_text):
        def _assert_row_texts_In_list_table():
            table = self.brower.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name("tr")
            self.assertIn(row_text,[row.text for row in rows])
        return self.wait_for(_assert_row_texts_In_list_table)

    def get_item_input_box(self):
        return self.brower.find_element_by_id('id_text')
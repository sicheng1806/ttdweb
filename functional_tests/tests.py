from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time,os

MAX_WAIT = 4


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument("-profile")
        options.add_argument("/home/sicheng1806/script/python/ttdweb/firefox_config")
        #options.add_argument('--headless')
        self.brower = webdriver.Firefox(options=options)
        staging_server = os.environ.get('STAGING_SERVER')
        staging_ip = os.environ.get('STAGING_IP')
        if staging_ip:
            self.live_server_url = staging_ip
        if staging_server:
            self.live_server_url = "http://" + staging_server

    def tearDown(self) -> None:
        self.brower.quit()

    def wait_for_rows_in_list_table(self,row_texts):
        start_time = time.time()
        while True:
            try:
                table = self.brower.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name("tr")
                for row_text in row_texts:
                    self.assertIn(row_text,[row.text for row in rows])
                return 
            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e 
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 卡秋纱听说又一个很酷的在线代办事项应用
        # 她去看了这个应用的首页
        self.brower.get(self.live_server_url)

        # 她注意到网页的标题和头部都包含 “To-Do” 这个词
        self.assertIn('To-Do',self.brower.title)
        header = self.brower.find_element_by_tag_name("h1").text
        self.assertIn("To-Do",header)

        # 应用邀请她输入一个待办事项
        inputbox = self.brower.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # 她在一个文本框中输入了 "购买孔雀羽毛" 
        ## 卡秋纱的爱好是使用假蝇做饵钓鱼
        inputbox.send_keys("Buy peacock feathers")
        
        # 她按回车键后，页面更新了
        # 待办事项表格中显示了 "1. 购买孔雀羽毛"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_rows_in_list_table(["1: Buy peacock feathers"])
        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了 "使用孔雀羽毛做假蝇"
        # 页面再次更新，她的清单中显示了这两个待办事项
        inputbox = self.brower.find_element_by_id("id_new_item")
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_rows_in_list_table([
            "1: Buy peacock feathers",
            "2: Use peacock feathers to make a fly"
        ])

        # 她很满意，去睡觉了

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 卡秋纱新建一个待办事项清单
        self.brower.get(self.live_server_url)
        inputbox = self.brower.find_element_by_id("id_new_item")
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_rows_in_list_table(["1: Buy peacock feathers"])

        # 她注意到页面有了个唯一的URL
        katyusha_list_url = self.brower.current_url 
        self.assertRegex(katyusha_list_url,'/lists/.+')

        # 现在一名叫做弗朗西斯的新用户访问了网页

        ## 我们使用一个新的浏览器会话，确保卡秋纱的信息不会从cookie中泄漏出去
        self.brower.quit()
        self.setUp()

        # 弗朗西斯访问首页
        # 页面中看不到卡秋纱的清单
        self.brower.get(self.live_server_url)
        page_text = self.brower.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers",page_text)

        # 弗朗西斯输入一个新待办事项，新建一个清单,也看不到卡秋莎的清单
        inputbox = self.brower.find_element_by_id("id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_rows_in_list_table(["1: Buy milk"])
        
        # 弗朗西斯获得了他的唯一URL
        francis_list_url = self.brower.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,katyusha_list_url)

        # 这个页面还是没有卡秋纱的清单
        page_text = self.brower.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers",page_text)
        self.assertIn("Buy milk",page_text)

        # 两人都很满意，然后去睡觉了
    
    def test_layout_and_styling(self):
        # edies 访问首页 
        self.brower.get(self.live_server_url)
        self.brower.set_window_size(1024,768)
        

        # 她看到输入框完美的居中显示
        inputbox = self.brower.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )
        # 她新建清单后，输入框仍完美地居中显示
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_rows_in_list_table(['1: testing'])
        inputbox = self.brower.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )
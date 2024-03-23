from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.test import LiveServerTestCase
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    

    def setUp(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument("-profile")
        options.add_argument("/home/sicheng1806/script/python/ttdweb/firefox_config")
        self.brower = webdriver.Firefox(options=options)

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
        
        self.fail("Finish the test!")

        # 卡秋纱想知道这个网站是否会记住他的清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 她访问那个URL，发现她的待办事项列表还在

        # 她很满意，去睡觉了


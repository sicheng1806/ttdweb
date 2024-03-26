from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class NewVisitorTest(FunctionalTest):
    #@skip
    def test_can_start_a_list_for_one_user(self):
        # 卡秋纱听说又一个很酷的在线代办事项应用
        # 她去看了这个应用的首页
        self.brower.get(self.live_server_url)

        # 她注意到网页的标题和头部都包含 “To-Do” 这个词
        self.assertIn('To-Do',self.brower.title)
        header = self.brower.find_element_by_tag_name("h1").text
        self.assertIn("To-Do",header)

        # 应用邀请她输入一个待办事项
        inputbox = self.get_item_input_box()
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
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了 "使用孔雀羽毛做假蝇"
        # 页面再次更新，她的清单中显示了这两个待办事项
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")
    #@skip
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 卡秋纱新建一个待办事项清单
        self.brower.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

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
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        
        # 弗朗西斯获得了他的唯一URL
        francis_list_url = self.brower.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,katyusha_list_url)

        # 这个页面还是没有卡秋纱的清单
        page_text = self.brower.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers",page_text)
        self.assertIn("Buy milk",page_text)

        # 两人都很满意，然后去睡觉了
    
    def test_lists_can_show_in_sort(self):
        # 丞登录首页
        self.brower.get(self.live_server_url)
        # 丞提交 “item2"
        self.get_item_input_box().send_keys("item2",Keys.ENTER)
        self.wait_for_row_in_list_table('1: item2')
        # 丞提交 "item1"
        self.get_item_input_box().send_keys("item1",Keys.ENTER)
        self.wait_for_row_in_list_table('2: item1')
        # 清单按顺序排步
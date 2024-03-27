from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

from lists.forms import DUPLICATE_ITEM_ERROR
        
class ItemValidationTest(FunctionalTest):
    
    
    def wait_for_validate_eror(self,error_text):
        return self.wait_for(lambda: self.assertEqual(
            self.brower.find_element_by_css_selector('.has-error').text,
            error_text
        ))
    @skip
    def test_cannot_add_empty_list(self):
        # 丞访问首页
        self.brower.get(self.live_server_url)
        
        # 提交了一个空表单
        self.get_item_input_box().send_keys(Keys.ENTER)
        # 浏览器截取了请求

        # 提交了“写代码”，清单刷新
        self.get_item_input_box().send_keys('写代码',Keys.ENTER)
        self.wait_for_row_in_list_table("1: 写代码")
        # 丞再次输入了空的表单，再次被浏览器拦截，表单没有增加
        self.get_item_input_box().send_keys(Keys.ENTER)
        table = self.wait_for(lambda:self.brower.find_element_by_id('id_list_table'))
        self.assertNotIn('2:',table.text)
        # 丞提交了"second item"，清单刷新
        self.get_item_input_box().send_keys('second item',Keys.ENTER)
        self.wait_for_row_in_list_table('2: second item')
        # 丞满意得退出了页面
    @skip
    def test_cannot_add_duplicate_items(self):
        # 丞访问首页，新建一个清单
        self.brower.get(self.live_server_url)
        self.get_item_input_box().send_keys("item 1",Keys.ENTER)
        self.wait_for_row_in_list_table("1: item 1")
        # 他输入了重复的清单
        self.get_item_input_box().send_keys("item 1",Keys.ENTER)

        # 看见有一条帮助错误的信息
        self.wait_for_validate_eror(DUPLICATE_ITEM_ERROR)

    def test_error_messages_are_cleared_on_input(self):
        # 丞新建一个清单，输入了重复清单
        self.brower.get(self.live_server_url)
        self.get_item_input_box().send_keys("item1",Keys.ENTER)
        self.wait_for_row_in_list_table("1: item1")
        self.get_item_input_box().send_keys("item1",Keys.ENTER)
        # 页面出现了错误提醒
        self.wait_for_validate_eror(DUPLICATE_ITEM_ERROR)
        # 在他输入其他内容时，验证错误消失
        self.get_item_input_box().send_keys("a")
        self.wait_for(lambda:self.assertFalse(
            self.brower.find_element_by_css_selector('.has-error').is_displayed()
        )) # is_displayed 用于验证元素是否可见

from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

from lists.forms import DUPLICATE_ITEM_ERROR
        
class ItemValidationTest(FunctionalTest):
       
    @skip
    def test_cannot_add_empty_list(self):
        # 丞访问首页
        self.brower.get(self.live_server_url)
        
        # 提交了一个空表单
        self.get_item_input_box().send_keys(Keys.ENTER)
        # 浏览器截取了请求
        # 清单页面不会加载
        # 丞输入了一个非空表单，这次来到了他自己的页面
        inputbox = self.get_item_input_box()
        inputbox.send_keys("写代码")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_rows_in_list_table(["1: 写代码"])
        self.assertIn("lists",self.brower.current_url)
        # 丞再次输入了空的表单，再次被浏览器拦截，表单没有增加
        table = self.wait_for(lambda:self.brower.find_element_by_id('id_list_table'))
        self.assertNotIn('2:',table.text)
        # 丞输入再次输入新的表单，报错信息消失了
        self.get_item_input_box().send_keys('second item',Keys.ENTER)
        self.wait_for_rows_in_list_table(['2: second item'])
        # 丞满意得退出了页面


    def test_cannot_add_duplicate_items(self):
        # 丞访问首页，新建一个清单
        self.brower.get(self.live_server_url)
        self.get_item_input_box().send_keys("item 1",Keys.ENTER)
        self.wait_for_rows_in_list_table(["1: item 1"])
        # 他输入了重复的清单
        self.get_item_input_box().send_keys("item 1",Keys.ENTER)

        # 看见有一条帮助错误的信息
        self.wait_for(lambda:self.assertEqual(
            self.brower.find_element_by_css_selector('.has-error').text,
            DUPLICATE_ITEM_ERROR
        ))



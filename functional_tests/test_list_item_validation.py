from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip
        
class ItemValidationTest(FunctionalTest):
       
    #@skip
    def test_cannot_add_empty_list(self):
        # 丞访问首页
        self.brower.get(self.live_server_url)
        
        # 提交了一个空表单
        self.brower.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        # 页面还是位于首页，并且底部出现了错误提示,提示待办事项不能为空
        self.wait_for(lambda : self.assertEqual(
            self.brower.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        self.assertEqual(self.brower.current_url,self.live_server_url)
        # 丞输入了一个非空表单，这次来到了他自己的页面
        inputbox = self.brower.find_element_by_id("id_new_item")
        inputbox.send_keys("写代码")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_rows_in_list_table(["1: 写代码"])
        self.assertIn("lists",self.brower.current_url)
        # 丞再次输入了空的表单，报错信息又出现了，表单没有增加
        self.brower.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for(lambda : self.assertEqual(
            self.brower.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        table = self.wait_for(lambda:self.brower.find_element_by_id('id_list_table'))
        self.assertNotIn('2:',table.text)
        # 丞输入再次输入新的表单，报错信息消失了
        self.brower.find_element_by_id('id_new_item').send_keys('second item',Keys.ENTER)
        self.wait_for_rows_in_list_table('2: second item')
        with self.assertRaises():
            self.wait_for(lambda : self.assertEqual(
            self.brower.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        # 丞满意得退出了页面





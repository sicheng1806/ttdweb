from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip
        
class ItemValidationTest(FunctionalTest):
       
    @skip
    def test_cannot_add_empty_list(self):
        # 丞访问首页
        
        # 提交了一个空表单

        # 页面还是位于首页，并且底部出现了错误提示

        # 丞输入了一个非空表单，这次来到了他自己的页面

        # 丞再次输入了空的表单，报错信息又出现了，表单没有增加

        # 丞退出了页面

        self.fail('write me')



from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # edies 访问首页 
        self.brower.get(self.live_server_url)
        self.brower.set_window_size(1024,768)
        

        # 她看到输入框完美的居中显示
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )
        # 她新建清单后，输入框仍完美地居中显示
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_rows_in_list_table(['1: testing'])
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )
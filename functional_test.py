from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument("-profile")
        options.add_argument("/home/sicheng1806/script/python/ttdweb/firefox_config")
        self.brower = webdriver.Firefox(options=options)

    def tearDown(self) -> None:
        self.brower.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 卡秋纱听说又一个很酷的在线代办事项应用
        # 她去看了这个应用的首页
        self.brower.get('http://localhost:8000')

        # 她注意到网页的标题和头部都包含 “To-Do” 这个词
        self.assertIn('To-Do',self.brower.title)
        self.fail('Finish the test!')

        # 应用邀请她输入一个待办事项

        # 她在一个文本框中输入了 "购买孔雀羽毛" 
        ## 卡秋纱的爱好是使用假蝇做饵钓鱼

        # 她按回车键后，页面更新了
        # 待办事项表格中显示了 "1. 购买孔雀羽毛"

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了 "使用孔雀羽毛做假蝇"
        # 页面再次更新，她的清单中显示了这两个待办事项

        # 卡秋纱想知道这个网站是否会记住他的清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 她访问那个URL，发现她的待办事项列表还在

        # 她很满意，去睡觉了

if __name__ == '__main__':
    unittest.main(warnings='ignore')
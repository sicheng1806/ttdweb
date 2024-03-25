from django.test import TestCase
from lists.models import Item,List

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response,'home.html')

class ListViewTest(TestCase):
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="itemey 1",list=list_)
        Item.objects.create(text='itemey 2',list=list_)

        resp = self.client.get(f"/lists/{list_.id}")

        self.assertContains(resp,'itemey 1')
        self.assertContains(resp,'itemey 2')
        


    def test_uses_list_template(self):
        list_ = List.objects.create()
        resp = self.client.get(f'/lists/{list_.id}')
        self.assertTemplateUsed(resp,'list.html')
    
    def test_displays_only_items_for_that_list(self):
        corrent_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=corrent_list)
        Item.objects.create(text='itemey 2',list=corrent_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item1',list=other_list)
        Item.objects.create(text='other list item2',list=other_list)

        resp = self.client.get(f'/lists/{corrent_list.id}')

        self.assertContains(resp,'itemey 1')
        self.assertContains(resp,'itemey 2')
        self.assertNotContains(resp,'other list item1')
        self.assertNotContains(resp,'other list item2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        resp = self.client.get(f'/lists/{correct_list.id}')
        self.assertEqual(resp.context['list'],correct_list)

class NewListTest(TestCase):

    def test_can_save_a_post_request(self):
        self.client.post('/lists/new',data={
            "item_text":'A new list item'
        })
        self.assertEqual(Item.objects.count(),1)
        self.assertEqual(Item.objects.first().text,'A new list item')
    
    def test_redirects_after_POST(self):
        resp = self.client.post('/lists/new',data={
            "item_text":'A new list item'
        })
        self.assertEqual(resp.status_code,302)

class NewItemTest(TestCase):

    def test_add_item_with_exsiting_post(self):
        corret_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post(f"/lists/{corret_list.id}/add_item",data={
            "item_text":"A new item"
        })

        self.assertEqual(Item.objects.count(),1)

from django.test import TestCase
from django.urls import resolve


from lists.models import Item,List

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response,'home.html')

class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List() 
        list_.save()
        first_item = Item()
        first_item.text = 'The first (ever) list item' 
        first_item.list = list_
        first_item.save() 

        second_item = Item() 
        second_item.text = 'Item the second' 
        second_item.list = list_
        second_item.save() 

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_)

        saved_items = Item.objects.all() 
        self.assertEqual(saved_items.count(),2) 
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,"The first (ever) list item")
        self.assertEqual(second_saved_item.text,'Item the second')
        self.assertEqual(first_saved_item.list,list_)
        self.assertEqual(second_saved_item.list,list_)

class ListViewTest(TestCase):
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="itemey 1",list=list_)
        Item.objects.create(text='itemey 2',list=list_)

        resp = self.client.get(f"/lists/{list_.id}")

        self.assertContains(resp,'itemey 1')
        self.assertContains(resp,'itemey 2')
        
    def test_can_save_POST(self):
        list_ = List.objects.create()
        resp = self.client.post(f"/lists/{list_.id}",{
            "item_text":"A new item text"
        })
        self.assertContains(resp,"A new item text")


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

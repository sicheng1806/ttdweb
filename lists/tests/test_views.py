from django.test import TestCase
from django.utils.html import escape
from unittest import skip

from lists.models import Item,List
from lists.forms import ItemForm,EMPTY_ITEM_ERROR,DUPLICATE_ITEM_ERROR

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')

    def test_home_page_uses_item_form(self):
        resp = self.client.get('/')
        self.assertIsInstance(resp.context.get('form'),ItemForm)

class ListViewTest(TestCase):
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="itemey 1",list=list_)
        Item.objects.create(text='itemey 2',list=list_)

        resp = self.client.get(f"/lists/{list_.id}")

        self.assertContains(resp,'itemey 1')
        self.assertContains(resp,'itemey 2')
        

    def test_correct_url_and_uses_list_template(self):
        list_ = List.objects.create()
        resp = self.client.get(f'/lists/{list_.id}')
        #breakpoint()
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
    
    def test_add_item_with_exsiting_list_by_POST(self):
        corret_list = List.objects.create()
        other_list = List.objects.create()
        resp = self.client.post(f"/lists/{corret_list.id}",data={
            "text":"A new item"
        })
        self.assertEqual(Item.objects.count(),1)
        self.assertRedirects(resp,f'/lists/{corret_list.id}')
    
    #@skip
    def test_validation_errors_are_sent_back(self):
        list_ = List.objects.create()
        Item.objects.create(text='item1',list=list_)
        Item.objects.create(text='item2',list=list_)
        resp = self.client.post(f'/lists/{list_.id}',data={'text':''})
        self.assertContains(resp,escape("You can't have an empty list item"))
        self.assertEqual(Item.objects.count(),2)
        self.assertEqual(List.objects.count(),1)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        resp = self.client.get(f'/lists/{list_.id}')
        self.assertIsInstance(resp.context['form'],ItemForm)
        self.assertContains(resp,'name="text"')
    @skip
    def test_duplicate_items_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        Item.objects.create(text='item1',list=list_)
        resp = self.client.post(list_.get_absolute_url(),data={
            'text':'item1'
        })
        self.assertContains(resp,DUPLICATE_ITEM_ERROR)
        self.assertTemplateUsed(resp,'list.html')
        self.assertEqual(Item.objects.count(),1)

class NewListTest(TestCase):

    def test_can_save_a_post_request(self):
        self.client.post('/lists/new',data={
            "text":'A new list item'
        })
        self.assertEqual(Item.objects.count(),1)
        self.assertEqual(Item.objects.first().text,'A new list item')
    
    def test_redirects_after_POST(self):
        resp = self.client.post('/lists/new',data={
            "text":'A new list item'
        })
        self.assertEqual(resp.status_code,302)

    def test_for_invalid_input_renders_home_template(self):
        resp = self.client.post('/lists/new',data={'text':''})
        #breakpoint()
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'home.html')
    def test_validation_errors_are_shown_on_home_page(self):
        resp = self.client.post('/lists/new',data={'text':''})
        self.assertContains(resp,escape(EMPTY_ITEM_ERROR))
    def test_for_invalid_input_passed_form_to_template(self):
        resp = self.client.post('/lists/new',data={'text':''})
        self.assertIsInstance(resp.context.get('form'),ItemForm)
        
    
    def test_validation_list_items_arent_saved(self):
        self.client.post('/lists/new',data={'text':''})
        self.assertEqual(Item.objects.count(),0)
        self.assertEqual(List.objects.count(),0)




    

    
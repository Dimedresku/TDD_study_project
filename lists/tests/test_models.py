from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


class ItemModelTest(TestCase):

    def test_default_text(self):
        '''test default test'''
        item = Item()
        self.assertEqual(item.text, '')

    def test_string_representation(self):
        item = Item(text='some_text')
        self.assertEqual(str(item), 'some_text')


class ListModelTest(TestCase):

    def test_item_is_related_to_list(self):
        '''test: element is related to list'''
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        ''' cannot add empty list elements'''
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_duplicate_items_are_invalid(self):
        '''test: duplicate item are invalid'''
        list_ = List.objects.create()
        Item.objects.create(text='foo bar', list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text='foo bar', list=list_)
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        '''test: can save same item in different lists'''
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='foo bar')
        item = Item(list=list2, text='foo bar')
        item.full_clean()

    def test_list_ordering(self):
        '''test list ordering'''
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])


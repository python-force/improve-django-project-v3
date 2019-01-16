from datetime import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from menu.models import Menu, Item, Ingredient


class MenuViewsTests(TestCase):

    def setUp(self):

        date_str = "2019-12-11"
        self.temp_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        self.user = User.objects.create_user('John Doe', password='johndoe')
        self.user.is_staff = True

        self.ingredient = Ingredient.objects.create(
            name="Blueberry"
        )
        self.item = Item.objects.create(
            name="Blueberry Soda Pop Cake",
            description="Lorem Ipsum is simply dummy",
            chef=self.user,
            standard=True,
        )
        self.item.ingredients.add(self.ingredient)
        self.menu = Menu.objects.create(
            season="Big Menu with Cakes and Candles",
            expiration_date=self.temp_date,
        )
        self.menu.items.add(self.item)

    def test_ingredient_creation(self):
        now = timezone.now()
        self.assertLess(self.ingredient.created_date, now)

    def test_item_creation(self):
        now = timezone.now()
        self.assertLess(self.item.created_date, now)

    def test_menu_creation(self):
        now = timezone.now()
        self.assertLess(self.menu.created_date, now)

    def test_menu_list(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_item_list(self):
        resp = self.client.get(reverse('item_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.item, resp.context['items'])
        self.assertTemplateUsed(resp, 'menu/item_list.html')

    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail',
                                       kwargs={'pk': self.item.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.item, resp.context['item'])
        self.assertTemplateUsed(resp, 'menu/detail_item.html')

    # Invalid Data
    def test_create_new_menu_view_fail(self):
        resp = self.client.post('/new/', {'season': "Big Menu",
                                          'items': '',
                                          'expiration_date': "2019-01-15"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('error_1_id_items' in resp.content.decode('utf-8'))

    def test_create_new_menu_view(self):
        menus = Menu.objects.count()
        resp = self.client.post('/new/', {'season': "Big Menu with Cakes",
                                          'items': [self.item.pk],
                                          'expiration_date': "2021-01-15"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Menu.objects.count(), menus + 1)

    def test_create_menu_view_no_data(self):
        resp = self.client.get(
            reverse('menu_new',)
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_change_menu_view_no_data(self):
        resp = self.client.get(
            reverse('menu_edit', kwargs={'pk': self.menu.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/change_menu.html')

    def test_change_item_view_no_data(self):
        resp = self.client.get(
            reverse('item_edit', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/change_item.html')

    def test_change_item_view(self):
        test_data = {
            'name': "Fancy Item and Dots",
            'description': "Fancy Item with sparkles and cakes",
            'standard': True,
            'ingredients': [self.ingredient.pk,],
        }
        resp = self.client.post(reverse('item_edit',
                                        kwargs={'pk': self.item.pk}),
                                test_data,
                                )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Item.objects.get(pk=1).name,
                         'Fancy Item and Dots')
        self.assertEqual(Item.objects.get(pk=1).description,
                         'Fancy Item with sparkles and cakes')

    def test_change_menu_view(self):
        test_data = {
            'season': "Testing New Title for this Menu",
            'expiration_date': datetime.strptime("2021-12-11", "%Y-%m-%d").date(),
            'items': [self.item.pk,],
        }
        resp = self.client.post(reverse('menu_edit',
                                        kwargs={'pk': 1}),
                                        test_data,
                                )
        # self.assertEqual(resp.status_code, 302)
        self.assertEqual(Menu.objects.get(pk=1).season,
                         'Testing New Title for this Menu')

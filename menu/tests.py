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
            name="Blueberry Soda",
            description="Blue Soda",
            chef = self.user,
            standard=True,
        )
        self.item.ingredients.add(self.ingredient)

        self.menu = Menu.objects.create(
            season="Big Menu",
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

    def test_create_new_menu_view(self):
        menus = Menu.objects.count()
        resp = self.client.post('/new/', {'season': "Big Menu", 'items': [self.item.pk], 'expiration_date': "2019-01-15"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual( Menu.objects.count(), menus + 1)

    def test_change_menu_view(self):
        test_data = {
            'season': "Big Menu",
            'items': [self.item.pk,],
            'expiration_date': "2019-01-15"
        }
        resp = self.client.post(reverse('menu_edit',
                                        kwargs={'pk': self.menu.pk}),
                                        test_data,
                                )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Menu.objects.get(pk=1).season, 'Big Menu')

    def test_change_item_view(self):
        test_data = {
            'name': "Fancy Item",
            'description': "Fancy Item with sparkles",
            'standard': True,
            'ingredients': [self.ingredient.pk,],
        }
        resp = self.client.post(reverse('item_edit',
                                        kwargs={'pk': self.item.pk}),
                                test_data,
                                )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Item.objects.get(pk=1).name, 'Fancy Item')
        self.assertEqual(Item.objects.get(pk=1).description, 'Fancy Item with sparkles')




    """
    # Invalid Data
    def test_create_new_menu_view_fail(self):
        resp = self.client.post('/new/', {'season': "Big Menu", 'items': '', 'expiration_date': "2019-01-15"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('error_1_id_items' in resp.content)

    
    # Valid Data
    def test_add_admin_form_view(self):
        user_count = User.objects.count()
        response = self.client.post("include url to post the data given",
                                    {'email': "user@mp.com", 'password': "user", 'first_name': "user"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertTrue('"error": false' in response.content)
        """

"""
class MineralViewsTests(TestCase):

    def setUp(self):

        self.mineral = Mineral.objects.create(
            name="Greigite",
            image_filename="greigite.jpg",
            image_caption="Greigite structure, SFe4 tetrahedra",
            category="SulfideThiospinel groupSpinel structural group",
            formula="Fe<sub>2</sub>+Fe<sub>3</sub>+<sub>2</sub>S<sub>4</sub>",
            strunz_classification="02.DA.05",
            color="Pale pink, tarnishes to metallic blue-black",
            crystal_system="Cubic",
            unit_cell="a = 9.876 Å; Z = 8",
            crystal_symmetry="Isometric hexoctahedralH-M symbol: (4/m32/m)Space group: F d3m",
            cleavage=None,
            mohs_scale_hardness="4 to 4.5",
            luster="Metallic to earthy",
            streak=None,
            diaphaneity="Opaque",
            optical_properties=None,
            refractive_index=None,
            crystal_habit="Spheres of intergrown octahedra and as disseminated microscopic grains",
            specific_gravity="4.049",
            group="Sulfides",
        )
        self.mineral2 = Mineral.objects.create(
            name="Greigite-2nd-Category",
            image_filename="greigite.jpg",
            image_caption="Greigite structure, SFe4 tetrahedra",
            category="SulfideThiospinel groupSpinel structural group",
            formula="Fe<sub>2</sub>+Fe<sub>3</sub>+<sub>2</sub>S<sub>4</sub>",
            strunz_classification="02.DA.05",
            color="Pale pink, tarnishes to metallic blue-black",
            crystal_system="Cubic",
            unit_cell="a = 9.876 Å; Z = 8",
            crystal_symmetry="Isometric hexoctahedralH-M symbol: (4/m32/m)Space group: F d3m",
            cleavage=None,
            mohs_scale_hardness="4 to 4.5",
            luster="Metallic to earthy",
            streak=None,
            diaphaneity="Opaque",
            optical_properties=None,
            refractive_index=None,
            crystal_habit="Spheres of intergrown octahedra and as disseminated microscopic grains",
            specific_gravity="4.049",
            group="Sulfides",
        )

    def test_index(self):

        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertTemplateUsed(resp, 'index.html')

    def test_mineral_detail_view(self):

        resp = self.client.get(reverse('detail',
                                       kwargs={'pk': self.mineral.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.mineral, resp.context['mineral'])
        self.assertTemplateUsed(resp, 'detail.html')

    def test_search_q(self):

        resp = self.client.get(reverse('search'), {'q': 'G'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertTemplateUsed(resp, 'index.html')

    def test_search_q2(self):

        resp = self.client.get(reverse('search'), {'q': 'X'})
        self.assertEqual(resp.status_code, 404)
        self.assertTemplateUsed(resp, '404.html')

    def test_search_group(self):

        resp = self.client.get(reverse('search'), {'group': 'Sulfides'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertTemplateUsed(resp, 'index.html')

    def test_search_text(self):

        resp = self.client.get(reverse('search'), {'text': 'Cubic'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertTemplateUsed(resp, 'index.html')
"""

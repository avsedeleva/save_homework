from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        User.objects.create(username='TestUser', password='1234567')
        cls.user = get_user_model().objects.get(username='TestUser')
        Group.objects.create(title='Тестовая группа', slug='test-group', description='Тестовое описание группы')
        cls.group = Group.objects.get(slug='test-group')
        Group.objects.create(title='Тестовая группа 2', slug='test-group_2', description='Тестовое описание группы 2')
        cls.group_2 = Group.objects.get(slug='test-group_2')
        Post.objects.create(
            text='Тестовый пост',
            group=PostPagesTests.group,
            author=PostPagesTests.user
        )
        cls.post = Post.objects.get(id=1)

    def setUp(self):
         # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: name"
        templates_pages_names = {
            'index.html': reverse('index'),
            'group.html': reverse('group', kwargs={'slug': 'test-group'}),
            'new_post.html': reverse('new_post'),
        }
        # Проверяем, что при обращении к name вызывается 
        # соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        post_text_0 = response.context.get('page')[0].text
        post_author_0 = response.context.get('page')[0].author.username
        post_group_0 = response.context.get('page')[0].group.title
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_author_0, 'TestUser')
        self.assertEqual(post_group_0, 'Тестовая группа')

    def test_group_page_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('group', kwargs={'slug': 'test-group'}))
        # Взяли первый элемент из списка постов и проверили, что его содержание
        # совпадает с ожидаемым.
        group_title_0 = response.context.get('page')[0].group.title
        group_slug_0 = response.context.get('page')[0].group.slug
        group_description_0 = response.context.get('page')[0].group.description
        post_text_0 = response.context.get('page')[0].text
        post_author_0 = response.context.get('page')[0].author.username
        post_group_0 = response.context.get('page')[0].group.title
        self.assertEqual(group_title_0, 'Тестовая группа')
        self.assertEqual(group_slug_0, 'test-group')
        self.assertEqual(group_description_0, 'Тестовое описание группы')
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_author_0, 'TestUser')
        self.assertEqual(post_group_0, 'Тестовая группа')

    def test_group_2_page_show_correct_context(self):    
        """Проверяем, что пост не попал в другую группу"""
        response = self.authorized_client.get(reverse('group', kwargs={'slug': 'test-group_2'}))
        with self.assertRaises(IndexError):
            post_text_0 = response.context.get('page')[0].text
            self.assertEqual(post_text_0, 'Тестовый пост')

    def test_new_post_page_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        # Список ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'text': forms.fields.CharField,
            # При создании формы поля модели типа TextField 
            # преобразуются в CharField с виджетом forms.Textarea           
            'group': forms.fields.ChoiceField,
        }        
        # Проверяем, что типы полей формы в словаре context 
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)
        
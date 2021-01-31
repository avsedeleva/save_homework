# posts/tests/tests_url.py
from posts.views import index
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post, Group

class StaticURLTests(TestCase):
    def test_homepage(self):
        # Создаем экземпляр клиента
        guest_client = Client()
        # Делаем запрос к главной странице и проверяем статус
        response = guest_client.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200) 

class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        User.objects.create(username='TestUser', password='1234567')
        cls.user = get_user_model().objects.get(username='TestUser')
        Group.objects.create(title='Тестовая группа', slug='test-group', description='Тестовое описание группы')
        cls.group = Group.objects.get(slug='test-group')
        Post.objects.create(
            text='Тестовый пост',
            group=PostURLTest.group,
            author=PostURLTest.user
        )
        cls.post = Post.objects.get(id=1)

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        """# Создаем пользователя
        self.user = get_user_model().objects.create(username='TestUser', password='1234567')"""
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(PostURLTest.user)
        self.templates_url_names = {
        'index.html': '/',
        'group.html': '/group/test-group/',
        'new_post.html': '/new/',
        }

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_url_exists_at_desired_location(self):
        """Страница /group/test-group/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test-group/')
        self.assertEqual(response.status_code, 200)

    def test_new_url_exists_at_desired_location(self):
        """Страница /new доступна авторизованному пользователю."""
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_new_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /new перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get('/new/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/new/')

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for template, reverse_name in self.templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

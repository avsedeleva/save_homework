from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.forms import PostForm
from posts.models import Post, Group


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        User.objects.create(username='TestUser', password='1234567')
        cls.user = get_user_model().objects.get(username='TestUser')
        Group.objects.create(title='Тестовая группа', slug='test-group', description='Тестовое описание группы')
        cls.group = Group.objects.get(slug='test-group')
        # Создаем форму, если нужна проверка атрибутов
        cls.form = PostForm()

    def setUp(self):
        # Создаем неавторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateFormTests.user)

    def test_create_new_post(self):
        """Валидная форма создает запись в Post."""
        # Подсчитаем количество записей в Post
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'author': self.user,
            'group': PostCreateFormTests.group.id,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, '/')
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), post_count+1)
        # Проверяем, что создалась запись с нашим текстом
        self.assertTrue(
            Post.objects.filter(text='Тестовый текст').exists()
        )
        
from django.test import TestCase
from posts.models import Post, Group
from django.contrib.auth import get_user_model



class PostModelTest(TestCase):
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
            group=PostModelTest.group,
            author=PostModelTest.user
        )
        cls.post = Post.objects.get(id=1)

    def test_verbose_name(self):
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст публикации',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(post._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        post = PostModelTest.post
        field_help_text = {
            'text': 'Введите текст публикации',
            'group': 'Выберете группу',
        }
        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(post._meta.get_field(value).help_text, expected)

    def test_object_str_fild_post(self):
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))

    def test_object_str_fild_group(self):
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

from django.test import TestCase

from publishings.forms import ClientForm


class ClientFormTest(TestCase):

    def test_clean_email(self):
        # Проверьте действительный адрес электронной почты
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'content': 'Some content',
            'is_status': True,
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_email_too_long(self):
        # Длина тестового электронного письма превышает установленный лимит
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'a' * 31 + '@example.com',
            'content': 'Some content',
            'is_status': True,
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['Электронная почта может содержать не более 30 символов'])

    def test_clean_email_no_at_symbol(self):
        # Тестовое электронное письмо без символа "@"
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johnexample.com',
            'content': 'Some content',
            'is_status': True,
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ["Введите правильный адрес электронной почты."])

    def test_empty_email(self):
        # Проверьте пустое поле электронной почты
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'content': 'Some content',
            'is_status': True,
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['Обязательное поле.'])

    def test_content_length_exceeds_limit(self):
        # Длина тестового содержимого превышает допустимое значение
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'content': 'a' * 1001,  # Assuming max length is 1000
            'is_status': True,
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
        self.assertEqual(form.errors['content'], ['Содержимое статьи не может превышать 1000 символов.'])

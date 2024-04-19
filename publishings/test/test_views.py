from django.test import TestCase

from publishings.models import Profile


class ProfileListViewTest(TestCase):
    def test_profile_list_view(self):

        # Создаем тестовый профиль
        Profile.objects.create(first_name='Test', last_name='User')

        # Получаем URL для представления списка профилей
        url = ''

        # Отправляем GET-запрос
        response = self.client.get(url)

        # Проверяем, что страница отображается успешно (статус код 200)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что ожидаемый профиль отображается на странице
        self.assertContains(response, 'Test User')
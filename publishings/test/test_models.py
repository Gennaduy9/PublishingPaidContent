from django.utils import timezone
from django.test import TestCase

from publishings.models import Profile, Subscription

from users.models import User


# Тестирование модели Profile
class ProfileModelTest(TestCase):
    def setUp(self):
        # Создание объекта профиля для тестирования
        self.profile = Profile.objects.create(
            first_name='Test',
            last_name='Test',
            content='Test',
            email='test@test.ru',
            is_status=True,
            user=User.objects.create(phone="+7(925)342-54-12", is_superuser=True, is_staff=True),
            created=timezone.now(),
            price=10000,
        )

    # Тестирование создания профиля
    def test_profile_creation(self):
        self.assertEqual(self.profile.first_name, 'Test')
        self.assertEqual(self.profile.content, 'Test')
        self.assertEqual(self.profile.email, 'test@test.ru')
        self.assertTrue(self.profile.created <= timezone.now())
        self.assertEqual(self.profile.price, 10000)

    # Тестирование отображения заголовка профиля
    def test_profile_title(self):
        self.assertEqual(str(self.profile), 'Test Test - Test')


# Тестирование модели Subscription
class SubscriptionModelTest(TestCase):
    def setUp(self):
        # Создание объекта подписки для тестирования
        self.subscription = Subscription.objects.create(
            user=User.objects.create(phone="+7(925)342-54-13", is_superuser=True, is_staff=True),
            status='Подписан',
            profile=Profile.objects.create(
                first_name='Test',
                last_name='Test',
                content='Test',
                email='test1@test.ru',
                is_status=True,
                user=User.objects.create(phone="+7(925)342-54-14", is_superuser=True, is_staff=True),
                created=timezone.now(),
                price=10000,
            ),

        )

    # Тестирование создания подписки
    def test_subscription_creation(self):
        self.assertEqual(self.subscription.status, 'Подписан')
        self.assertEqual(self.subscription.profile.first_name, 'Test')
        self.assertEqual(self.subscription.user.phone, '+7(925)342-54-13')

    # Тестирование отображения заголовка подписки
    def test_subscription_title(self):
        self.assertEqual(str(self.subscription), 'Подписан')

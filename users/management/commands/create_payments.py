from django.core.management.base import BaseCommand
from users.models import User, Payment
from lms.models import Course, Lesson


class Command(BaseCommand):
    help = 'Создает тестовые данные для модели Payment'

    def handle(self, *args, **options):
        # Получаем существующих пользователей и объекты курсов/уроков
        user1 = User.objects.first()
        user2 = User.objects.filter(email='anotheruser@example.com').first()

        course1 = Course.objects.first()
        lesson1 = Lesson.objects.first() if Lesson.objects.exists() else None

        if not user1 or not course1:
            self.stdout.write(
                self.style.ERROR('Необходимо сначала создать пользователей и курсы')
            )
            return

        # Создаем платежи
        payments_data = [
            {
                'user': user1,
                'payment_date': '2024-01-15',
                'payment_course': course1,
                'payment_lesson': None,
                'amount': 5000.00,
                'payment_method': Payment.TRANSFER,
            },
            {
                'user': user1,
                'payment_date': '2024-02-20',
                'payment_course': None,
                'payment_lesson': lesson1,
                'amount': 1500.00,
                'payment_method': Payment.CASH,
            },
            {
                'user': user2,
                'payment_date': '2024-03-10',
                'payment_course': course1,
                'payment_lesson': None,
                'amount': 5000.00,
                'payment_method': Payment.TRANSFER,
            },
        ]

        for payment_data in payments_data:
            payment, created = Payment.objects.get_or_create(
                user=payment_data['user'],
                payment_date=payment_data['payment_date'],
                payment_course=payment_data['payment_course'],
                payment_lesson=payment_data['payment_lesson'],
                defaults={
                    'amount': payment_data['amount'],
                    'payment_method': payment_data['payment_method'],
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Создан платеж: {payment}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Платеж уже существует: {payment}')
                )

        self.stdout.write(
            self.style.SUCCESS('Данные для платежей успешно созданы!')
        )

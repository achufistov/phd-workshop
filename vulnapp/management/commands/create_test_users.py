from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from vulnapp.models import UserProfile
from datetime import date
import random

class Command(BaseCommand):
    help = 'Creates test users and profiles for the workshop'

    def handle(self, *args, **kwargs):
        last_names = [
            'Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов',
            'Попов', 'Васильев', 'Соколов', 'Михайлов', 'Новиков'
        ]
        
        first_names = [
            'Александр', 'Дмитрий', 'Максим', 'Иван', 'Артем',
            'Никита', 'Михаил', 'Даниил', 'Егор', 'Андрей'
        ]
        
        middle_names = [
            'Александрович', 'Дмитриевич', 'Максимович', 'Иванович', 'Артемович',
            'Никитич', 'Михайлович', 'Даниилович', 'Егорович', 'Андреевич'
        ]

        positions = [
            'Старший разработчик',
            'Младший разработчик',
            'Тестировщик',
            'DevOps инженер',
            'Системный администратор',
            'Руководитель проекта',
            'Аналитик данных',
            'Специалист по безопасности',
            'Технический писатель',
            'Специалист по поддержке'
        ]

        departments = [
            'Отдел разработки и тестирования ПО',
            'Отдел разработки и тестирования ПО',
            'Отдел разработки и тестирования ПО',
            'Отдел автоматизации',
            'Отдел автоматизации',
            'Управление проектами',
            'Отдел аналитики',
            'Отдел ИБ',
            'Отдел разработки и тестирования ПО',
            'Отдел технической поддержки'
        ]

        addresses = [
            'г. Москва, ул. Ленина, д. 10, кв. 5',
            'г. Санкт-Петербург, пр. Невский, д. 25, кв. 12',
            'г. Екатеринбург, ул. Мира, д. 15, кв. 8',
            'г. Новосибирск, ул. Гагарина, д. 30, кв. 3',
            'г. Казань, ул. Баумана, д. 20, кв. 7',
            'г. Нижний Новгород, ул. Рождественская, д. 18, кв. 4',
            'г. Самара, ул. Куйбышева, д. 22, кв. 9',
            'г. Омск, ул. Ленина, д. 35, кв. 6',
            'г. Ростов-на-Дону, ул. Большая Садовая, д. 40, кв. 11',
            'г. Уфа, ул. Октябрьской революции, д. 28, кв. 2'
        ]

        for i in range(10):
            username = f'user{i+1}'
            password = f'user{i+1}123'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'is_staff': i == 0, 
                    'is_superuser': i == 0
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user {username}'))
            
            full_name = f"{last_names[i]} {first_names[i]} {middle_names[i]}"
            passport_number = f"4521 {random.randint(100000, 999999)}"
            hire_date = date(2025, random.randint(1, 4), random.randint(1, 28))
            salary = random.randint(80000, 250000)
            position = positions[i]
            department = departments[i]
            address = addresses[i]
            phone_number = f"7{random.randint(9000000000, 9999999999)}"
            
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': full_name,
                    'passport_number': passport_number,
                    'salary': salary,
                    'position': position,
                    'department': department,
                    'hire_date': hire_date,
                    'address': address,
                    'phone_number': phone_number
                }
            )
            
            if not created:
                profile.full_name = full_name
                profile.passport_number = passport_number
                profile.salary = salary
                profile.position = position
                profile.department = department
                profile.hire_date = hire_date
                profile.address = address
                profile.phone_number = phone_number
                profile.save()
            
            self.stdout.write(self.style.SUCCESS(f'Updated profile for user {username}'))

        self.stdout.write(self.style.SUCCESS('Successfully created all test users and profiles')) 
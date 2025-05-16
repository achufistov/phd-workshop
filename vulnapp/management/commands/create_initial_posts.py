from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from vulnapp.models import Post

class Command(BaseCommand):
    help = 'Creates initial posts in each category'

    def handle(self, *args, **kwargs):
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin1234')
            admin.save()

        posts_data = {
            'strategy': {
                'title': 'Стратегия развития компании на 2025 год',
                'content': 'В этом году мы планируем расширить наше присутствие на международных рынках и запустить несколько инновационных продуктов. Основные направления развития включают цифровую трансформацию и оптимизацию бизнес-процессов.'
            },
            'innovation': {
                'title': 'Новые технологии в разработке',
                'content': 'Мы внедряем искусственный интеллект и машинное обучение в наши продукты. Это позволит нам создавать более эффективные решения для наших клиентов!'
            },
            'culture': {
                'title': 'Корпоративная культура и ценности',
                'content': 'Наша компания основана на принципах открытости, инноваций и взаимного уважения. Мы поощряем инициативу и поддерживаем профессиональный рост каждого сотрудника.'
            },
            'tech': {
                'title': 'Обновление технологического стека',
                'content': 'Мы переходим на новые версии фреймворков и библиотек, что позволит улучшить производительность и безопасность наших решений.'
            },
            'news': {
                'title': 'Открытие нового офиса',
                'content': 'Мы рады сообщить об открытии нового офиса в центре города. Мы всегда готовы создавать более комфортные условия для работы!'
            }
        }

        for category, data in posts_data.items():
            post, created = Post.objects.get_or_create(
                title=data['title'],
                defaults={
                    'content': data['content'],
                    'category': category,
                    'author': admin
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created post "{data["title"]}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Post "{data["title"]}" already exists')
                ) 
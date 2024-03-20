from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().
                filter(status=Post.Status.PUBLISHED))  # Метод get_queryset() менеджера возвращает набор запросов
        # QuerySet, который будет исполнен. Этот метод был определен, чтобы сформировать конкретно-прикладной
        # набор запросов в QuerySet, фильтрующий посты по их статусу и возвращающий посты со статусов PUBLISHED


class Post(models.Model):

    class Status(models.TextChoices):  # Класс Status используется для определения допустимых значений поля status ниже
        DRAFT = 'DF', 'DRAFT'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)  # Слаг – это короткая метка, содержащая только буквы, цифры,
    # знаки подчеркивания или дефисы. Мы будем использовать поле slug для формирования красивых и дружественных
    # для поисковой оптимизации URL-адресов постов блога;
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')  # related_name - это имя обратной связи,
    # от User к Post. Такой подход позволит легко обращаться к связанным объектам из объекта User,
    # используя обозначение user.blog_posts
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  # auto_now_add дата будет сохраняться автоматически
    # во время создания объекта поста
    updated = models.DateTimeField(auto_now=True)  # При применении параметра auto_now дата будет обновляться
    # автоматически во время сохранения объекта поста
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    # status представляет статус поста в блоге. choices  указывает, что значение поля status должно быть
    # одним из значений, определенных в классе Status
    objects = models.Manager()  # Менеджер применимый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер для опубликованных постов

    class Meta:
        ordering = ['-publish']  # Атрибут ordering - сообщает Django, что он должен
        # сортировать результаты по полю publish. Знак минуса (-) перед publish обозначает сортировку
        # в обратном порядке, т.е., от самых новых записей к самым старым.
        indexes = [
            models.Index(fields=['-publish']),
        ]     # Индексы улучшают производительность запросов к базе данных, делая поиск и сортировку
        # данных более эффективными. Здесь используется индекс для ускорения сортировки результатов
        # запросов в обратном порядке по полю publish.

    def __str__(self):
        return self.title

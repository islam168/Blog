from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']  # отображение на странице списка постов,
    # только определенные поля
    list_filter = ['status', 'created', 'publish', 'author']  # фильтр постов в админ панели по полям указанным здесь
    search_fields = ['title', 'body']  # атрибут search_fields определяем список полей, по которым можно выполнять поиск
    prepopulated_fields = {'slug': ('title',)}  # при вводе заголовка нового поста поле slug заполняется автоматически
    raw_id_fields = ['author']  # добавление поискового виджета, для поиска автора
    date_hierarchy = 'publish'  # чуть ниже строки поиска, находятся навигационные ссылки для навигации по иерархии дат
    ordering = ['status', 'publish']

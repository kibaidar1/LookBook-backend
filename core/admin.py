from django.contrib import admin

from core.models import User, Look, Comment, Clothes, ClothesLink


class LookInline(admin.TabularInline):
    model = Look.clothes.through


class ClothesInline(admin.TabularInline):
    model = Clothes.looks.through


class ClothesLinkInline(admin.TabularInline):
    model = ClothesLink


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)


@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'slug')}),
        ('Content', {'fields': ('colour', 'gender', 'description', 'image')}),
        ('Context', {'fields': ('author', 'created_at')}),
    )
    list_display = ('name', 'slug', 'created_at', 'author', 'colour', 'gender')
    list_filter = ('name', 'colour', 'gender')
    search_fields = ('name', 'slug', 'author')
    prepopulated_fields = {'slug': ('name',)}

    inlines = [
        ClothesLinkInline,
        LookInline,
    ]


@admin.register(Look)
class LookAdmin(admin.ModelAdmin):
    fieldsets = (None, {'fields': ('name', 'slug')}), \
        ('Content', {'fields': ('description', 'gender', 'image')}), \
        ('Context', {'fields': ('author', 'created_at')}),
    list_display = ('name', 'slug', 'gender', 'author', 'created_at',)
    list_filter = ('name', 'gender', 'author', 'created_at')
    search_fields = ('name', 'slug', 'author')
    prepopulated_fields = {'slug': ('name',)}

    inlines = [
        ClothesInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('look', 'author', 'created_at', 'text')
    list_display = ('author', 'look', 'created_at')
    list_filter = ('author', 'look', 'created_at')
    search_fields = ('author', 'look')



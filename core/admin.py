from django.contrib import admin
from django.forms import modelformset_factory

from core.models import User, Look, Comment, Clothes, ClothesLink, LookImages, ClothesCategory


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


class ClothesInline(admin.StackedInline):
    model = Clothes.category.through


@admin.register(ClothesCategory)
class ClothesCategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'look')
    list_filter = ('name',)
    search_fields = ('name',)

    inlines = [ClothesInline]


class ClothesLinkInline(admin.TabularInline):
    model = ClothesLink


class ClothesCategoryInline(admin.StackedInline):
    model = ClothesCategory.clothes.through


@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'slug')}),
        ('Content', {'fields': ('colour', 'gender')}),
        ('Context', {'fields': ('author',)}),
    )
    list_display = ('name', 'slug', 'created_at', 'author', 'colour', 'gender')
    list_filter = ('name', 'colour', 'gender')
    search_fields = ('name', 'slug', 'author')
    prepopulated_fields = {'slug': ('name',)}

    inlines = [
        ClothesCategoryInline,
        ClothesLinkInline
    ]


class LookImagesInline(admin.TabularInline):
    model = LookImages
    readonly_fields = ('id', 'image_tag',)


class ClothesCategoryInLookInline(admin.TabularInline):
    model = ClothesCategory
    fields = ('name',)
    raw_id_fields = ('look',)
    show_change_link = True
    show_full_result_count = True


@admin.register(Look)
class LookAdmin(admin.ModelAdmin):
    fieldsets = (None, {'fields': ('name', 'slug')}), \
        ('Content', {'fields': ('description', 'gender',)}), \
        ('Context', {'fields': ('author',)}),
    list_display = ('name', 'slug', 'gender', 'author', 'created_at',)
    list_filter = ('name', 'gender', 'author', 'created_at')
    search_fields = ('name', 'slug', 'author')
    prepopulated_fields = {'slug': ('name',)}

    inlines = [
        LookImagesInline,
        ClothesCategoryInLookInline
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('look', 'author', 'text')
    list_display = ('author', 'look', 'created_at')
    list_filter = ('author', 'look', 'created_at')
    search_fields = ('author', 'look')



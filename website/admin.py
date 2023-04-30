from django.contrib import admin

from website.models import User, Style, Comment, Clothes


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


class StyleInline(admin.TabularInline):
    model = Style.clothes.through


class ClothesInline(admin.TabularInline):
    model = Clothes.styles.through


@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'link', 'image')
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

    model = Clothes
    inlines = [
        StyleInline,
    ]


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    fieldsets = (None, {'fields': ('name', 'slug')}), \
        ('Content', {'fields': ('description', 'image')}), \
        ('Context', {'fields': ('author', 'created_at')}),
    list_display = ('name', 'slug', 'description', 'author', 'created_at',)
    list_filter = ('name', 'author', 'created_at')
    search_fields = ('name', 'author', 'created_at',)
    prepopulated_fields = {'slug': ('name',)}

    model = Style
    inlines = [
        ClothesInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('style', 'author', 'created_at', 'text')
    list_display = ('author', 'style', 'created_at')
    list_filter = ('author', 'style', 'created_at')
    search_fields = ('author', 'style')



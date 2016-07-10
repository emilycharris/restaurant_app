from django.contrib import admin
from app.models import Order, Menu, Profile, Category, Position



# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    list_display = ["item", "description", "category", "price"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'server', 'item', 'quantity', 'notes', 'fulfilled', 'paid']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'position']

class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'position']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']

admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register (Profile, ProfileAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Category, CategoryAdmin)

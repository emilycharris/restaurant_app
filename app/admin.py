from django.contrib import admin
from app.models import Order, Menu, Profile, Category, Position, Items

# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    list_display = ["item", "description", "category", "price"]

class ItemsAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'item', 'quantity', 'notes']

class ItemsInline(admin.StackedInline):
    model = Items

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'server', 'fulfilled', 'paid']
    inlines = (ItemsInline,)

    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'position']

class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'position']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']

admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Items, ItemsAdmin)
admin.site.register (Profile, ProfileAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Category, CategoryAdmin)

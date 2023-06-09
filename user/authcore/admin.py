from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from authcore.models import User, Address, Customer


class UserAdmin(DjangoUserAdmin):
    pass


admin.register(User, UserAdmin)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    exclude = ['user']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'street', 'city')

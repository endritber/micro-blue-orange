from administration.admin import admin_site
from .models import *

# Register models to admin site here
admin_site.register(Customer)
admin_site.register(Address)

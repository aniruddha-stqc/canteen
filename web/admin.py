from django.contrib import admin
from .models import *

# Register the Thali model so it appears in the admin interface
admin.site.register(Thali)
admin.site.register(Extra)
admin.site.register(Customer)
admin.site.register(Concession)
admin.site.register(Order)
admin.site.register(Wallet)
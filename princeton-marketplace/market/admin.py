from django.contrib import admin
from market.models import Posting, Category, UserProfile
# Register your models here.

# class PostingAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Title',           {'fields': ['title']}),
#         ('Author',          {'fields': ['author']}),
#         ('Responder',       {'fields': ['responder']}),
#         ('Open',            {'fields': ['is_open']}),
#         ('Date Posted',     {'fields': ['date_posted']}),
#         ('Expiration Date', {'fields': ['date_expires']}),
#         ('Payment Method',  {'fields': ['method_of_pay']}),
#         ('Category',        {'fields': ['category']}),
#         ('Description',     {'fields': ['description']}),
#         ('Price',           {'fields': ['price']}),
#     ]

# admin.site.register(Posting, PostingAdmin)
admin.site.register(Posting)
admin.site.register(Category)
admin.site.register(UserProfile)
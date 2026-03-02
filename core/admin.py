from django.contrib.admin import AdminSite, register, ModelAdmin
from .models import Job, Internship

class JobNetAdminSite(AdminSite):
    site_header = "JobNet Admin"
    site_title = "JobNet Portal"
    index_title = "Manage Jobs & Internships"

jobnet_admin = JobNetAdminSite(name="jobnet_admin")

@register(Job, site=jobnet_admin)
class JobAdmin(ModelAdmin):
    list_display = ('title', 'company', 'location', 'posted_on','salary')
    search_fields = ('title', 'company')
    list_filter = ('location', 'company')

@register(Internship, site=jobnet_admin)
class InternshipAdmin(ModelAdmin):
    list_display = ('title', 'company', 'location', 'stipend', 'duration','skills')
    search_fields = ('title', 'company')
    list_filter = ('location', 'company', 'duration')

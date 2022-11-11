from django.contrib import admin

from .models import Student

class StudentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_filter = ('subject', 'name')
    list_display = ('id', 'roll_no', 'name', 'subject', 'marks', 'updated_at',)
    search_fields = ['name','roll_no']

admin.site.site_header = "Student Data Admin"
admin.site.site_title = 'Student Data Administration'
admin.site.index_title = 'Student Data Administration'
admin.site.register(Student, StudentAdmin)

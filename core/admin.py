from django.contrib import admin
from .models import Service, ReferenceCase, ReferenceImage, Project, ProjectAccess, ProjectFile, ContactMessage

class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 1

class ProjectAccessInline(admin.TabularInline):
    model = ProjectAccess
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    search_fields = ("title",)

class ReferenceImageInline(admin.TabularInline):
    model = ReferenceImage
    extra = 1

@admin.register(ReferenceCase)
class ReferenceCaseAdmin(admin.ModelAdmin):
    list_display = ("title", "client_name", "completion_date", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "client_name")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ReferenceImageInline]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "customer_name", "status", "owner", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "customer_name", "owner__username")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectAccessInline, ProjectFileInline]

@admin.register(ProjectAccess)
class ProjectAccessAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "can_view_schemes", "can_view_source", "can_view_files", "active")
    list_filter = ("active", "can_view_schemes", "can_view_source", "can_view_files")
    search_fields = ("project__title", "user__username")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "created_at", "is_processed")
    list_filter = ("is_processed",)
    search_fields = ("name", "email", "company", "message")

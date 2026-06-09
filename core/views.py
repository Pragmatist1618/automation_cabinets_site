from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods
from .forms import ContactForm
from .models import Service, ReferenceCase, ReferenceImage, Project, ProjectAccess, ProjectFile

def home(request):
    services = Service.objects.all()
    references = ReferenceCase.objects.filter(is_published=True)[:3]
    return render(request, "core/home.html", {"services": services, "references": references})

def references(request):
    items = ReferenceCase.objects.filter(is_published=True)
    return render(request, "core/references.html", {"references": items})

def reference_detail(request, slug):
    item = get_object_or_404(ReferenceCase, slug=slug, is_published=True)
    images = item.images.all()
    return render(request, "core/reference_detail.html", {"item": item, "images": images})

@require_http_methods(["GET", "POST"])
def contacts(request):
    form = ContactForm(request.POST or None)
    success = False
    if request.method == "POST" and form.is_valid():
        form.save()
        success = True
        form = ContactForm()
    return render(request, "core/contacts.html", {"form": form, "success": success})

@login_required
def dashboard(request):
    accesses = ProjectAccess.objects.select_related("project").filter(user=request.user, active=True)
    projects = [a.project for a in accesses]
    return render(request, "core/dashboard.html", {"projects": projects})

@login_required
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    access = ProjectAccess.objects.filter(project=project, user=request.user, active=True).first()
    if not access and not request.user.is_staff and project.owner_id != request.user.id:
        raise Http404("Нет доступа к проекту")

    files = ProjectFile.objects.filter(project=project)
    if not request.user.is_staff and project.owner_id != request.user.id:
        if not access.can_view_files:
            files = files.none()
        else:
            if not access.can_view_schemes:
                files = files.exclude(category=ProjectFile.Category.SCHEME)
            if not access.can_view_source:
                files = files.exclude(category=ProjectFile.Category.SOURCE)

    return render(request, "core/project_detail.html", {"project": project, "files": files, "access": access})

@login_required
def download_file(request, pk):
    file_obj = get_object_or_404(ProjectFile, pk=pk)
    project = file_obj.project
    access = ProjectAccess.objects.filter(project=project, user=request.user, active=True).first()
    allowed = request.user.is_staff or project.owner_id == request.user.id or access is not None
    if not allowed:
        raise Http404("Нет доступа")

    if access and not request.user.is_staff and project.owner_id != request.user.id:
        if file_obj.category == ProjectFile.Category.SCHEME and not access.can_view_schemes:
            raise Http404("Нет доступа")
        if file_obj.category == ProjectFile.Category.SOURCE and not access.can_view_source:
            raise Http404("Нет доступа")
        if not access.can_view_files:
            raise Http404("Нет доступа")

    response = FileResponse(file_obj.file, as_attachment=True, filename=file_obj.file.name.split("/")[-1])
    return response

@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: " + request.build_absolute_uri(reverse("sitemap")),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")

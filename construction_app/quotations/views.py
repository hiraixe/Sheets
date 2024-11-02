from django.shortcuts import render, redirect
from .models import Project, ProjectElement, Material, Quotation
from django.contrib.auth.decorators import login_required


@login_required
def request_quotation(request):
    if request.method == 'POST':
        area_size = request.POST['area_size']
        selected_elements = request.POST.getlist('elements')
        selected_materials = request.POST.getlist('materials')

        project = Project.objects.create(
            description="New Project",
            location="Sample Location",
            created_by=request.user,
            status="PENDING"
        )

        for element_id in selected_elements:
            element = ProjectElement.objects.get(id=element_id)
            element.project = project
            element.save()

            for material_id in selected_materials:
                material = Material.objects.get(id=material_id)
                if material.element == element:
                    material.save()

        return redirect('quotation_list')

    # Load elements and materials for selection
    elements = ProjectElement.objects.all()
    materials = Material.objects.all()
    return render(request, 'request_quotation.html', {'elements': elements, 'materials': materials})


@login_required
def quotation_list(request):
    quotations = Quotation.objects.filter(user=request.user)
    return render(request, 'quotation_list.html', {'quotations': quotations})


@login_required
def quotation_detail(request, pk):
    quotation = Quotation.objects.get(id=pk)
    return render(request, 'quotation_detail.html', {'quotation': quotation})
from django.shortcuts import render

# Create your views here.

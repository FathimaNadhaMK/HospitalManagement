from.models import DepartmentModel

def department_list(request):
    department_link=DepartmentModel.objects.all()
    return dict(dept_list=department_link)
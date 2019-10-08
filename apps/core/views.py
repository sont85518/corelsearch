from apps.settings import BASE_DIR
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

from search import service


class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        if name.split('.')[-1] not in ['jpg', 'JPG', 'JPEG', 'png', 'PNG', 'jpeg']:
            return render(request, 'upload.html', {'error': 'Your file should be a image!'})

    return render(request, 'upload.html', context)


def search(request):
    context = {}
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)

            if name.split('.')[-1] not in ['jpg', 'JPG', 'JPEG', 'png', 'PNG', 'jpeg']:
                return render(request, 'upload.html', {'error': 'Your file should be a image!'})

            try:
                respone = service.search(fs.location + '/' + name, t=0.73)
            except:
                return render(request, 'upload.html', {'error': 'An error occurred!'})

            list_img = ['/static/' + x[0] for x in respone]

            context['returned'] = list_img
        except Exception as ex:
            return render(request, 'search.html', context)

    try:
        return render(request, 'search.html', context)
    except Exception as ex:
        print(ex)
        render(request, 'home.html', context)

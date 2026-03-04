from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class IndexView(View):
    """Main index view displaying service status"""

    def get(self, request):
        context = {
            'status_en': 'Service Status: Online',
            'status_zh': '服務狀態：在線',
        }
        return render(request, 'index.html', context)


@method_decorator(login_required, name='dispatch')
class FileManagerView(View):
    """File manager GUI view"""

    def get(self, request):
        return render(request, 'file_manager.html')

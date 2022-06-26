from msilib.schema import ListView
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from eventex.core.models import Course, Speaker, Talk

home = ListView.as_view(template_name='index.html', model = Speaker)

def speaker_detail(request, slug):
    # speaker = Speaker(
    #         name = 'Grace Hopper',
    #         slug = 'grace-hopper',
    #         title = 'Programadora e almirante',
    #         photo = 'https://hbn.link/hopper-pic',
    #         website = 'https://hbn.link/hopper-site',
    #         description = 'Inventora do compilador, criadora da linguagem de programação Flow-Matic. A Linguagem serviu de base para a linguagem COBOL permitindo a popularização das aplicações comerciais.'
    #     )    
    #speaker = Speaker.objects.get(slug=slug)
    speaker = get_object_or_404(Speaker,slug=slug)
    return render(request,'core/speaker_detail.html',{'speaker':speaker}) 

talk_list = ListView.as_view(model=Talk)
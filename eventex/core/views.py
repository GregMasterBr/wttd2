from multiprocessing import context
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from eventex.core.models import Course, Speaker, Talk

class HomeView(View):
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        #speakers = Speaker.objects.all()
        #return render(self.request, self.template_name,{'speakers':speakers})
        context = self.get_context_data()
        return self.render_to_response({'speakers':speakers})

    def render_to_response(self, context):
       return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        speakers = Speaker.objects.all()
        context = {'speakers':speakers}
        context.update(kwargs)
        return context 
# def home(request):
#     # speakers = [
#     #     {
#     #         'name':'Grace Hopper',
#     #         'photo':'https://hbn.link/hopper-pic',
#     #         'title':'Programadora e almirante'
#     #     },
#     #     {
#     #         'name':'Alan Turing',
#     #         'photo':'https://hbn.link/turing-pic',
#     #         'title':'Físico'
#     #     }        
#     # ]
#     speakers = Speaker.objects.all()
#     return render(request,'index.html',{'speakers':speakers})

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

def talk_list(request):
    # context = {
    #     'morning_talks': [Talk(title='Título da Palestra', start='10:00', description='Descrição da palestra.')],
    #     'afternoon_talks':[Talk(title='Título da Palestra', start='13:00', description='Descrição da palestra.')],
    # }
    # context = {
    #     'morning_talks': Talk.objects.filter(start__lt='12:00'),
    #     'afternoon_talks': Talk.objects.filter(start__gte='12:00'),
    # }    
    
    #speaker = Speaker(name='Henrique Bastos', slug='henrique-bastos')
    #simular um queryset
    #courses = [dict(title='Título do Curso', start='09:00', description='Descrição do curso.',speakers={'all':[speaker]})]

    # at_morning = list(Talk.objects.at_morning()) + list(Course.objects.at_morning())
    # at_morning.sort(key=lambda o: o.start)

    # at_afternoon = list(Talk.objects.at_afternoon()) + list(Course.objects.at_afternoon())
    # at_afternoon.sort(key=lambda o: o.start)    

    context = {
        'morning_talks': Talk.objects.at_morning(),
        'afternoon_talks': Talk.objects.at_afternoon(),
    }        
    return render(request,'core/talk_list.html' , context) 

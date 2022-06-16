from django.shortcuts import render

# Create your views here.

def home(request):
    speakers = [
        {
            'name':'Grace Hopper',
            'photo':'https://hbn.link/hopper-pic',
            'subject':'Tema X'
        },
        {
            'name':'Alan Turing',
            'photo':'https://hbn.link/turing-pic',
            'subject':'Tema Y'
        }        
    ]
    return render(request,'index.html',{'speakers':speakers})

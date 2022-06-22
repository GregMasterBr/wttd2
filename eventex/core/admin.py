from django.contrib import admin
from django.utils.html import format_html
from eventex.core.models import Contact, Speaker, Talk


class ContactInLine(admin.TabularInline):
    model = Contact
    extra = 1
    #max_num = 1

class SpeakerModelAdmin(admin.ModelAdmin):
    inlines = [ContactInLine]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['photo_img', 'name', 'website_link','get_contato']
    search_fields = ('name',)
    
    def get_contato(self, obj):
        #return obj.link.value
        return  'colocar a forma de contato'

    get_contato.short_description = 'Contato'  #Renames column head    

    def website_link(self, obj):
        #return '<a href="{0}" target="blank">{0}</a>'.format(obj.website)
        return format_html('<a href="{0}" target="blank">{0}</a>', obj.website)
    
    website_link.short_description = 'website'

    def photo_img(self,obj):
        return format_html('<img width="32px" src="{0}" alt="foto do palestrante" />', obj.photo)
    
    photo_img.short_description = 'foto'

admin.site.register(Speaker, SpeakerModelAdmin)
admin.site.register(Talk)
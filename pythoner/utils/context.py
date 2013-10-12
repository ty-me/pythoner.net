from django.conf import settings

def settings_processor(request):
        my_dict= {
                'VERSION':settings.VERSION,
                'DEBUG':settings.DEBUG,
        }
        return my_dict


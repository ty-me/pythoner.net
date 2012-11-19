#encoding:utf-8
from django.http import HttpResponse
import Image,ImageDraw,ImageFont,random,StringIO
import time,os

def display(request):

    string = {'number':'123456789',
              'litter':'ABCEFGHKMNPRTUVWXY'}
    # the worlds list maxlength = 8
    worlds = [
        'about',
        'bronze',
        'blouse',
        'china',
        'complex',
        'document',
        'django',
        'facebook',
        'finally',
        'freezer',
        'github',
        'google',
        'instance',
        'linux',
        'lambda',
        'mysql',
        'object',
        'python',
        'syntax',
        'twitter',
    ]
    background = (random.randrange(230,255),random.randrange(230,255),random.randrange(230,255))
    img_width = 150
    img_height = 30
    font_color = ['black','darkblue','darkred']
    font_size = 24
    current_path = os.path.normpath(os.path.dirname(__file__))
    font = ImageFont.truetype(os.path.join(current_path,'timesbi.ttf').replace('\\','/'),font_size)
    request.session['verify'] = ''

    # creat a image
    im = Image.new('RGB',(img_width,img_height),background)
    #code = random.sample(string['litter'],4)
    code = worlds[random.randrange(0,len(worlds))]
    # creat a pen
    draw = ImageDraw.Draw(im)

    # draw lines
    for i in range(random.randrange(3,5)):
        line_color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        xy = (random.randrange(0,img_width/4),random.randrange(0,img_height),
              random.randrange(3*img_width/4,img_width),random.randrange(0,img_height))
        draw.line(xy,fill=line_color,width=1)

    # draw the litter
    x = random.randrange(10,20)
    for i in code:
        y = random.randrange(0,5)
        draw.text((x,y), i, font=font, fill=random.choice(font_color))
        x += 16
        request.session['verify'] += i
    del x

    del draw
    buf = StringIO.StringIO()
    im.save(buf,'gif')
    buf.closed
    return HttpResponse(buf.getvalue(),'image/gif')

# check verify code
def check_verify(request):
    try:
        if request.GET.get('verify').upper() == request.session.get('verify','').upper():
            return True
    except :
        pass
    return False

def set(request):
    """
    set mark
    """
    try:
        request.session['action_times'] = request.session['action_times']+1
    except KeyError,e:
        request.session['action_times'] = 0

    request.session['time_stamp'] = time.time()

def reset(request):
    """
    reset mark
    """
    request.session['action_times'] = 0
    request.session['time_stamp'] = time.time()

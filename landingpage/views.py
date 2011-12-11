from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from marketingforhackers.landingpage.models import Lead
from mailsnake import MailSnake
from marketingforhackers import settings

def index(request):
    # try to figure out where they came from
    try:
        referrer = request.META.get('HTTP_REFERER')
    except AttributeError:
        referrer = "direct"
        
    analytics = {"referrer": referrer}
    
    return render_to_response("index.html", analytics, context_instance=RequestContext(request))
    
def submit(request):
    # grab info
    email = request.POST['email']
    referrer = request.POST['referrer']
    
    # save locally
    lead_to_submit = Lead(email=email, referrer=referrer)
    lead_to_submit.save()
    
    # send to Mailchimp
    key = settings.MAILCHIMP_API_KEY
    list = settings.MAILCHIMP_LIST_NUM
    
    # see: http://www.nerdydork.com/integrate-mailchimp-with-your-django-app.html
    mailsnake = MailSnake(key)
    mailsnake.listSubscribe(
        id = list,
        email_address = email,
        double_optin = False,
        send_welcome = True
    )
    
    return  HttpResponseRedirect(reverse('landingpage.views.thanks'))
    
def thanks(request):
    return render_to_response("thanks.html")
    
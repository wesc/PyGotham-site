# Create your views here.
import re

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from settings import MEDIA_URL,SSL_MEDIA_URL,MAX_SPONSORED,MAX_PAID
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from confreg.models import ConfRegModel,FreeCodes,FreeCodesUsers,EmailNotifications
from confreg.forms import ConfRegForm
from decimal import Decimal

@login_required
def conf_register(request):
    generic_error = None

    # Count current number of registered. If we exceed max, get out.
    paid_regs = ConfRegModel.objects.filter(paid__gt = Decimal('0') ).count()
    spons_regs = ConfRegModel.objects.filter(payment_amount_method = 'need_sponsorship').count()

    template_name = 'confreg/conf_reg.html'

    # If user is not active, get out.
    userobj = User.objects.get(username=request.user.username)
    if not userobj.is_active:
        return redirect(MEDIA_URL + '/confreg/need_to_activate')

    # If user already registered, see if they paid, etc.
    try:
        confreg = ConfRegModel.objects.get(user=request.user)
        if confreg.paid <= Decimal('0') and not confreg.got_sponsored \
            and not confreg.freebee and not confreg.payment_amount_method == 'need_sponsorship':
            return redirect(SSL_MEDIA_URL + '/confreg/payment')

        template_name = 'confreg/already_entered.html'
        form = ConfRegForm()

    except ConfRegModel.DoesNotExist:
        if paid_regs + spons_regs >= MAX_PAID + MAX_SPONSORED:
            template_name = 'confreg/soldout.html'
            form = ConfRegForm()
  
        # This is what we expect
        elif request.method == 'POST':
            form = ConfRegForm(request.POST)
            # cache: add user tracking, so payment save can be tracked.
            if form.is_valid():
                if not form.cleaned_data['read_the_policy']:
                    generic_error = 'You have to check that you\'ve read the policy to continue.'
                elif form.cleaned_data['payment_amount_method'] == 'need_sponsorship':
                    if spons_regs >= MAX_SPONSORED:
                        generic_error = 'Sorry, we\'ve reached our max number of sponsorships.'
                    else:
                        confreg = ConfRegModel.objects.create(user=request.user)
                        newform = ConfRegForm(request.POST,instance=confreg)
                        newform.save()
                        template_name = 'confreg/on_hold.html'
    
                elif form.cleaned_data['payment_amount_method'] == 'freebee_code':
                    try:
                        legit_code = FreeCodes.objects.get(code = form.cleaned_data['discount_code'])
                        FreeCodesUsers.objects.create(user = request.user, code = legit_code)
                        template_name = 'confreg/in_default.html'
                        confreg = ConfRegModel.objects.create(user=request.user)
                        confreg.freebee = True
                        newform = ConfRegForm(request.POST,instance=confreg)
                        newform.save()
                    except FreeCodes.DoesNotExist:
                        generic_error = 'Sorry, this discount code doesn\'t exist.'
                else:
                    confreg = ConfRegModel.objects.create(user=request.user)
                    newform = ConfRegForm(request.POST,instance=confreg)
                    newform.save()
                    return redirect(SSL_MEDIA_URL + '/confreg/payment')
        else:
            form = ConfRegForm()
    
    context = RequestContext(request)

    return render_to_response(template_name,
              {'form': form, 'SSL_MEDIA_URL': SSL_MEDIA_URL,'generic_error':generic_error},
              context_instance=context)

@login_required
def payment(request):
    confreg = ConfRegModel.objects.get(user=request.user)
    if confreg.payment_amount_method == 'indiv_amt':
        template_name = 'confreg/paypal_103.html'
    elif confreg.payment_amount_method == 'corp_amt':
        template_name = 'confreg/paypal_205.html'
    else:
        #default
        template_name = 'confreg/paypal_103.html'
    context = RequestContext(request)

    return render_to_response(template_name,
          {'SSL_MEDIA_URL': SSL_MEDIA_URL},
          context_instance=context)


@login_required
def user_state(request):
    # If user already registered, see if they paid, etc.
    try:
        confreg = ConfRegModel.objects.get(user=request.user)
        if confreg.paid <= Decimal('0') and not confreg.got_sponsored \
            and not confreg.freebee and confreg.payment_amount_method != 'need_sponsorship':
            #import pprint
            #return HttpResponse(pprint.pformat(confreg.__dict__))
            return redirect(SSL_MEDIA_URL + '/confreg/payment')

        template_name = 'confreg/already_entered.html'
        context = RequestContext(request)
    
        return render_to_response(template_name,
              {'SSL_MEDIA_URL': SSL_MEDIA_URL},
              context_instance=context)

    except ConfRegModel.DoesNotExist:
        # They need to register.
        return conf_register(request)

@login_required
def conf_edit(request):
    pass

@csrf_exempt
@login_required
def check_paypal_success(request,slug=None):
    # Prevent dumb hacking
    referer = request.META.get('HTTP_REFERER', '')
    if not re.match('https://www.paypal.com.*$',referer):
        return redirect(SSL_MEDIA_URL + '/')

    amount = slug
    confreg = ConfRegModel.objects.get(user=request.user)
    confreg.paid = Decimal(amount)
    confreg.save()
    template_name = 'confreg/in_default.html'
    context = RequestContext(request)
    
    return render_to_response(template_name,
          {'SSL_MEDIA_URL': SSL_MEDIA_URL,'amount':amount},
          context_instance=context)

@login_required
def check_paypal_fail(request):
    template_name = 'confreg/pay_later.html'
    context = RequestContext(request)
    
    return render_to_response(template_name,
          {'SSL_MEDIA_URL': SSL_MEDIA_URL},
          context_instance=context)

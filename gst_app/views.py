from django.template import loader
import pdfkit
import os
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from urllib import request, response
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required



from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime


from paytm import Checksum

MERCHANT_KEY = 'f63ilt9f9!374rCZ'



# Create your views here.

def index(requests):

    return render(requests, 'landing/index.html')


def about(requests):

    return render(requests, 'about/about.html')


def contact(requests):

    return render(requests, 'contact/contact.html')

def faq(requests):

    return render(requests, 'faq/faq.html')

def terms(requests):

    return render(requests, 'terms/terms.html')

def policy(requests):

    return render(requests, 'terms/terms.html')

def blogs(requests):

    blogs = blog.objects.all()

    return render(requests, 'blog/blog.html',{'blogs':blogs})

@staff_member_required(login_url='/')
def delete_blogs(requests,id):

    blog.objects.all().filter(id=id).delete()

    return redirect("/create_blogs")

    

@staff_member_required(login_url='/')
def create_blogs(request):

    blogs = blog.objects.all()


    if request.method == "POST":

        heading1 = request.POST.get('heading1', None)
        description = request.POST.get('description', None)
        image = request.FILES.get('image', None)

        blog.objects.create(heading1=heading1,description=description,image=image)

        return redirect("/create_blogs")

    return render(request, 'blog/create_blogs.html',{'blogs':blogs})


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/')  # redirect when user is not logged in
def form_view(request):

    username = request.user.username

    user_id = request.user.id

    num = phone_numbers.objects.filter(user_name=username)

    all_states=states.objects.all()
    
    pri=price.objects.all()

    if request.method == "POST":

        full_name = request.POST.get('full_name', None)
        company_name = request.POST.get('company_name', None)
        company_type = request.POST.get('company_type', None)
        company_address = request.POST.get('company_address', None)
        gst_number = request.POST.get('gst_number', None)
        p_number = request.POST.get('p_number', None)
        email = request.POST.get('email', None)
        amount_input = request.POST.get('amount', None)
        total_states = request.POST.get('total_states', None)
        state = request.POST.get('state', None)
        # aadhar_card = request.FILES.get('aadhar_card')
        # photograph = request.FILES.get('photograph', None)
        # proof_of_address = request.FILES.get('proof_of_address', None)
        # pan_card = request.FILES.get('pan_card', None)
        # aadhar_card = request.FILES.get('aadhar_card',None)
        # photograph = request.FILES.get('photograph', None)
        # proof_of_address = request.FILES.get('proof_of_address', None)
        # pan_card = request.FILES.get('pan_card', None)
        
        # print(state)

        # state_list = []

        # Maharashtra = request.POST.get('Maharashtra', None)
        # if Maharashtra == "Maharashtra":
        #     state_list.append('Maharashtra')

        # Gujrat = request.POST.get('Gujrat', None)
        # if Gujrat == "Gujrat":
        #     state_list.append('Gujrat')

        # Karnataka = request.POST.get('Karnataka', None)
        # if Karnataka == "Karnataka":
        #     state_list.append('Karnataka')

        # West_Bengal = request.POST.get('West_Bengal', None)
        # if West_Bengal == "West_Bengal":
        #     state_list.append('West Bengal')

        # Telangana = request.POST.get('Telangana', None)
        # if Telangana == "Telangana":
        #     state_list.append('Telangana')

        # Delhi = request.POST.get('Delhi', None)
        # if Delhi == "Delhi":
        #     state_list.append('Delhi')

        # Rajasthan = request.POST.get('Rajasthan', None)
        # if Rajasthan == "Rajasthan":
        #     state_list.append('Rajasthan')

        # Bihar = request.POST.get('Bihar', None)
        # if Bihar == "Bihar":
        #     state_list.append('Bihar')

        # AndhraPradesh = request.POST.get('AndhraPradesh', None)
        # if AndhraPradesh == "AndhraPradesh":
        #     state_list.append('Andhra Pradesh')

        # listToStr = ' '.join(map(str, state_list))

        # docs = documents.objects.create(aadhar_card=aadhar_card, photograph=photograph, proof_of_address=proof_of_address, pan_card=pan_card)

        username = request.user.username

        obj, created = phone_numbers.objects.get_or_create(user_name=username)
        obj.phone_number = request.POST.get('p_number', None)
        obj.user_name = username
        obj.save()

        # aadhar_card=aadhar_card, photograph=photograph, proof_of_address=proof_of_address, pan_card=pan_card,

       
        done = orders.objects.create(gst_number=gst_number,company_addess=company_address,user_id=user_id, user_name=username, full_name=full_name, company_name=company_name, company_type=company_type, p_number=p_number, email=email, total_amount=amount_input, total_states=total_states, state=state)
        
        return redirect("/order_page/"+str(done.id))

    else:
        return render(request, 'form/form.html', {'numbers': num,'all_states':all_states,'pri':pri})


@csrf_exempt
@login_required(login_url='/')
def order_page(request, id):

    username = request.user.username
   

        # orders_placed1 = orders.objects.all().filter(user_name=username, id=(list_1[i]))

    orders_placed = orders.objects.get(id=id)     
    
    pri = price.objects.all()

    param_dict = {

        'MID': 'XJailZ92874680327655',
        'ORDER_ID': str(id),
        'TXN_AMOUNT': str(orders_placed.total_amount),
        'CUST_ID': str(request.user.id),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'DEFAULT',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'https://www.thegstco.com/handlerequest/' + str(orders_placed.id) + str("/") + str(request.user.id)+str("/"),
        # 'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/' + str(orders_placed.id) + str("/") + str(request.user.id)+str("/"),

    }

    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)

    total_amount = str(orders_placed.total_amount),
    
    return render(request, 'order_page/order_page.html', {'param_dict': param_dict,'pri':pri,'state_str':orders_placed.state,'total_amount':orders_placed.total_amount,'total_states':orders_placed.total_states})

    # ===========================================================================================================================================================


@csrf_exempt
def handlerequest(request, id, user_id):

    user = User.objects.get(id=user_id)

    
    orders_placed = orders.objects.get(id=id)

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            
            orders.objects.filter(id=id).update(payment="paid")
            
            return render(request, 'order/order_successful.html', {'id': id})
        else:
            return render(request, 'order/order_successful.html', {'id': id})
    return render(request, 'order/order_unsuccessful.html', {'response': response_dict})



# for generating pdf invoice
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os



def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


from django.views.generic import  View

class GenerateInvoice(View):
    
    def get(self, request, pk, *args, **kwargs):
        try:
            order_db = orders.objects.get(id = pk, user_name = request.user.username)  
            pri=price.objects.all()  #you can filter using order_id as well
        except:
            return HttpResponse("505 Not Found")
        data = {
            'order_id': order_db.id,
            'user_email': order_db.email,
            'date': str(order_db.date),
            'name': order_db.full_name,
            'order': order_db,
            'amount': order_db.total_amount,
            'state':order_db.state,
            'total_states': order_db.total_states,
            'pri':pri
        }
        pdf = render_to_pdf('invoice/invoice.html',data )
        # return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



def invoice (request,id):
        try:
            order_db = orders.objects.get(id = id, user_name = request.user.username)     #you can filter using order_id as well
        except:
            return HttpResponse("505 Not Found")
        data = {
            'order_id': order_db.id,
            'user_email': order_db.email,
            'date': str(order_db.date),
            'name': order_db.full_name,
            'order': order_db,
            'amount': order_db.total_amount,
            'state':order_db.state,
            'total_states': order_db.total_states
        }
        # pdf = render_to_pdf('invoice/invoice.html',data )
        # # return HttpResponse(pdf, content_type='application/pdf')

        # # force download
        # if pdf:
        #     response = HttpResponse(pdf, content_type='application/pdf')
        #     filename = "Invoice_%s.pdf" %(['order_id'])
        #     content = "inline; filename='%s'" %(filename)
        #     #download = request.GET.get("download")
        #     #if download:
        #     content = "attachment; filename=%s" %(filename)
        #     response['Content-Disposition'] = content
        #     return response
        # return HttpResponse("Not found")

        return render(request, 'invoice/invoice.html',data)





@login_required(login_url='/')
def upload_docments(request, id):

    username = request.user.username

    orders_placed1 = orders.objects.get(id=id, user_name=username)


    if orders_placed1.proof_of_address and orders_placed1.aadhar_card and orders_placed1.photograph and orders_placed1.pan_card :

        return redirect("/")
    

    if orders_placed1.proof_of_address:
        proof_of_address1=True
    else:
        proof_of_address1=False


    if orders_placed1.aadhar_card:
        aadhar_card1=True
    else:
        aadhar_card1=False

    if orders_placed1.photograph:
        photograph1=True
    else:
        photograph1=False

    if orders_placed1.pan_card:
        pan_card1=True
    else:
        pan_card1=False


    if request.method == "POST":

        orders_done = orders.objects.get(id=id, user_name=username)

        aadhar_card = request.FILES.get('aadhar_card',None)
        if aadhar_card != None:
            orders_done.aadhar_card = aadhar_card
        
        photograph = request.FILES.get('photograph', None)
        if photograph != None:
            orders_done.photograph = photograph
        
        proof_of_address = request.FILES.get('proof_of_address', None)
        if proof_of_address != None:
          orders_done.proof_of_address = proof_of_address

        pan_card = request.FILES.get('pan_card', None)
        if pan_card != None:
            orders_done.pan_card = pan_card

        orders_done.save()
                
        return redirect('/order')

        # orders.objects.create(aadhar_card=aadhar_card,photograph=photograph,proof_of_address=proof_of_address,pan_card=pan_card)

    return render(request, 'form/upload_docments.html',{'proof_of_address':proof_of_address1,'aadhar_card':aadhar_card1,'photograph':photograph1,'pan_card':pan_card1})




@login_required(login_url='/')  # redirect when user is not logged in
def order(requests):

    pri = price.objects.all()

    orders_placed = orders.objects.all().filter(user_name=requests.user.username, user_id=requests.user.id,payment="paid").order_by("-id")
    
    return render(requests, 'order/order_details.html', {'orders_placed': orders_placed,'pri':pri})


@login_required(login_url='/')  # redirect when user is not logged in
def profile(request):

    # user_id = request.user.user_id

    username = request.user.username

    numbers = phone_numbers.objects.filter(user_name=username)

    if request.method == "POST":

        phone_number = request.POST.get('phone_number', None)
        user_name = request.POST.get('user_name', None)

        obj, created = phone_numbers.objects.get_or_create(user_name=user_name)
        obj.phone_number = request.POST.get('phone_number', None)
        obj.user_name = request.POST.get('user_name', None)
        obj.save()

        # obj1,created=orders.objects.get_or_create(user_name=user_name)
        # obj1.p_number=request.POST.get('phone_number', None)
        # obj1.save()

        messages.info(request, 'Phone Number Saved successfully!')
        return render(request, 'profile/profile.html', {"numbers": numbers})

    return render(request, 'profile/profile.html', {"numbers": numbers})

@login_required(login_url='/')  # redirect when user is not logged in
@staff_member_required(login_url='/')
def admin_panel(requests):

    orders_list = orders.objects.all().filter(payment="paid").order_by("-id")

    Recieved=orders.objects.filter(payment="paid",order_status="Order Recieved").count()
    Processing=orders.objects.filter(payment="paid",order_status="Processing").count()
    Submitted=orders.objects.filter(payment="paid",order_status="Submitted For Approval").count()
    Completed=orders.objects.filter(order_status="Order Completed").count()
    total=orders.objects.filter(payment="paid").count()

    pri = price.objects.all()

    if requests.method == "POST":
        state_price = requests.POST.get('price', None)

        percentage_price = requests.POST.get('percentage_price', None)

        percentage = requests.POST.get('percentage', None)
        
        price.objects.all().delete()

        price.objects.create(state_price=state_price,percentage_price=percentage_price,percentage=percentage)

        return(redirect("/admin_panel"))

    return render(requests, 'admin_panel/index.html', {"orders": orders_list,'pri':pri,'Recieved':Recieved,'Processing':Processing,'Submitted':Submitted,'Completed':Completed,'total':total})



@login_required(login_url='/')  # redirect when user is not logged in
@staff_member_required(login_url='/')
def admin_panel_upaid(requests):

         orders_list = orders.objects.all().filter(payment="Unpaid").order_by("-id")

         Recieved=orders.objects.filter(payment="paid",order_status="Order Recieved").count()
         Processing=orders.objects.filter(payment="paid",order_status="Processing").count()
         Submitted=orders.objects.filter(payment="paid",order_status="Submitted For Approval").count()
         Completed=orders.objects.filter(order_status="Order Completed").count()
         total=orders.objects.filter(payment="paid").count()

         pri = price.objects.all()

         return render(requests, 'admin_panel/index_copy.html', {"orders": orders_list,'pri':pri,'Recieved':Recieved,'Processing':Processing,'Submitted':Submitted,'Completed':Completed,'total':total})





@login_required(login_url='/') 
@staff_member_required(login_url='/')
def order_information(requests,id):

    order_db1 = orders.objects.get(id=id)

    order_db = orders.objects.all().filter(id=id)

    return render(requests, 'order_information/order_information.html',{'order_db':order_db})


@login_required(login_url='/')  # redirect when user is not logged in
@staff_member_required(login_url='/')
def users_database(requests):

    numbers = phone_numbers.objects.all()
    users = User.objects.all()

    return render(requests, 'admin_panel/users_database.html', {"numbers": numbers, "users": users})





@login_required(login_url='/')  # redirect when user is not logged in
@staff_member_required(login_url='/')
def change_order_status(self, pk,status):

    try:
        status = status.replace("-"," ")
    except:
        pass

    if  orders.objects.all().filter(id=pk).exists():
        orders.objects.all().filter(id=pk).update(order_status=status)
        orders_placed=orders.objects.get(id=pk)
        
        return redirect('/order_information/'+str(pk))

    else:
        return HttpResponseBadRequest

@login_required(login_url='/')  # redirect when user is not logged in
def logout_view(request):

    logout(request)
    return redirect('/')



@staff_member_required(login_url='/')
def all_states(request):

    states_db=states.objects.all()


    if "State_name_form" in request.POST:

        state_name = request.POST.get('state_name', None)
        state_id = request.POST.get('state_id', None)

        states.objects.create(state_name=state_name,state_id=state_id)

        return redirect('/all_states')

    if "State_price_form" in request.POST:

        state_price = request.POST.get('state_price', None)
        percentage = request.POST.get('percentage', None)

        price.objects.all().delete()

        price.objects.create(state_price=state_price,price_with_percentage=percentage)

        return redirect('/all_states')
        
       
        
    return render (request, 'admin_panel/state.html',{'states_db':states_db})

@staff_member_required(login_url='/')
def delete_states(request,id):

    states.objects.filter(id=id).delete()
    return redirect('/all_states')




import csv
@login_required(login_url='/')
@staff_member_required(login_url='/')
def getfile(request):  
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="Ketan More.csv"'  
    orders_db = orders.objects.all()  
    writer = csv.writer(response)  
    for order in orders_db:  
        writer.writerow([order.user_name,order.user_id,order.full_name,order.email,order.company_name,order.company_type,order.p_number,order.created_date,order.state,order.total_states,order.total_amount,order.payment])  
    return response  









def Maharashtra(requests):

    return render(requests, 'states/Maharashtra.html')

def Delhi(requests):

    return render(requests, 'states/Delhi.html')

def Karnataka(requests):

    return render(requests, 'states/Karnataka.html')

def Telangana(requests):

    return render(requests, 'states/Telangana.html')

def Gujarat(requests):

    return render(requests, 'states/Gujarat.html')

def Punjab(requests):

    return render(requests, 'states/Punjab.html')

from django.shortcuts import render,redirect
from . models import *
import string
import random
import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.shortcuts import get_object_or_404

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def index(request):
    return render(request,'index.html')

def create_new_account(request):
    return render(request,'create_new_account.html')

def customer_login(request):
    return render(request,'customer_login.html')

def dashboard(request,account_number):
    print(f"logger account number is {account_number}")
    logger_data=customer_register_table.objects.get(account_number=account_number)
    print(logger_data)
    x=datetime.datetime.now()
    current_date=x.strftime("%d-%b-%Y")
    print(current_date)
    current_time=x.strftime("%H:%M:%p")
    print(current_time)
    return render(request,'dashboard.html',{'logger_data':logger_data,'current_date':current_date,'current_time':current_time})

def my_accounts(request,account_number):
    print(f"logger account number is {account_number}")
    logger_data=customer_register_table.objects.get(account_number=account_number)
    print(logger_data)
    return render(request,'my_accounts.html',{'logger_data':logger_data})

def deposit(request,account_number):
    print(account_number)
    logger_data=customer_register_table.objects.get(account_number=account_number)
    print(logger_data)
    return render(request,'deposit.html',{'logger_data':logger_data})

def withdraw(request,account_number):
    logger_data=customer_register_table.objects.get(account_number=account_number)
    print(logger_data)
    return render(request,'withdraw.html',{'logger_data':logger_data})
    

def bank_statment(request,account_number):
    logger_data=customer_register_table.objects.get(account_number=account_number)
    print(logger_data)
    user_bankstatment=bank_statment_table.objects.filter(account_number=account_number)
    return render(request,'bank_statment.html',{'logger_data':logger_data,'user_bankstatment':user_bankstatment})

def admin_login(request):
    return render(request,'admin_login.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def new_account_form_submission(request):
    
    if request.method=="POST":
        print("data received")
        full_name=request.POST.get('full_name')
        print(f"full name is {full_name}")
        email_id=request.POST.get('email_id')
        print(f"email id is {email_id}")
        phone_number=request.POST.get('phone_number')
        print(f"phone number is {phone_number}")
        deposit_amount=request.POST.get('deposit_amount')
        print(f"deposit amount is {deposit_amount}")
        password=request.POST.get('password')
        print(f"password is {password}")
        
        #acoount number genrartion logic 
        random_number=random.randint(00000,99999)
        bank_code="SBI2024"
        account_number=bank_code+str(random_number)
        print(f"your new account number is {account_number}")
        
        #datatime logic
        date_time=datetime.datetime.now()
        print(f"registered datetime {date_time}")
        
        if customer_register_table.objects.filter(email_id=email_id,phone_number=phone_number):
            print("already this email and phone number has registered")
            messages.error(request,'already this email and phone number has registered',extra_tags='already')
            return render(request,'create_new_account.html')
        elif customer_register_table.objects.filter(email_id=email_id):
            print("already this email has taken")
            messages.error(request,'already this email has registered',extra_tags='already')
            return render(request,'create_new_account.html')
        elif customer_register_table.objects.filter(phone_number=phone_number):
            print("already this phone number has taken")
            messages.error(request,'already this phone number has registered',extra_tags='already')
            return render(request,'create_new_account.html')
        else:
             #to save a data into database logic
            ex1=customer_register_table(full_name=full_name,
                                    email_id=email_id,
                                    phone_number=phone_number,
                                    deposit_amount=deposit_amount,
                                    password=password,
                                    account_number=account_number,
                                    registered_dt=date_time)
            ex1.save()
            print("****data saved successfully*****")   
            
            #mail send logic
            try:
                subject="SBI Account Number Generated Successfully"
                message=f'Hi!...{full_name} your new SBI account number is {account_number}..'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email_id])
                print('Email sent successfully')
            except Exception as e:
                print('Email not sent')
            return render(request,'customer_login.html')

    else:
        print("data not received")
        return render(request,'create_new_account.html')
        


def customer_login_form_submission(request):
    if customer_register_table.objects.filter(account_number=request.POST.get('account_number'),password=request.POST.get('password')):
        print("login success")
        logger_data=customer_register_table.objects.get(account_number=request.POST.get('account_number'),password=request.POST.get('password'))
        print(logger_data)
        x=datetime.datetime.now()
        current_date=x.strftime("%d-%b-%Y")
        print(current_date)
        current_time=x.strftime("%H:%M:%p")
        print(current_time)
        return render(request,'dashboard.html',{'logger_data':logger_data,'current_date':current_date,'current_time':current_time})
    else:
        print("pls check your account number or password")
        messages.error(request,'check your account number or password',extra_tags='failed')
        return render(request,'customer_login.html')
        
        
def deposit_form_submission(request, account_number):
    if request.method == "POST":
        # Fetch the customer record using the account number
        logger_data = customer_register_table.objects.get(account_number=account_number)
        
        old_balance = logger_data.deposit_amount
        print(f"Old balance is {old_balance}")
        
        # Get the deposit amount from the form submission
        current_deposit_amount = request.POST.get('deposit_amount')
        
        
        if current_deposit_amount:
            print(f"Current deposit amount is {current_deposit_amount}")
            
            # Calculate the new balance
            new_updated_balance = int(old_balance) + int(current_deposit_amount)
            print(f"New updated balance is {new_updated_balance}")
            
            # Update the balance in the database
            logger_data.deposit_amount = new_updated_balance
            logger_data.save()  # Save the changes to the database
            print("Deposit amount updated successfully.")
            
            x=datetime.datetime.now()
            #update deposit data in bank statment
            ubs=bank_statment_table(full_name=logger_data.full_name,
                                    account_number=logger_data.account_number,
                                    deposit_number=current_deposit_amount,
                                    withdraw_amount="-",
                                    registered_dt=x,
                                    balance_amount=new_updated_balance)
            ubs.save()
            print("bank statment updated successfuly")
            
            
            messages.success(request, f'Deposited successfully! Your new balance is {new_updated_balance}', extra_tags='deposited')
            
            # Redirect to the deposit page (or another page) to prevent re-submission
            return redirect('deposit_form_submission',account_number=account_number)  # Use the name of your deposit page URL pattern
        else:
            messages.error(request, 'Deposit amount is required.')
    
    # If it's a GET request or after redirect, render the deposit form
    logger_data = customer_register_table.objects.get(account_number=account_number)
    return render(request, 'deposit.html', {'logger_data': logger_data})

    
        



def withdraw_form_submission(request, account_number):
    if request.method == "POST":
        # Fetch the customer record using the account number
        logger_data = customer_register_table.objects.get(account_number=account_number)
        
        old_balance = logger_data.deposit_amount
        print(f"Old balance is {old_balance}")
        
        
        # Get the deposit amount from the form submission
        current_withdraw_amount = request.POST.get('withdraw_amount')
        
        
        if int(current_withdraw_amount)<=int(old_balance):
            print(f"withdraw  amount is {current_withdraw_amount}")
            
            # Calculate the new balance
            new_updated_balance = int(old_balance) - int(current_withdraw_amount)
            print(f"New updated balance is {new_updated_balance}")
            
            # Update the balance in the database
            logger_data.deposit_amount = new_updated_balance
            logger_data.save()  # Save the changes to the database
            
            print("withdraw amount updated successfully.")
            x=datetime.datetime.now()
            #update deposit data in bank statment
            ubs=bank_statment_table(full_name=logger_data.full_name,
                                    account_number=logger_data.account_number,
                                    deposit_number="-",
                                    withdraw_amount=current_withdraw_amount,
                                    registered_dt=x,
                                    balance_amount=new_updated_balance)
            ubs.save()
            print("bank statment updated successfuly")
            messages.success(request, f'withdrw successfully! Your new balance is {new_updated_balance}', extra_tags='deposited')
            
            # Redirect to the deposit page (or another page) to prevent re-submission
            return redirect('withdraw_form_submission',account_number=account_number)  # Use the name of your deposit page URL pattern
        else:
            messages.error(request, 'insufficient fund',extra_tags='failed')
    
    # If it's a GET request or after redirect, render the deposit form
    logger_data = customer_register_table.objects.get(account_number=account_number)
    return render(request, 'withdraw.html', {'logger_data': logger_data})



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def bank_statement_pdf(request, account_number):
    logger_data = get_object_or_404(customer_register_table, account_number=account_number)
    user_bankstatment = bank_statment_table.objects.filter(account_number=account_number)  # Adjust model name if different
    
    context = {
        'logger_data': logger_data,
        'user_bankstatment': user_bankstatment,
    }
    
    # Generate the PDF using the template
    pdf = render_to_pdf('bank_statement_template.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"BankStatement_{account_number}.pdf"
        content = f"inline; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generating PDF")



        
        
        
        
    
    
    
        
        
        
    

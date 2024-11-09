from django.urls import path 

from . import views 

urlpatterns=[
    path('',views.index,name='index'),
    path('create_new_account',views.create_new_account,name='create_new_account'),
    path('customer_login',views.customer_login,name='customer_login'),
    path('dashboard/<str:account_number>',views.dashboard,name='dashboard'),
    path('my_accounts/<str:account_number>',views.my_accounts,name='my_accounts'),
    path('deposit/<str:account_number>',views.deposit,name='deposit'),
    path('withdraw/<str:account_number>',views.withdraw,name='withdraw'),
    path('bank_statment/<str:account_number>',views.bank_statment,name='bank_statment'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('new_account_form_submission',views.new_account_form_submission,name='new_account_form_submission'),
    path('customer_login_form_submission',views.customer_login_form_submission,name='customer_login_form_submission'),
    path('deposit_form_submission/<str:account_number>',views.deposit_form_submission,name='deposit_form_submission'),
    path('withdraw_form_submission/<str:account_number>',views.withdraw_form_submission,name='withdraw_form_submission'),
    path('bank_statement_pdf/<str:account_number>/', views.bank_statement_pdf, name='bank_statement_pdf'),
    
]
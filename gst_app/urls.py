"""gst_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gst_app import views



urlpatterns = [
    path("",views.index,name='index'),
    path("form_view/",views.form_view,name='form_view'),
    path("order/",views.order,name='order'),
    path("admin_panel/",views.admin_panel,name='admin_panel'),
    path("admin_panel_upaid/",views.admin_panel_upaid,name='admin_panel_upaid'),
    path("change_order_status/<int:pk>/<str:status>",views.change_order_status,name='change_order_status'),
    path("order_page/<str:id>/",views.order_page,name='order_page'),
    path("logout_view/",views.logout_view,name='logout_view'),
    path("profile/",views.profile,name='profile'),
    path("users_database/",views.users_database,name='users_database'),
    path("handlerequest/<str:id>/<str:user_id>/",views.handlerequest,name='handlerequest'), 
    path("upload_docments/<str:id>/",views.upload_docments,name='upload_docments'),
    path('generateinvoice/<int:pk>/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),
    path('invoice/<int:id>/', views.invoice, name = 'invoice'),
    path("all_states/",views.all_states,name='states'),
    path("delete_states/<int:id>/",views.delete_states,name='delete_states'),
    path("delete_blogs/<int:id>/",views.delete_blogs,name='delete_blogs'),
    path('csv',views.getfile),
    path("blogs/",views.blogs,name='blogs'),
    path("create_blogs/",views.create_blogs,name='create_blogs'),
    path("order_information/<str:id>",views.order_information,name='order_information'),
    path("about/",views.about,name='about'),
    path("contact/",views.contact,name='contact'),
    path("faq/",views.faq,name='faq'),
    path("terms/",views.terms,name='terms'),
    path("policy/",views.policy,name='policy'),

    path("states/Maharashtra/",views.Maharashtra,name='Maharashtra'),
    path("states/Delhi/",views.Delhi,name='Delhi'),
    path("states/Karnataka/",views.Karnataka,name='Karnataka'),
    path("states/Telangana/",views.Telangana,name='Telangana'),
    path("states/Gujarat/",views.Gujarat,name='Gujarat'),
    path("states/Punjab/",views.Punjab,name='Punjab'),
]

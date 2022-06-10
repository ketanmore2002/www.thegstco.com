# import email
# from email.mime import image
# from venv import create
from django.db import models

from gdstorage.storage import GoogleDriveStorage

from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission

permission =  GoogleDriveFilePermission(
   GoogleDrivePermissionRole.READER,
   GoogleDrivePermissionType.USER,
   "info@thegstco.com",
)

gd_storage = GoogleDriveStorage(permissions=(permission, ))

gd_storage = GoogleDriveStorage()

# Create your models here.

class orders(models.Model):

    documents_id = models.CharField(max_length=300,null=True)
    user_name = models.CharField(max_length=300,null=True)
    user_id = models.CharField(max_length=300,null=True)
    full_name = models.CharField(max_length=300,null=True)
    email = models.CharField(max_length=300,null=True)
    company_name = models.CharField(max_length=300,null=True)
    company_type = models.CharField(max_length=300,null=True)
    gst_number = models.CharField(max_length=300,null=True)
    company_addess = models.CharField(max_length=3000,null=True)
    p_number = models.CharField(max_length=300,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=300,null=True)
    total_states = models.CharField(max_length=300,null=True)
    total_amount = models.IntegerField(null=True)
    payment = models.CharField(max_length=300,null=True,default="Unpaid")
    pan_card = models.FileField(upload_to ='pan_card/%Y/%m/%D/',null=True,blank=True,storage=gd_storage)
    proof_of_address = models.FileField(upload_to ='proof_of_address/%Y/%m/%D/',null=True,blank=True,storage=gd_storage)
    photograph = models.ImageField(upload_to ='photograph/%Y/%m/%D/',null=True,blank=True,storage=gd_storage)
    aadhar_card = models.FileField(upload_to ='aadhar_card/%Y/%m/%D/',null=True,blank=True,storage=gd_storage)
    order_status = models.CharField(max_length=30,default="Order Recieved",null=True)
    date = models.DateField(auto_now_add=True,null=True)

    pan_card1 = models.FileField(upload_to ='pan_card/%Y/%m/%D/',null=True,blank=True, storage=gd_storage)
    

    def __str__(self):

            return self.full_name+ " - " + self.company_name+ " - " + self.state


# class documents(models.Model):

#     orders_id = models.CharField(max_length=300,null=True)
#     pan_card = models.FileField(upload_to ='pan_card/%Y/%m/%D/',null=True,blank=True,storage=gd_storage)
#     proof_of_address = models.FileField(upload_to ='proof_of_address/%Y/%m/%D/',null=True,blank=True,storage=gd_storage)
#     photograph = models.ImageField(upload_to ='photograph/%Y/%m/%D/',null=True,blank=True,storage=gd_storage)
#     aadhar_card = models.FileField(upload_to ='aadhar_card/%Y/%m/%D/',null=True,blank=True,storage=gd_storage)
   
#     def __str__(self):

#         return self.orders_id



class phone_numbers(models.Model):

    user_name = models.CharField(max_length=30,null=True)
    phone_number = models.CharField(max_length=30,null=True)

    def __str__(self):

        return self.user_name+ " - " + self.phone_number



class states(models.Model):
    state_name = models.CharField(max_length=300,null=True)
    state_id = models.CharField(max_length=300,null=True)

    def __str__(self):

        return self.state_name


class price(models.Model):

    state_price = models.CharField(max_length=300,null=True)

    price_with_percentage = models.CharField(max_length=300,null=True)


   



class blog(models.Model):

    heading1 = models.CharField(max_length=300,null=True)

    description = models.CharField(max_length=300000,null=True)

    image = models.FileField(upload_to ='blog_image/%Y/%m/%D/',null=True,blank=True, storage=gd_storage) 

    def __str__(self):

        return self.heading1







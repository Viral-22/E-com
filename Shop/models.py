from django.db import models

# Create your models here.
class Book(models.Model):
    book_id=models.AutoField
    book_name=models.CharField(max_length=100)
    category = models.CharField(max_length=50,default="")
    sub_category=models.CharField(max_length=50,default="")
    price=models.IntegerField(default="0")
    desc=models.CharField(max_length=300)
    publication_date=models.DateField()
    image=models.ImageField(upload_to="Shop/images", default="")

    def __str__(self):
        return self.book_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.IntegerField(default="0")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=55)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=25)
    zip_code = models.CharField(max_length=20)
    phone=models.CharField(max_length=10,default="")


class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)

def __str__(self):
    return self.update_desc[0:10] + "..."
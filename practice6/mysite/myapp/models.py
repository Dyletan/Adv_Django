from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount}"  
    

    def __str__(self):
        return self.name

class GroupExpense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, blank=True)
    users = models.ManyToManyField(User)
    
    def split_expense(self):
        return self.amount / self.users.count()

    def create_user_shares(self):
        share_amount = self.split_expense()
        for user in self.users.all():
            UserExpenseShare.objects.create(group_expense=self, user=user, share=share_amount)
            
class UserExpenseShare(models.Model):
    group_expense = models.ForeignKey(GroupExpense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 20:08:28 2020

@author: aly
"""

from django.urls import path
from . import views 

urlpatterns = [
            path('login/', views.LoginView),
            path('register/', views.RegisterView),
            path('forgotpassword/', views.ForgotPasswordView),
            path('verify/<verification_code>', views.EmailConfirmationView),
            path('getAdminUsers', views.GetAdminUsersView),
            path('getUnvalidatedUsers', views.GetUnvalidatedUsersView),
            path('createSubCategory', views.CreateSubCategoryView),
            path('getSubCategories', views.GetSubCategoriesView),
            path('deleteSubCategory', views.DeleteSubCategoryView),
            #TODO:
            path('createOrder', views.CreateOrderView),
            #TODO:
            path('updateOrder', views.UpdateOrderView),
            path('getOrder', views.GetOrderView),
            #TODO:
            path('getOrdersOfBuyer', views.GetOrdersOfBuyer),
            #TODO:
            path('getOrdersOfSeller', views.GetOrdersOfSeller),
            path('createItem', views.CreateItemView),
            path('updateItem', views.UpdateItemView),
            path('getItem', views.GetItemView),
            
        ]
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
            path('transfertokens/', views.TransferTokens)
        ]
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    hashed_pw = models.CharField(max_length=255)
    admin = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, default="")

class Message(models.Model):
    message = models.CharField(max_length=255)
    messager = models.ForeignKey(User, related_name="sent_message", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_message", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    message = models.ForeignKey(Message, related_name="comment", on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, related_name="sent_comment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

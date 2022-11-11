from dataclasses import fields
import datetime
import imp
from pyexpat import model
import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from student.models import Student
from django.utils.timezone import now


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user



class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ["id", "name", "roll_no", "subject", "marks"]
		ordering = ["-created"]

	def clean(self):
		super().clean()
		import pdb
		pdb.set_trace()
		print(self.cleaned_data)
		student = Student.objects.get(id=self.cleaned_data["id"])
		self.cleaned_data.update({"created_at":student.created_at, "updated_at":student.updated_at})
		return self.cleaned_data



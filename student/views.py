from django.shortcuts import  render, redirect
import student

from student.models import Student
from student.serializers import StudentSerializer
from .forms import NewUserForm, StudentForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
import logging
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

def homepage(request):
    return render(request,'homepage.html')

def index(request):
    if not request.user.is_authenticated:
        return redirect("student:login")
    students = Student.objects.order_by('-created_at')[:5]
    return render(request,'homepage.html', {'students': students})


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("student:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("student:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def student_by_id(request, student_id):
    if not request.user.is_authenticated:
        return redirect("student:login")
    student = Student.objects.get(pk=student_id)
    return render(request, 'student_by_id.html', {'student':student})

def creating_student(request):
    if not request.user.is_authenticated:
        return redirect("student:login")
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student created successfully." )
            return redirect("student:index")
    form = StudentForm()
    return render(request, 'student.html', context={'student_form': form})


def update_view(request, student_id):
    if not request.user.is_authenticated:
        return redirect("student:login")
    obj = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(f"/student/{student_id}")
    context = {"form": form}
    return render(request, "update_view.html", context)


#update and delete student using API request

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_update(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        form_data = JSONParser().parse(request)
        form_serializer = StudentSerializer(student, data=form_data)
        if form_serializer.is_valid():
            form_serializer.save()
            logger.warning("Student %s updated  successfully", student_id)
            return JsonResponse({'message': 'updated  successfully!'})
        else:
            logger.warning("Student %s not updated, invalid data", student_id)
            return JsonResponse({'message': 'not a valid data to update!'})

    except Student.DoesNotExist:
        logger.error("Student %s does not exist", student_id)
        return JsonResponse({'message': 'No Student with that ID exists!'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["POST", "DELETE"])
@permission_classes((AllowAny,))
def api_delete(request, student_id):
    try:
        Student.objects.get(id=student_id).delete()
        logger.warning("Student %s deleted  successfully", student_id)
        return JsonResponse({'message': 'not a valid data to update!'}, status=status.HTTP_204_NO_CONTENT)

    except Student.DoesNotExist:
        logger.error("Student %s does not exist", student_id)
        return JsonResponse({'message': 'No Student with that ID exists!'}, status=status.HTTP_404_NOT_FOUND)




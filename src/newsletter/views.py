from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import SignUpForm, ContactForm

from .models import SignUp
# Create your views here.

def home(request):
	title = "My title"

	if request.user.is_authenticated():
		title = "My title {}".format(request.user)

	form = SignUpForm(request.POST or None)

	context = {
		"title": title,
		"form": form,
	}

	if form.is_valid():
		# form.save()
		# print(request.POST['email']) not recommended
		instance = form.save(commit=False)

		full_name = form.cleaned_data.get("full_name")
		if not full_name:
			full_name = "Minh"
		instance.full_name = full_name
		instance.save()
		context = {
			"title": "Thank you",
		}

	if request.user.is_authenticated() and request.user.is_staff:
		#print(SignUp.objects.all())
		# i = 1
		# for instance in SignUp.objects.all():
		# 	print(i)
		# 	print(instance.full_name)
		# 	i += 1

		queryset = SignUp.objects.all().order_by('-timestamp') #.filter(full_name__iexact="Justin")
		#print(SignUp.objects.all().order_by('-timestamp').filter(full_name__iexact="Justin").count())
		context = {
			"queryset": queryset
		}

	return render(request, "home.html", context)

def contact(request):
	title = "Contact us"
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key, value in form.cleaned_data.items():
			# print(key, value)
		form_email = form.cleaned_data.get('email')
		form_message = form.cleaned_data.get('message')
		form_full_name = form.cleaned_data.get('full_name')
		subject = "Site contact form"
		contact_message = """
		<!DOCTYPE html>
		<html lang="en">
		<head>
			<meta charset="UTF-8">
			<title>Test</title>
		</head>
		<body>
			{} {} {}

		</body>
		</html>
		""".format(form_full_name, form_message, form_email)
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, "minhpn.org.ec@gmail.com"]
		send_mail(
			subject,
			contact_message, 
			from_email, 
			[to_email], 
			fail_silently=False,
			)
	context = {
		"form": form,
		"title": title,
	}
	return render(request, "forms.html", context)














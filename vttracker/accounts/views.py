from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from accounts.forms import RegistrationForm
import simplejson as json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='accounts/login')
def register(request):

	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		response_data = {}

		if form.is_valid():

			user = form.save(commit=False)
			user.save()

			response_data['status'] = True
			response_data['msg'] = "El Usuario " + user.email + " se creo correctamente."

			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			response_data['status'] = False
			response_data['errors'] = form.errors

			return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		form = RegistrationForm()
		args = {'form': form}
	return render(request, 'registration/registerUser.html', args)

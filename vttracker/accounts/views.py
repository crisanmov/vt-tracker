from django.shortcuts import render
from accounts.forms import RegistrationForm

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			return redirect('/accounts/regiter')
	else:
		form = RegistrationForm()
		args = {'form': form}
	return render(request, 'registration/registerUser.html', args)

from django.shortcuts import render, redirect

from .models import (
    Skill,
    Project,
    Profile,
    Experience,
    Education
)

from .forms import ContactForm

def home(request):

    skills = Skill.objects.all()

    projects = Project.objects.all()

    profile = Profile.objects.first()

    experiences = Experience.objects.all().order_by('-start_date')

    education = Education.objects.all().order_by('-end_year')

    if request.method == 'POST':

        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():

            contact_form.save()

            return redirect('home')

    else:

        contact_form = ContactForm()

    context = {

        'profile': profile,

        'skills': skills,

        'projects': projects,

        'experiences': experiences,

        'education': education,

        'contact_form': contact_form,
    }

    return render(
        request,
        'home.html',
        context
    )

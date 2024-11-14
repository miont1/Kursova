from django.shortcuts import render
from .models import Profile

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    contex = {'profiles': profiles}
    return render(request, 'users/profiles.html', contex)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    adv_descr = profile.advantage_set.exclude(description__exact="").exclude(description__isnull=True)
    adv = profile.advantage_set.filter(description__exact="").union(profile.advantage_set.filter(description__isnull=True))

    contex = {'profile': profile, 'adv_descr': adv_descr,
              'adv': adv}
    return render(request, 'users/profile.html', contex)

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ProfileForm
from main.models import Profile
from main.models import Movie

# Create your views here.
class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:profile_list')
        return render(request, 'index.html')
    
@method_decorator(login_required, name='dispatch')
class ProfileList(View):
    def get(self, request,*args, **kwargs):
        profiles=request.user.profiles.all()
        return render(request, 'profileList.html', {
            'profiles':profiles
        })

@method_decorator(login_required, name='dispatch')
class ProfileCreate(View):
    def get(self, request, *args, **kwargs):
        form=ProfileForm()
        return render(request, 'ProfileCreate.html',{
            'form':form
        })
    
    def post(self, request, *args, **kwargs):
        form=ProfileForm(request.POST or None)
        
        if form.is_valid():
            #print(form.cleaned_data)
            profile = Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect('main:profile_list')
            
        return render(request, 'profileCreate.html',{
            'form':form
        })

@method_decorator(login_required, name='dispatch')
class Watch(View):
    def get(self, request, profile_id, *args, **kwargs):
        try:
            profile = Profile.objects.get(uuid=profile_id)
            movies = Movie.objects.filter(age_limit=profile.age_limit)
            
            if profile not in request.user.profiles.all():
                return redirect(to='main:profile_list')
            
            return render(request, 'movieList.html',{
                'movies':movies
            })
        except Profile.DoesNotExist:
            return redirect(to='main:profile_list')


@method_decorator(login_required, name='dispatch')
class ShowMovieDetail(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            
            return render(request, 'movieDetail.html',{
                'movie':movie
            })
        except Movie.DoesNotExist:
            return redirect('main:profile_list')

@method_decorator(login_required, name='dispatch')
class ShowMovie(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            movie = movie.videos.values()
            
            return render(request, 'showMovie.html',{
                'movie':list(movie)
            })
            
        except Movie.DoesNotExist:
            return redirect('main:profile_list')
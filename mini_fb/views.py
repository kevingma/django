# mini_fb/views.py

from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class ShowAllProfilesView(ListView):
    """Shows all profiles"""
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)
        else:
            return get_object_or_404(Profile, user=self.request.user)


class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get(self, request, *args, **kwargs):
        profile_form = self.form_class()
        user_form = UserCreationForm()
        return render(request, self.template_name, {
            'profile_form': profile_form,
            'user_form': user_form,
        })

    def post(self, request, *args, **kwargs):
        profile_form = self.form_class(request.POST)
        user_form = UserCreationForm(request.POST)

        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('show_own_profile')
        else:
            return render(request, self.template_name, {
                'profile_form': profile_form,
                'user_form': user_form,
            })


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile
        response = super().form_valid(form)

        images = self.request.FILES.getlist('images')
        for image in images:
            img = Image(image_file=image, status_message=self.object)
            img.save()

        return response

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def dispatch(self, request, *args, **kwargs):
        status_message = self.get_object()
        if status_message.profile.user != request.user:
            messages.error(request, "You are not authorized to delete this status message.")
            return redirect('show_profile', pk=status_message.profile.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('show_own_profile')


class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        other_pk = self.kwargs.get('other_pk')
        profile = get_object_or_404(Profile, user=request.user)
        other_profile = get_object_or_404(Profile, pk=other_pk)

        try:
            profile.add_friend(other_profile)
            messages.success(request, f"You are now friends with {other_profile.first_name} {other_profile.last_name}.")
        except Exception as e:
            messages.error(request, str(e))

        return redirect('show_profile', pk=other_profile.pk)


class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = context['profile'].get_friend_suggestions()
        return context


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = context['profile'].get_news_feed()
        return context

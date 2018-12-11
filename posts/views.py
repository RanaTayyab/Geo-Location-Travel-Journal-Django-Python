from django.db.models.signals import pre_delete
from django.dispatch import receiver
import cloudinary

from django import forms
from django.http import HttpResponse

from cloudinary.forms import cl_init_js_callbacks


from braces.views import SelectRelatedMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models

User = get_user_model()
# Create your views here.


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', 'group')


class UserPost(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(
                username__iexact=self.kwargs.get('username')
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('message', 'group', 'profile_pic')
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        user = self.object.save()
        profile = form.save(commit=False)
        print(profile)
            # Set One to One relationship between
            # UserForm and UserProfileInfoForm

        #print(self.request.FILES)
            # Check if they provided a profile picture
        #if 'profile_pic' in self.request.FILES:
                # If yes, then grab it from the POST form reply
            #profile.profile_pic = self.request.FILES['profile_pic']
            # Now save model
        profile.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

    @receiver(pre_delete, sender=model)
    def photo_delete(sender, instance, **kwargs):
        cloudinary.uploader.destroy(instance.profile_pic.public_id)

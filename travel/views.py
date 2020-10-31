from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Comment, DataTracking
from django import forms
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from textblob import TextBlob
from django.template.defaultfilters import stringfilter
from ip2geotools.databases.noncommercial import DbIpCity
from django.db.models import F
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 4
def PostDetails(request, slug):
    template_name = 'post.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})
def VirtualTour(request, slug):
    posts = get_object_or_404(Post, slug=slug)
    Post.objects.filter(title=posts.title).update(viewcount=F('viewcount')+1)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
        country = DbIpCity.get(ip, api_key='free')
        country = country.country
    else:
        ip = request.META.get('REMOTE_ADDR')
        country="IN"
    if DataTracking.objects.filter(Q(blogtitle=posts.title) & Q(country=country)).count()>=1:
        DataTracking.objects.filter(Q(blogtitle=posts.title) & Q(country=country)).update(viewcount=F('viewcount')+1)
    else:
        DataTracking.objects.create(blogtitle=posts.title,country=country,viewcount=1)
    return render(request, 'virtual.html', {'posts':posts})
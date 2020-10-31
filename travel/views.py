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
def about(request):
    return render(request, 'about.html')
def policy(request):
    return render(request, 'policy.html')
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
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
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
def searchquery(request):
    template_name='searchresults.html'
    searchqueries=request.GET.get('q')
    results=Post.objects.filter(Q(status=1) & Q(Q(Q(title__istartswith=searchqueries) | Q(Q(title__icontains=' '+searchqueries) | Q(title__icontains=','+searchqueries))) | Q(Q(content__istartswith=searchqueries) | Q(Q(content__icontains=' '+searchqueries) | Q(Q(content__icontains=','+searchqueries) | Q(Q(content__icontains='.'+searchqueries) | Q(Q(content__icontains='<br>'+searchqueries) | Q(content__icontains='<p>'+searchqueries))))))))
    if request.GET.get('t'):
        tag=request.GET.get('t')
        results=Post.objects.filter(Q(Q(status=1) & Q(tag_let_one=tag)) & Q(Q(Q(title__istartswith=searchqueries) | Q(Q(title__icontains=' '+searchqueries) | Q(title__icontains=','+searchqueries))) | Q(Q(content__istartswith=searchqueries) | Q(Q(content__icontains=' '+searchqueries) | Q(Q(content__icontains=','+searchqueries) | Q(Q(content__icontains='.'+searchqueries) | Q(Q(content__icontains='<br>'+searchqueries) | Q(content__icontains='<p>'+searchqueries))))))))
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    if not results:
        bszahid = TextBlob(str(searchqueries))
        aszahid=str(bszahid.correct())
        if aszahid!=searchqueries:
            taszahid=aszahid.replace(" ","+")
            return render(request, template_name, {'post_list':pages,'searched':searchqueries,"aszahid":aszahid,"taszahid":taszahid})
        else:return render(request, template_name, {'post_list':pages,'searched':searchqueries,"notfound":"notfound"})
    if request.GET.get('t'):
        return render(request, template_name, {'post_list':pages,'searched':searchqueries,'tag':tag})
    return render(request, template_name, {'post_list':pages,'searched':searchqueries})
def autocomplete(request):
    template_name='searchresults.html'
    if 'term' in request.GET:
        term = request.GET.get('term')
        qs=Post.objects.filter(Q(status=1) & Q(Q(title__istartswith=request.GET.get('term')) | Q(Q(title__icontains=' '+request.GET.get('term')) | Q(title__icontains=','+request.GET.get('term')))))
        titles=list()
        for post in qs:
            titles.append(post.title)
        return JsonResponse(titles, safe=False)
    return render(request, template_name)
def MostPopular(request):
    queryset = Post.objects.filter(status=1).order_by('-viewcount')
    if request.GET.get('c'):
        datsza=DataTracking.objects.filter(country=request.GET.get('c')).values_list('blogtitle').order_by('-viewcount')
        lt = datsza
        out = [item for t in lt for item in t]
        datsza = out
        queryset = Post.objects.filter(Q(status=1) & Q(title__in=datsza)).order_by('-viewcount')
    countrylist=DataTracking.objects.values_list('country', flat=True).distinct()
    template_name = 'popular.html'
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return render(request, template_name, {'post_list':pages,'countrylist':countrylist})

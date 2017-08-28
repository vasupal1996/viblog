from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse

from post.models import Post, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search_query(request):
    if request.method == 'GET':
        try:
            if 'q' in request.GET:
                query_string= request.GET.get('q')

                if len(query_string) == 0:
                    return HttpResponseBadRequest('Invalid Search')
                else:
                    query_list = query_string.split(' ')
                    posts = _search(query_list)
                    paginator = Paginator(posts, 1) 
                    page = request.GET.get('page')
                    if page is None:
                        page = 1
                    else:
                        pass
                    try:
                        posts = paginator.page(page)
                    
                    except PageNotAnInteger:
                        
                        posts = paginator.page(1)
                        return HttpResponseBadRequest()
                    except EmptyPage:
                        
                        posts = paginator.page(paginator.num_pages)
                    
                        return HttpResponseBadRequest()
                    
                    context = {
                        'posts': posts,
                    }
                    return render(request, 'search/search.html', {'posts': posts,})
        except:
            return HttpResponseBadRequest('Outside Try')

def _search(query_list):
    result = []
    for query in query_list:
        query = query.lower()
    try:        
        posts = Post.objects.order_by('-date_created').filter(
            Q(tag__tag__icontains=query) |
            Q(title__icontains=query) |
            Q(content__icontains=query) 
        )
        for post in posts:
            if post in result:
                pass
            else:
                result.append(post)
    except:
        result = None
    return result
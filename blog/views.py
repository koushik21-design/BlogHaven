from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from blog.models import Blog, Category, Comment, Like,Dislike
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.db.models import Q

# Create your views here.
def posts_by_category(request,category_id):
    posts=Blog.objects.filter(status='Published',category=category_id)
    try:
        category=Category.objects.get(pk=category_id)
    except:
        return redirect('home')
    #category=get_object_or_404(Category,pk=category_id)
    context={
        'posts':posts,
        'category':category,
        
    }
    return render(request,'posts_by_category.html',context)

@login_required
def blogs(request,slug):
    single_blog=get_object_or_404(Blog,slug=slug,status='Published')
    if request.method=='POST':
        comment=Comment()
        comment.user=request.user
        comment.blog=single_blog
        comment.comment=request.POST['comment']
        comment.save()
        if Like.objects.filter(blog=single_blog, user=request.user).exists():
            Like.objects.filter(blog=single_blog, user=request.user).delete()
        else:
            Like.objects.create(blog=single_blog, user=request.user)
            Dislike.objects.filter(blog=single_blog, user=request.user).delete()
        return HttpResponseRedirect(request.path_info)
    
    comments=Comment.objects.filter(blog=single_blog)
    comment_count=comments.count()
    likes_count=single_blog.likes.count()
    dislikes_count=single_blog.dislikes.count()
    context={
        'single_blog':single_blog,
        'comments':comments,
        'comment_count':comment_count,
        'likes_count':likes_count,
        'dislikes_count':dislikes_count,
    }
    return render(request,'blogs.html',context)

@login_required
def like_post(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    user = request.user

    if Like.objects.filter(blog=single_blog, user=user).exists():
        Like.objects.filter(blog=single_blog, user=user).delete()
    else:
        Like.objects.create(blog=single_blog, user=user)
        Dislike.objects.filter(blog=single_blog, user=user).delete()

    return redirect('blogs', slug=slug)

@login_required
def dislike_post(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    user = request.user

    if Dislike.objects.filter(blog=single_blog, user=user).exists():
        Dislike.objects.filter(blog=single_blog, user=user).delete()
    else:
        Dislike.objects.create(blog=single_blog, user=user)
        Like.objects.filter(blog=single_blog, user=user).delete()

    return redirect('blogs', slug=slug)



def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.none()

    if keyword:
        blogs = Blog.objects.filter(
            Q(title__icontains=keyword) | Q(blog_body__icontains=keyword),
            status='Published'
        ).order_by('-created_at')

    paginator = Paginator(blogs, 10)  # 10 results per page
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    context = {
        'blogs': blogs,
        'keyword': keyword
    }
    return render(request, 'search.html', context)


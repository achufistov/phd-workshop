from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile, Post, Comment
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.views.static import serve
import os
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'vulnapp/login.html', {'form': {'errors': True}})
    
    return render(request, 'vulnapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        posts = Post.objects.all()[:5]
        return render(request, 'vulnapp/home.html', {
            'profile': profile,
            'posts': posts
        })
    except UserProfile.DoesNotExist:
        return render(request, 'vulnapp/home.html', {'profile': None})

@login_required
def search(request):
    query = request.GET.get('q', '')
    debug_file = request.GET.get('debug', '')  # Hidden parameter for path traversal
    
    if debug_file:
        try:
            # Vulnerable code - no path verification
            with open(debug_file, 'r') as f:
                content = f.read()
            return HttpResponse(content)
        except:
            return HttpResponse("Error reading file", status=500)
    
    # Intentionally vulnerable to xss - using mark_safe with user input
    safe_query = mark_safe(f"""
        <div class="search-results">
            <h3>Результаты поиска для: {query}</h3>
            <p>Найдено результатов: 0</p>
        </div>
    """)
    return render(request, 'vulnapp/search.html', {'query': safe_query})

# Intentionally vulnerable to IDOR - no authentication check
def user_profile(request, user_id):
    try:
        profile = UserProfile.objects.get(id=user_id)
        return render(request, 'vulnapp/profile.html', {'profile': profile})
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

@login_required
def post_list(request):
    category = request.GET.get('category', '')
    if category:
        posts = Post.objects.filter(category=category)
    else:
        posts = Post.objects.all()
    return render(request, 'vulnapp/post_list.html', {
        'posts': posts,
        'categories': Post.CATEGORY_CHOICES
    })

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent=None) 
    return render(request, 'vulnapp/post_detail.html', {
        'post': post,
        'comments': comments
    })

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content', '')
        parent_id = request.POST.get('parent_id')
        
        # Intentionally vulnerable to XSS - using mark_safe with user input
        safe_content = mark_safe(content)
        
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=safe_content,
            parent_id=parent_id if parent_id else None
        )
        
        return redirect('post_detail', post_id=post_id)
    return redirect('home')

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        
        post = Post.objects.create(
            title=title,
            content=content,
            category=category,
            author=request.user
        )
        
        return redirect('post_detail', post_id=post.id)
    
    return render(request, 'vulnapp/create_post.html', {
        'categories': Post.CATEGORY_CHOICES
    })

def directory_listing(request, path):
    base_dir = os.path.join(settings.STATICFILES_DIRS[0], path)
    
    if path == '' or path == '/':
        return HttpResponse("Access Forbidden", status=403)
    
    if not os.path.exists(base_dir):
        return HttpResponse("Directory not found", status=404)
    
    if not os.path.isdir(base_dir):
        return serve(request, path, document_root=settings.STATICFILES_DIRS[0])
    
    response = HttpResponse(status=301)
    response['Location'] = f'/static/{path}/'
    return response

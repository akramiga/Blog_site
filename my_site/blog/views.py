from django.shortcuts import render, get_object_or_404
from.models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.
def post_list(request):
    post_list= Post.published.all()
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page',1)
    try: posts = paginator.page(page_number)
    # If page_number is out of range get last page of results 
    except EmptyPage: posts = paginator.page(paginator.num_pages)
    # If page_number is not an integer get the first page
    except PageNotAnInteger: posts = paginator.page(1)
    return render(request, 'blog/post/list.html', {'posts': posts} )

def post_detail(request, year,month,day,post): 
    
    # try: post = Post.published.get(id=id) 
    # except Post.DoesNotExist: raise Http404("No Post found.") 
    post = get_object_or_404( Post, status=Post.Status.PUBLISHED, 
        slug=post, publish__year=year,publish__month=month, publish__day=day
     )
    return render( request,'blog/post/detail.html', {'post': post} )


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name= 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # we are retrieving a post by its id
    post = get_object_or_404(Post, id=post_id, status= Post.Status.PUBLISHED) 
    sent = False
    if request.method == 'POST': # Form was submitted 
        form = EmailPostForm(request.POST)   
        if form.is_valid(): # Form fields passed validation 
            cd = form.cleaned_data # ... send email 
            post_url = request.build_absolute_uri( post.get_absolute_url() ) 
            subject = (f"{cd['name']} ({cd['email']}) " f"recommends you read {post.title}") 
            message = (f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}") 
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cd['to']] ) 
            sent = True   
    else: form = EmailPostForm()
    return render( request, 'blog/post/share.html', { 'post': post,'form': form, 'sent': sent } )
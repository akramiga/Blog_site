from django.shortcuts import render, get_object_or_404
from.models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from taggit.models import Tag
# Create your views here.
def post_list(request, tag_slug=None):
    post_list= Post.published.all()
    tag = None
    if tag_slug: 
        tag = get_object_or_404(Tag, slug=tag_slug) 
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page',1)
    try: posts = paginator.page(page_number)
    # If page_number is out of range get last page of results 
    except EmptyPage: posts = paginator.page(paginator.num_pages)
    # If page_number is not an integer get the first page
    except PageNotAnInteger: posts = paginator.page(1)
    return render(
        request, 
        'blog/post/list.html', 
        {'posts': posts, 'tag': tag} 
    )

def post_detail(request, year,month,day,post): 
    
    # try: post = Post.published.get(id=id) 
    # except Post.DoesNotExist: raise Http404("No Post found.") 
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED, 
        slug=post, publish__year=year,
        publish__month=month, 
        publish__day=day
    )
    # retrieve all active comments for the post
    comments = post.comments.filter(active=True) 
    # Form for users to comment 
    form = CommentForm()
    return render(
        request,
        'blog/post/detail.html', 
        {'post': post, 'comments': comments, 'form': form })


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name= 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # we are retrieving a post by its id
    post = get_object_or_404(
        Post, 
        id=post_id, 
        status= Post.Status.PUBLISHED
    ) 
    sent = False
    if request.method == 'POST': # Form was submitted 
        form = EmailPostForm(request.POST)   
        if form.is_valid(): # Form fields passed validation 
            cd = form.cleaned_data # ... send email 
            post_url = request.build_absolute_uri( post.get_absolute_url() ) 
            subject = (
                f"{cd['name']} ({cd['email']}) " 
                f"recommends you read {post.title}"
            ) 
            message = (
                f"Read {post.title} at {post_url}\n\n" 
                f"{cd['name']}\'s comments: {cd['comments']}"
            ) 
            send_mail(
                subject=subject, 
                message=message, 
                from_email=None, 
                recipient_list=[cd['to']] 
            ) 
            sent = True   
    else: form = EmailPostForm()
    return render( 
        request, 
        'blog/post/share.html', 
        { 'post': post,'form': form, 'sent': sent } 
    )


@require_POST 
def post_comment(request, post_id): 
    #retrieve a published post
    post = get_object_or_404(
        Post, 
        id=post_id, 
        status=Post.Status.PUBLISHED
    ) 
    comment = None #variable to store the comment object when it is created.
    # A comment was posted 
    form = CommentForm(data=request.POST) 
    if form.is_valid(): 
        # Create a Comment object without saving it to the database 
        comment = form.save(commit=False)
        # Assign the post to the comment created
        comment.post = post 
        # Save the comment to the database
        comment.save() 
    return render(
        request, 
        'blog/post/comment.html',
        {'post': post, 'form': form, 'comment': comment } 
    )
# from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


@require_POST
def post_comment(request, post_id):
  post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
  comment = None
  form = CommentForm(data=request.POST)
  if form.is_valid():
    comment = form.save(commit=False)
    comment.post = post
    comment.save()

  return render(request, 'blog/post/comment.html', {
    'post': post,
    'form': form,
    'comment': comment,
  })


def post_share(request, post_id):
  post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

  sent = False

  if request.method == 'POST':
    form = EmailPostForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      post_url = request.build_absolute_uri(post.get_absolute_url())
      subject = f"{cd['name']} recommends you red "\
                f"{post.title}"
      message = f"Read {post.title} at {post_url}\n\n"\
                f"{cd['name']}\'s comments: {cd['comment']}"
      send_mail(subject, message, 'vlad.rosi.92@gmail.com', [cd['to']])
      sent = True
  else:
    form = EmailPostForm()

  return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


class PostListView(ListView):
  # model = Post
  queryset = Post.published.all()
  context_object_name = 'posts'
  paginate_by = 3
  template_name = 'blog/post/list.html'


def post_list(request):
  post_list = Post.published.all()
  pagination = Paginator(post_list, 3)
  page_number = request.GET.get('page', 1)
  try:
    posts = pagination.page(page_number)
  except EmptyPage:
    posts = pagination.page(pagination.num_pages)
  except PageNotAnInteger:
    posts = pagination.page(1)

  return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):

  post = get_object_or_404(Post,\
                          status=Post.Status.PUBLISHED,\
                          slug=post,\
                          publish__year=year,\
                          publish__month=month,\
                          publish__day=day)

  comments = post.comments.filter(active=True)
  form = CommentForm()

  return render(request, 'blog/post/detail.html', {
    'post': post,
    'comments': comments,
    'form': form,
  })


# def post_detail(request, id):
# post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
# try:
#   post = Post.published.get(id=id)
# except:
#   raise Http404('No Post found.')

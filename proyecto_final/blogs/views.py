from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.files.storage import default_storage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blogs, Post
from .forms import BlogForm, PostForm, SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from blogs.models import Blog_img

def about_us(request):
    return render(request, 'blogs/about_us.html')

def show_default_image_url(request):
    blog_img = Blog_img()
    default_image_url = blog_img.image.url
    return HttpResponse(f"URL de la imagen predeterminada: {default_image_url}")
# Vistas para Blogs
class BlogListView(ListView):
    model = Blogs
    template_name = 'blogs/home.html'
    context_object_name = 'blogs'

class BlogDetailView(DetailView):
    model = Blogs
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blog'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(blog=self.object).order_by('-created_at')
        paginator = Paginator(posts, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Blogs
    form_class = BlogForm
    template_name = 'blogs/blog_create.html'
    success_url = reverse_lazy('Home')
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        response = super().form_valid(form)

        blog = self.object

        if 'thumbnail' in self.request.FILES:
            Blog_img.objects.create(blog=blog, image=self.request.FILES['thumbnail'])
        else:
            if not hasattr(blog, 'thumbnail'):
                Blog_img.objects.create(blog=blog)
        
        return response

    def form_invalid(self, form):
        # Manejo en caso de error en el formulario
        return self.render_to_response(self.get_context_data(form=form))

class BlogUpdateView(LoginRequiredMixin,UpdateView):
    model = Blogs
    form_class = BlogForm
    template_name = 'blogs/blog_update.html'
    success_url = reverse_lazy('Home')
    
    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()

        if blog.author != request.user and not request.user.is_superuser:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        response = super().form_valid(form)
        blog = self.get_object()

        if 'thumbnail' in self.request.FILES:
            if blog.thumbnail and blog.thumbnail.image and blog.thumbnail.image.name != 'blogs_imgs/default_blog_img.jpg':
                old_image = blog.thumbnail.image
                if default_storage.exists(old_image.name):
                    default_storage.delete(old_image.name)

            blog.thumbnail.image = self.request.FILES['thumbnail']
            blog.thumbnail.save()
        
        return response
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blogs
    template_name = 'blogs/blog_delete.html'
    success_url = reverse_lazy('Home')

    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()

        if blog.author != request.user and not request.user.is_superuser:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = self.get_object()
        return context
    def form_valid(self, form):
        blog = self.get_object()

        # Lógica personalizada para eliminar la imagen
        if hasattr(blog, 'thumbnail') and blog.thumbnail.image and blog.thumbnail.image.name != 'blogs_imgs/default_blog_img.jpg':
            old_image = blog.thumbnail.image
            if default_storage.exists(old_image.name):
                default_storage.delete(old_image.name)

        # Llama al método padre para eliminar el objeto
        return super().form_valid(form)
class UserBlogsListView(LoginRequiredMixin, ListView):
    model = Blogs
    template_name = 'blogs/user_blogs_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return Blogs.objects.filter(author=self.request.user)


# Vistas para Posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogs/post_form.html'

    def form_valid(self, form):
        blog = get_object_or_404(Blogs, pk=self.kwargs['pk'])
        form.instance.blog = blog
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.kwargs['pk']})

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blogs/post_form.html'
    success_url = reverse_lazy('post_list')
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        if post.author != request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.blog.pk})
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blogs/post_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.blog.pk})

def search(request):
    form = SearchForm(request.GET or None)
    blogs = []
    posts = []
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            # Filtrar blogs por título, keywords y descripción
            blogs = Blogs.objects.filter(
                Q(title__icontains=query) |
                Q(keywords__icontains=query) |
                Q(description__icontains=query)
            )
            # Filtrar posts por contenido
            posts = Post.objects.filter(content__icontains=query)

    return render(request, 'blogs/search_results.html', {
        'form': form,
        'blogs': blogs,
        'posts': posts,
    })
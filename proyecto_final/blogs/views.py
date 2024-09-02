from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.files.storage import default_storage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blogs, Post
from .forms import BlogForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
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



# Vistas para Posts
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('post_list')

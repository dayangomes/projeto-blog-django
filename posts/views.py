from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from posts.models import Post
from django.db.models import Count, Q, Case, When # Importa os filtros para o queryset.
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages

class PostIndex(ListView):
    model = Post # Muda o model padrão para o model Post.
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts' # Muda o nome padrão do objeto para 'posts'.
    # ordering = ['-data_post'] # Ordena os posts por data_post.

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('categoria_post') # O select_related faz 
        qs = qs.order_by('-id').filter(publicado_post=True)
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1)
                )
            )
        )

        return qs
        # return Post.objects.filter(publicado_post=True).order_by('-data_post')

class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'
    
    def get_queryset(self):
        qs = super().get_queryset()

        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            # O iexact é usado pois 
            Q(titulo_post__icontains=termo)
            | Q(autor_post__first_name__iexact=termo)
            | Q(conteudo_post__icontains=termo)
            | Q(excerto_post__icontains=termo)
            | Q(categoria_post__nome_cat__iexact=termo)
        ) 

        return qs

class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()

        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs
     
        # Filtra os posts por categoria, com case insensitive.
        qs = qs.filter(categoria_post__nome_cat__iexact=categoria) 


        return qs

class PostDetalhes(UpdateView):
    model = Post
    template_name = 'posts/post_detalhes.html'
    form_class = FormComentario
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentario.objects.filter(
            publicado_comentario=True,
            post_comentario=post, 
        )
        contexto['comentarios'] = comentarios # Adiciona os comentarios no contexto.
        

        return contexto
    
    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)
        comentario.post_comentario = post

        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user

        comentario.save()
        messages.success(self.request, 'Comentário enviado com sucesso!')
        return redirect('post_detalhes', pk=post.id)
    

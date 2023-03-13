from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from posts.models import Post
from django.db.models import Count, Q, Case, When # Importa os filtros para o queryset.

class PostIndex(ListView):
    model = Post # Muda o model padrão para o model Post.
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts' # Muda o nome padrão do objeto para 'posts'.
    # ordering = ['-data_post'] # Ordena os posts por data_post.

    def get_queryset(self):
        qs = super().get_queryset()
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
    pass

class PostCategoria(PostIndex):
    pass

class PostDetalhes(UpdateView):
    pass

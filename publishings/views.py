from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from publishings.forms import ClientForm
from publishings.models import Profile, Subscription


class BaseView(TemplateView):
    template_name = 'publishings/category_list.html'
    extra_context = {
        'title': 'Главная страница',
        'title_blog': 'Наш блок',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Profile.objects.all()
        return context_data


class CategoryListView(ListView):
    model = Subscription
    template_name = 'publishings/category_list.html'
    extra_context = {
        'title': 'Наши подписчики'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Profile.objects.all()
        return context_data


class ConnectionView(TemplateView):
    template_name = 'publishings/connection_list.html'
    extra_context = {
        'title': 'Обратная связь',
    }

    def get_context_data(self, **kwargs):
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            email = self.request.POST.get('email')
            message = self.request.POST.get('message')
            print(f'You have new message from {name}({email}): {message}')
        return super().get_context_data(**kwargs)


class ClientListView(ListView):
    model = Profile
    template_name = 'publishings/client_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        client_id = self.kwargs.get('pk')
        client_item = Profile.objects.get(id=client_id)

        context['client_pk'] = client_id
        context['title'] = f'Наш клиент {client_item.full_name}'

        return context


class ClientCreateView(CreateView):
    model = Profile
    form_class = ClientForm
    template_name = 'publishings/client_form.html'
    success_url = reverse_lazy('publishings:category_list')
    extra_context = {
        'title': 'Добавить статью',
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Profile
    form_class = ClientForm
    template_name = 'publishings/client_form.html'
    success_url = reverse_lazy('publishings:category_list')
    permission_required = []

    def has_permission(self):
        client = self.get_object()
        if self.request.user == client.user:
            return super().has_permission()


class ClientDeleteView(DeleteView):
    model = Profile
    template_name = 'publishings/client_confirm_delete.html'
    success_url = reverse_lazy('client:message_list')
    permission_required = []

    def has_permission(self):
        email = self.get_object()
        if self.request.user == email.user:
            return super().has_permission()











def about(request):
    return render(request, 'publishings/about.html', {"title": "О сайте"})

def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")

def addpage(request):
    return HttpResponse("Добавление статьи")

def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")



# def categories(request, cat_id):  # HttpRequest
#     return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")
#
# def categories_bu_slug(request, categories_slug):  # HttpRequest
#     if request.POST:
#         print(request.POST)
#     return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {categories_slug}</p>")
#
# def archive(request, year):
#     if year > 2024:
#         uri = reverse("publishings/categories_slug", args=("music", ))
#         return redirect(uri)
#         # return redirect("home")
#         # return redirect("/publishings/", permanent=True)
#         # raise Http404()
#     return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")
#
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

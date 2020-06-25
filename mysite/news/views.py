from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .models import News, Category
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались.')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def test(request):
    objects = ['john', 'paul', 'george', 'ringo', 'john1', 'paul1', 'george1', 'ringo1', 'john2', 'paul2', 'george2',
               'ringo2']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})


def feedback_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'from@mail.ru', ['to@mail.ru'],
                             fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('test')
            else:
                messages.error(request, 'Ошибка отправки')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})


class HomeNews(MyMixin, ListView):
    model = News  # по сути сделали news = News.objects.all()
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    queryset = News.objects.select_related('Category')
    mixin_prop = 'hello world'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


# def index(requests):
#     # print(dir(requests))
#     news = News.objects.all()
#     context = {
#                 'news': news,
#                 'title': 'Список новостей'
#                }
#     return render(requests, template_name='news/index.html', context=context)

class NewsByCategory(MyMixin, ListView):
    model = News  # по сути сделали news = News.objects.all()
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


# def get_category(requests, category_id):
#     news = News.objects.filter(category_id=category_id)
#
#     category = Category.objects.get(pk=category_id)
#     context = {
#                 'news': news,
#                 'category': category,
#                }
#     return render(requests, template_name='news/category.html', context=context)


class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = 'news_id'
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'


# def view_news(requests, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(requests, 'news/view_news.html', {'news_item': news_item})


class CreateNews(LoginRequiredMixin, CreateView):
    login_url = '/admin/'
    form_class = NewsForm
    template_name = 'news/add_news.html'

    # success_url = reverse_lazy('home')
    # context_object_name =

# def add_news(requests):
#     # если не связано с моделькой?
#     # if requests.method=='POST':
#     #     form = NewsForm(requests.POST)
#     #     if form.is_valid():
#     #         # print(form.cleaned_data)
#     #         news=News.objects.create(**form.cleaned_data)
#     #         return redirect(news)
#     # else:
#     #     form = NewsForm()
#     if requests.method == 'POST':
#         form = NewsForm(requests.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(requests, 'news/add_news.html',{'form': form})


# Create your views here.
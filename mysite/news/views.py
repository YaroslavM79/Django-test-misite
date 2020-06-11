from django.db.models import Count
from django.shortcuts import render, get_object_or_404,redirect
from .forms import NewsForm
from .models import News, Category
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy


class HomeNews(ListView):
    model = News #по сути сделали news = News.objects.all()
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)


# def index(requests):
#     # print(dir(requests))
#     news = News.objects.all()
#     context = {
#                 'news': news,
#                 'title': 'Список новостей'
#                }
#     return render(requests, template_name='news/index.html', context=context)

class NewsByCategory(ListView):
    model = News #по сути сделали news = News.objects.all()
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)



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



class CreateNews(CreateView):
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

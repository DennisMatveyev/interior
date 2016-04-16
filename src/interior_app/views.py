# coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.generic.list import ListView
from interior.utils import get_mailchimp_api
import mailchimp

from .models import (PortfolioObject, 
                     Article, 
                     ArticlePhoto,
                     Category,
                     Tag,
                     Sort,
                     Subscriber,
                     Feedback)
from .forms import ContactForm, SubscriberForm, SelectForm


def home(request):
    portfolios = PortfolioObject.objects.all()
    photos = []
    for portfolio in portfolios:
        for obj in portfolio.photo_set.all():
            photos.append(obj)
    
    form = SubscriberForm()
    feedbacks = Feedback.objects.all()
    context = {"photos": photos[::2], "form": form, "feedbacks": feedbacks}

    return render(request, "home.html", context)

def subscribe(request):
    success = ''
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form_email = form.cleaned_data['email']
            form.save()
            success = "Благодарим Вас за подписку!"
            form = SubscriberForm()
            
            m = get_mailchimp_api()
            email = {"email": form_email}
            m.lists.subscribe('12d4af8bc0', email, 
                              double_optin=False, 
                              update_existing=False, 
                              send_welcome=False)
    else:
        form = SubscriberForm()

    context = {"form": form, "success": success}

    return render(request, "home.html", context)

class PortfolioObjectList(ListView):
    model = PortfolioObject
    context_object_name = 'portfolios'
    template_name = 'portfolio.html'

    def get_context_data(self, **kwargs):
        context = super(PortfolioObjectList, self).get_context_data(**kwargs)
        form = SelectForm()
        context["form"] = form
        return context

def select_by_sort(request):
    if request.method == 'POST':
        form = SelectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sort = Sort.objects.get(name=name)
            portfolios = sort.portfolioobject_set.all()
            context = {"portfolios": portfolios, "name": name, "form": form}
                        
            if portfolios:
                return render(request, 'selected_by_sort.html', context)
            else:
                form = SelectForm()
                info = 'Нет объектов типа ' + str(sort)
                return render(request, 'portfolio.html', {'form': form, 'info': info})
    else:
        form = SelectForm()

    return render(request, 'portfolio.html', {'form': form})

def portfolio_detail(request, object_id=None):
    item = get_object_or_404(PortfolioObject, id=object_id)
    template = "portfolio_detail.html"
    context = {"item": item}

    return render(request, template, context)

def services(request):
    return render(request, "services.html", {})

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sender = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            recipients = ['imat.site@gmail.com']
            try:
                send_mail(subject, message, sender, recipients)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
            return render(request, 'contacts_thanks.html')
    else:
        form = ContactForm()

    return render(request, 'contacts.html', {'form': form}) 

class ArticlesList(ListView):
    context_object_name = 'articles'
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super(ArticlesList, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        tags = Tag.objects.all()
        context['tags'] = tags
        context['categories'] = categories
        return context

    def get_queryset(self):
        articles = Article.objects.all()
        paginator = Paginator(articles, 2)
        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        return articles

class ArticleDetail(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

def search(request):
    if 'search_input' in request.GET and request.GET['search_input']:
        search_input = request.GET['search_input']
        articles = Article.objects.filter(text__icontains=search_input)

        return render(request, 'search_result.html', {'articles': articles})

def category(request, id):
    category = Category.objects.select_related().get(id=id)
    articles = category.article_set.all()
    context = {"articles": articles, "category": category}
    return render(request, 'articles_by_category.html', context)

def tag(request, id):
    tag = Tag.objects.select_related().get(id=id)
    articles = tag.article_set.all()
    context = {"articles": articles, "tag": tag}
    return render(request, 'articles_by_tag.html', context)

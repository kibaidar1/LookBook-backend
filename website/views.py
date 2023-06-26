from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from website.forms import CommentForm, SigUpForm, SignInForm
from website.models import Style, Comment, Clothes


class MainView(View):
    def get(self, request, *args, **kwargs):
        styles = Style.objects.all()
        paginator = Paginator(styles, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        last_styles = Style.objects.all().order_by('-id')[:5]
        # hot_styles = HotStyles.objects.all()
        # common_tags = Style.tag.most_common()[:10]

        return render(request, 'index.html', context={
            'page_obj': page_obj,
            'last_styles': last_styles,
            # 'hot_styles': hot_styles,
            # 'common_tags': common_tags,
        })


class StyleDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        style = get_object_or_404(Style, slug=slug)
        clothes = Clothes.objects.filter(style=style)

        prev_style = style.get_prev_style()
        next_style = style.get_next_style()
        comment_form = CommentForm()

        return render(request, 'style_detail.html', context={
            'style': style,
            'clothes': clothes,
            'prev_style': prev_style,
            'next_style': next_style,
            'comment_form': comment_form
    })

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            author = self.request.user
            style = get_object_or_404(Style, url=slug)
            Comment.objects.create(style=style, author=author, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'style_detail.html', context={
            'comment_form': comment_form
        })


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SigUpForm()
        return render(request, 'signup.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SigUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'signup.html', context={
            'form': form,
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'signin.html', context={
            'form': form,
        })

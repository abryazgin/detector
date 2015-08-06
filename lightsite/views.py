# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response,get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.views.generic import CreateView, UpdateView
from django.views.generic import ListView, DetailView, TemplateView

from .models import Company, Photo, Staff, CompanyLogo, CompanyInvite
from .forms import PhotoForm, CompanyEditForm, CompanyNewForm
from UploadProgressCachedHandler import UploadProgressCachedHandler
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.template import RequestContext
import json, urllib, os
from deta import runner
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class MainView(TemplateView):
    template_name = 'lightsite/main.html'


def check_image_from_ajax(request):
    form = PhotoForm(request.POST, request.FILES)
    print ("check_image_from_ajax", request.FILES, form.is_valid())
    if form.is_valid():
        photo = Photo(photo=request.FILES['photo'])
        photo.save()
        return HttpResponse(
            json.dumps({
                'result': 'success'}))
    else:
        return HttpResponse(
            json.dumps({'data': u"Скорее всего Вы выбрали файл с неподходящим форматом.",
                        'result': 'error'}))


def get_media_path(abspath):
    return abspath.replace(settings.BASE_DIR, '', 1)


def search_logo_from_ajax(request):
    logo = [{'imgPath': get_media_path(result.logoImg), 'company_pk': result.companyId} for result in
            runner.runAll(request.FILES['photo'], None, 2)]
    print ('logo', logo)
    context = {
        "logo": logo,
    };

    return render_to_response("lightsite/finded_logo_snippet.html",
                              context)


def save_logo_from_ajax(request):

    company_id = request.POST.get('company_id', None)
    if company_id:
        try:
            company = Company.objects.get(pk=company_id)

            newLogo = CompanyLogo(company=company, photo=request.FILES['photo'], creator=request.user)
            newLogo.save()
            context = {
                "logo": newLogo,
                "MEDIA_URL": settings.MEDIA_URL
            };

            return render_to_response("lightsite/logo_img_snippet.html",
                                      context)
        except Company.DoesNotExist:
            raise HttpResponseServerError('Не найдена компания ' + company_id)
    else:
        return HttpResponseServerError('Не найден параметр company_id')

def remove_logo_from_ajax(request):
    print request.GET
    logo_id = request.GET.get('logo_id', None)
    if logo_id:
        try:
            logo = CompanyLogo.objects.get(pk=logo_id)
            logo.delete()
            return HttpResponse("Логотип успешно удален")
        except Company.DoesNotExist:
            raise HttpResponseServerError('Не найден логотип ' + logo_id)
    else:
        return HttpResponseServerError('Не найден параметр logo_id')

def remove_company_from_ajax(request):
    print request.GET
    company_id = request.GET.get('company_id', None)
    if company_id:
        try:
            company = Company.objects.get(pk=company_id)
            company.delete()
            return HttpResponse("Компания успешно удалена")
        except Company.DoesNotExist:
            raise HttpResponseServerError('Не найдена компания ' + company_id)
    else:
        return HttpResponseServerError('Не найден параметр company_id')


def get_prev_photo_from_ajax(request):
    latest_photo_list = Photo.objects.order_by('-date_create')[:20]
    context = {
        "latest_photo_list": latest_photo_list,
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render_to_response("lightsite/prev_photo_snippet.html",
                              context)


class ListCompanyView(LoggedInMixin, ListView):
    template_name = 'lightsite/list_company.html'
    model = Company

    def get_context_data(self, **kwargs):
        context = super(ListCompanyView, self).get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context


    def get_queryset(self):
        companies = self.model.objects.filter(staff__user=self.request.user)
        for co in companies:
            co.logos = CompanyLogo.objects.filter(company=co)
            co.invites = CompanyInvite.objects.filter(company=co)
            print co.invites
        return companies

class CompanyEditView(LoggedInMixin, UpdateView):
    model = CompanyInvite
    form_class = CompanyEditForm
    template_name = 'lightsite/edit-company.html'

    def get_success_url(self, pk):
        return reverse('company-view', args=(pk,))

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            ci = CompanyInvite.objects.get(company__pk=pk)
        except CompanyInvite.DoesNotExist:
            print 'creating new invite'
            company = Company.objects.get(pk=pk)
            ci = CompanyInvite(company=company, creator=self.request.user)
            ci.save()
        return ci

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        s = get_object_or_404(CompanyInvite, company__pk=pk)

        form = CompanyEditForm(request.POST, instance=s)
        if form.is_valid():
            ci = form.save()
            form.save()
            return HttpResponse(
            json.dumps({'data': u"Страница успешно сохранилась.",
                        'result': 'success',
                        'next': self.get_success_url(ci.company.pk)}))
        return HttpResponse(
            json.dumps({'data': u"Наполните, пожалуйста, страницу-приветствие.",
                        'result': 'error'}))

class CompanyNewView(LoggedInMixin, FormView):

    form_class = CompanyNewForm
    template_name = 'lightsite/new-company.html'

    def get_success_url(self, pk):
        return reverse('company-list')

    def post(self, request, *args, **kwargs):

        form = CompanyNewForm(request.POST)
        if form.is_valid():

            company = Company(name=form.cleaned_data['name'])
            company.save()

            ci = CompanyInvite(company=company, html=form.cleaned_data['html'], creator=self.request.user)
            ci.save()

            staff = Staff(company=company, user=request.user)
            staff.save()

            return HttpResponse(
            json.dumps({'data': u"Компания успешно сохранилась.",
                        'result': 'success',
                        'next': self.get_success_url(company.pk)}))
        return HttpResponse(
            json.dumps({'data': u"Заполните, пожалуйста, название и страницу-приветствие.",
                        'result': 'error'}))

class CompanyView(TemplateView):

    template_name = 'lightsite/view-company.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        ci = get_object_or_404(CompanyInvite, company__pk=pk)
        context['ci'] = ci
        return context

class ListStatisticView(LoggedInMixin, TemplateView):
    template_name = 'lightsite/list_statistic.html'



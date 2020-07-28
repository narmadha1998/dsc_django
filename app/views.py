# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django import template
from django.http import HttpResponse, JsonResponse
from .models import Camera, Video, Suspect
from django.views.generic import ListView
import json
from json import dumps
from django.db.models import Q
from django.urls import reverse
# @login_required(login_url="/login/")
# def index(request):
#     return render(request, "index.html")
@login_required(login_url="/login/")
def index(request):
    return render(request, "ui-maps.html")

@login_required(login_url="/login/")
def CameraDetailView(request, id=None, *args, **kwargs):
    camera = Camera.objects.get(id=id)
    video = Video.objects.filter(camera=id)
    context={
        'count':len(video),
        'video':video,
        'camera':camera,
    }
    return render(request, "videos.html", context)

@login_required(login_url="/login/")
def suspectDetails(request, id=None, *args, **kwargs):
    video = Video.objects.get(id=id)
    suspects = Suspect.objects.filter(video=id)
    context={
        'suspects' : suspects
    }
    return render(request, "page-user.html", context)

class SearchVideoView(ListView):
    template_name = "search.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchVideoView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self,*args,**kwargs):
        request = self.request
        method_dict=request.GET
        query=method_dict.get('q',None)
        print("Query:",query)
        if query is not None:
            print("SearchProd:",Video.objects.search(query))
            return Video.objects.search(query)
        return Video.objects.all()

@login_required(login_url="/login/")
def oneSuspectData(request, id=None, *args, **kwargs):
    suspects = Suspect.objects.get(id=id)
    context={
        'suspects' : suspects
    }
    return render(request, "ui-typography.html", context)

@login_required(login_url="/login/")
def trackPerson(request, id=None, *args, **kwargs):
    suspects = Suspect.objects.get(id=id)
    context={
        'track' : suspects
    }
    return render(request, "ui-tables.html", context)

@login_required(login_url="/login/")
def VideoDetailView(request, id=None, *args, **kwargs):
    video = Video.objects.get(id=id)
    # xlabels = {"Normal":2478, "Assault":5267, "Burglary":734, "Abuse":433, "Fighting":784}
    xlabels = ["Normal", "Assault", "Burglary", "Abuse", "Fighting"]
    ylabels = [78,4267,734,784,5600]
    json_xlabels = dumps(xlabels)
    json_ylabels = dumps(ylabels)
    context={
        'video':video,
        'crimexlabels':json_xlabels,
        'crimeylabels':json_ylabels,

    }


    return render(request, "video-details.html", context)



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))

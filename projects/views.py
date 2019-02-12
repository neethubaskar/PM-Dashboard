from django.views.generic import TemplateView
from rest_framework.views import APIView
from django.views import View
from django.shortcuts import redirect, render, render_to_response
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login

import requests
import json
import gitlab
import datetime
from datetime import timedelta

from django.contrib.auth.models import User



class LoginPage(TemplateView):
    """ view for rendering login page """
    template_name = 'login.html'


class ProjectView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'project.html')

class DashBoard(View):
    # login_url = "/"

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


class LoginAPIView(APIView):
    """ view for authenticating gitlab account"""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            str_domain = request.data.get('domain')
            str_token = request.data.get('token')
            str_domain = 'http://'+str_domain
            gl = gitlab.Gitlab(str_domain, private_token=str_token)
            gl.auth()
            # import pdb; pdb.set_trace()
            user = authenticate(request, username=str_domain, password=str_token)
            if(user):
                login(request, user)
                token_json = requests.post('http://'+request.get_host()+'/api-token-auth/',{'username':str_domain,'password':str_token})
                token = json.loads(token_json._content.decode("utf-8"))['token']
                return JsonResponse({'status':'success','id':user.id,'token':token})
            new_user = User(username=str_domain, first_name = str_token)
            new_user.set_password(str_token)
            new_user.save()

            user = authenticate(request, username=str_domain, password=str_token)
            login(request, user)
            token_json = requests.post('http://'+request.get_host()+'/api-token-auth/',{'username':str_domain,'password':str_token})
            token = json.loads(token_json._content.decode("utf-8"))['token']
            return JsonResponse({'status':'success','id':new_user.id,'token':token})
        except Exception as e:
            return JsonResponse({'status':'failed'})

class DashboardAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            dat_previous_day = datetime.datetime.now() - timedelta(1)
            dat_previous_day = dat_previous_day.strftime("%Y-%m-%d")
            if not request.data.get('id'):
                return JsonResponse({'status':'failed','project':'Authentication failed'})
            ins_user = list(User.objects.filter(id = int(request.data.get('id'))).values('first_name','username'))
            lst_projects = []

            # gitlab authentication
            gl = gitlab.Gitlab(ins_user[0]['username'], private_token=ins_user[0]['first_name'])
            gl.auth()
            # gitlab owned projects
            projects = gl.projects.list(owned = True)

            int_opend_issues = 0
            int_labeled_issues = 0
            int_commits = 0

            for project in projects:
                dct_project = {}
                # opened issues
                issues = project.issues.list(state='opened')
                if issues:
                    int_opend_issues += len(issues)
                # doing issues
                issues_labeled = project.issues.list(labels=['doing'])
                if issues_labeled:
                    int_labeled_issues += len(issues_labeled)
                # previous day commits
                commits = project.commits.list(since=dat_previous_day+'T00:00:00Z')
                if commits:
                    int_commits += len(commits)

                dct_project['project'] = project.name
                dct_project['id'] = project.id
                lst_projects.append(dct_project)

            dct_dashboard = {}
            dct_dashboard['project'] = lst_projects
            dct_dashboard['opened_issues'] = int_opend_issues
            dct_dashboard['labeled_issues'] = int_labeled_issues
            dct_dashboard['commits'] = int_commits
            return JsonResponse({'status':'success','project':dct_dashboard})
        except Exception as e:
            return JsonResponse({'status':'failed'})


class ProjectAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            dat_previous_day = datetime.datetime.now() - timedelta(1)
            dat_previous_day = dat_previous_day.strftime("%Y-%m-%d")

            int_user_id = int(request.data.get('id'))
            int_project_id = int(request.data.get('project_id'))

            ins_user = list(User.objects.filter(id = int_user_id).values('first_name','username'))
            # gitlab authentication
            gl = gitlab.Gitlab(ins_user[0]['username'], private_token=ins_user[0]['first_name'])
            gl.auth()

            project = gl.projects.get(int_project_id)
            int_issues = len(project.issues.list(state='opened'))
            int_labeled = len(project.issues.list(labels=['doing']))
            int_commits = len(project.commits.list(since=dat_previous_day+'T00:00:00Z'))

            dct_project = {}
            dct_project['issues'] = int_issues
            dct_project['labeled'] = int_labeled
            dct_project['commits'] = int_commits
            return JsonResponse({'status':'success','data':dct_project})
        except Exception as e:
            return JsonResponse({'status':'failed'})

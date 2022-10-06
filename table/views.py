from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from sphinxapi import SphinxClient
from .models import User
from datetime import date


def main_index(request):
    if request.GET:
        last_name = request.GET.get('Last_name')
        first_name = request.GET.get('First_name')
        print(request)
        if first_name and last_name:
            s = SphinxClient()
            s.SetServer('127.0.0.1', 9312)
            s.SetLimits(0, 1000000)
            result = s.Query(first_name and last_name, index='mytest')
            users = []
            if result and result['status'] == 0 and result['total']:
                matches = {row.get('id'): row.get('weight') for row in result['matches']}
                if matches:
                    users = [u for u in User.objects.filter(id__in=matches.keys()).filter(Q(first_name=first_name) & Q(last_name = last_name))]
                    users.sort(key=lambda a: matches.get(a.id, 0))

            return render(request, 'main/index.html',
                          {
                              'first_name': first_name,
                              'datas': users,
                          })
        elif first_name:
            s = SphinxClient()
            s.SetServer('127.0.0.1', 9312)
            s.SetLimits(0, 1000000)
            result = s.Query(first_name, index='mytest')
            users = []
            if result and result['status'] == 0 and result['total']:
                matches = {row.get('id'): row.get('weight') for row in result['matches']}
                if matches:
                    users = [u for u in User.objects.filter(id__in=matches.keys()).filter(first_name = first_name)]
                    users.sort(key=lambda a:matches.get(a.id,0))

            return render(request, 'main/index.html',
                          {
                              'first_name' : first_name,
                              'datas': users,
                          })
        elif last_name:
            s = SphinxClient()
            s.SetServer('127.0.0.1', 9312)
            s.SetLimits(offset=0,limit=1000000)
            result = s.Query(last_name, index='mytest')
            users = []
            if result and result['status'] == 0 and result['total']:
                matches = {row.get('id'): row.get('weight') for row in result['matches']}
                if matches:
                    users = [u for u in User.objects.filter(id__in=matches.keys()).filter(last_name = last_name)]
                    users.sort(key=lambda a: matches.get(a.id, 0))


            return render(request, 'main/index.html',
                          {
                              'Last_name': last_name,
                              'datas': users,
                          })
        else:
            users = User.objects.filter(birthday__day=date.today().day, birthday__month=date.today().month)
            context = {
                'datas': users
            }
            return render(request, 'main/index.html',
                          context)
    else:
        users = User.objects.filter(birthday__day=date.today().day, birthday__month=date.today().month)
        context = {
            'datas': users
        }
        return render(request, 'main/index.html',
                      context)



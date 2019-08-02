# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import DetailView

from rest_framework.decorators import api_view
from rest_framework.response import Response

from consumption import queries
from consumption.models import User, UserConsumption
from consumption.serializers import (
    UserSerializer, UserSummarySerializer, AreaSummarySerializer)


# API rest views
@api_view(["GET"])
def consumption_view(request):
    """returns JSON user summary (via DRF) and custom serializer"""
    consumption = queries.user_summary()
    consumption_serializer = UserSummarySerializer(
        consumption, many=True)
    return Response(consumption_serializer.data)


def data_by_month(request):
    """returns JSON monthly summary (via JsonResponse)"""
    data = list(queries.monthly_summary())
    return JsonResponse(data, safe=False)


def user_data_by_month(request, user_id):
    """returns JSON user's monthly summary (via JsonResponse)"""
    data = list(queries.user_monthly_summary(user_id))
    return JsonResponse(data, safe=False)


def area_data_by_month(request, area_code):
    """returns JSON area's monthly summary (via JsonResponse)"""
    data = list(queries.area_monthly_summary(area_code))
    return JsonResponse(data, safe=False)


# Page Views
def dashboard(request):
    """returns dashboard page"""
    return render(request, 'consumption/summary.html')


class UserDetailView(DetailView):
    """User details view (Class Based View)"""
    template_name = 'consumption/user_detail.html'
    model = User

    def get_context_data(self, **kwargs):
        """adds required context"""
        context = super().get_context_data(**kwargs)
        user = self.object
        context.update({
            "user": user,
            "consumption": user.user_consumption(),
        })
        return context


def area_detail(request, area_code):
    """returns area detail page"""
    context = {
        "area_code": area_code,
        "consumption": queries.area_summary(area_code),
    }
    return render(request, 'consumption/area_detail.html', context)

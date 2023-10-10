import json
from django.http import HttpRequest, JsonResponse, HttpResponseServerError
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from accounts.models import Role
from .models import Issue, Status

import arrow

# Create your views here.


class IssueListView(LoginRequiredMixin, ListView):
    template_name = "issues/list.html"
    model = Issue

    def post(self, request: HttpRequest):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                issue = Issue.objects.get(id=data["id"])
                new_status = Status.objects.get(name=data["status"])
                issue.status = new_status
                issue.save()

            except KeyError:
                HttpResponseServerError("Malfunction")

            return JsonResponse({"success": True})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_team = self.request.user.team
        po_role = Role.objects.get(name="product owner")

        product_owner = get_user_model().objects.get(role=po_role, team=user_team)

        context["todo_issue_list"] = []
        context["inprogress_issue_list"] = []
        context["done_issue_list"] = []

        # Get all issues and order by priority and creation date
        context["issue_list"] = (
            Issue.objects.filter(reporter=product_owner)
            .order_by("created_on")
            .order_by("priority")
            .reverse()
        )

        # Get separated states of issues

        todo = Status.objects.get(name="to do")
        temp_todo_list = context["issue_list"].filter(status=todo)
        for issue in temp_todo_list.all():
            issue.created_on = arrow.get(issue.created_on).humanize()
            context["todo_issue_list"].append(issue)

        in_progress = Status.objects.get(name="in progress")
        temp_in_progress_list = context["issue_list"].filter(status=in_progress)
        for issue in temp_in_progress_list.all():
            issue.created_on = arrow.get(issue.created_on).humanize()
            context["inprogress_issue_list"].append(issue)

        done = Status.objects.get(name="done")
        temp_done_list = context["issue_list"].filter(status=done)
        for issue in temp_done_list.all():
            issue.created_on = arrow.get(issue.created_on).humanize()
            context["done_issue_list"].append(issue)

        return context


class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name = "issues/detail.html"
    model = Issue


class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "description", "assignee", "status", "priority"]

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

    def test_func(self):
        role = Role.objects.get(name="product owner")
        return self.request.user.role == role


class IssueUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ["summary", "description", "assignee", "status", "priority"]

    def form_valid(self, form):
        issue = self.get_object()
        role = Role.objects.get(name="scrum master")
        if form.instance.assignee != issue.assignee and role != self.request.user:
            form.instance.assignee = issue.assignee

        return super().form_valid(form)


class IssueDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("list")

    def test_func(self):
        role = Role.objects.get(name="product owner")
        return role == self.request.user.role

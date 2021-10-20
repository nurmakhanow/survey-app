from rest_framework import permissions


class IsSurveyAdmin(permissions.BasePermission):
    message = "You are not survey-admin"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_survey_admin

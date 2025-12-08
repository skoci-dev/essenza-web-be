from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services import ProjectService
from services.project import dto
from docs.api.public import ProjectPublicAPI

from . import serializers


class ProjectPublicViewSet(BaseViewSet):
    """Public ViewSet for managing projects."""

    _project_service = ProjectService()

    @ProjectPublicAPI.list_projects_schema
    def list_projects(self, request: Request) -> Response:
        """List all projects."""
        str_page_number = request.query_params.get("page", "1")
        str_page_size = request.query_params.get("page_size", "20")

        page = ProjectPublicViewSet._project_service.get_paginated_projects(
            str_page_number=str_page_number,
            str_page_size=str_page_size,
            filters=dto.ProjectFilterDTO(is_active=True),
        )

        return api_response(request).paginated(
            message="Projects retrieved successfully.",
            data=serializers.ProjectCollectionSerializer(page, many=True).data,
            page=page,
        )

    @ProjectPublicAPI.retrieve_project_schema
    def retrieve_project(self, request: Request, slug: str) -> Response:
        """Retrieve a specific project by slug."""
        project, error = ProjectPublicViewSet._project_service.get_project_by_slug(
            slug=slug
        )
        if error:
            return api_response(request).error(
                message=str(error),
            )

        return api_response(request).success(
            message="Project retrieved successfully.",
            data=serializers.ProjectDetailSerializer(project).data,
        )

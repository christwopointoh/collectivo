"""Views of the collectivo core."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from collectivo.version import __version__
from drf_spectacular.utils import extend_schema, OpenApiResponse


class VersionView(APIView):
    """API views of the project version."""

    @extend_schema(responses={200: OpenApiResponse()})
    def get(self, request):
        """Return the current version of the project."""
        data = {
            'version': __version__,
        }
        return Response(data)


class SchemaMixin:
    """Adds an action 'schema' to a viewset."""

    @extend_schema(responses={200: OpenApiResponse()})
    @action(detail=False, url_path='schema', permission_classes=[])
    def _schema(self, request):
        """Return model schema."""
        serializer = self.get_serializer_class()()
        field_data = {}
        for field_name, field_obj in serializer.fields.items():
            field_data[field_name] = {
                "field_type": str(field_obj).split("(")[0],
                "read_only": field_obj.read_only,
                "required": field_obj.required,
                "label": field_obj.label
                # TODO condition, validation, input_type,
                # TODO default value, write_only
            }
            if hasattr(field_obj, "choices"):
                field_data[field_name]["choices"] = field_obj.choices
        return Response(field_data)

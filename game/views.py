from rest_framework import viewsets, generics, filters
from user_account.permissions import IsParticipant, RoleBasedPermission, GameSessionPermission, GameResultPermission
from game.models import GameSession, GameResult
from game.serializers import GameSessionSerializer, GameResultSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


@extend_schema_view(
    list=extend_schema(
        summary="List of Game Sessions",
        responses={
            400: OpenApiResponse(description="Bad request — invalid query parameters."),
            401: OpenApiResponse(description="Unauthorized — authentication credentials were not provided or are invalid."),
            500: OpenApiResponse(description="Internal server error.")
        }
    ),
    retrieve=extend_schema(
        summary="Retrieve a Game Session",
        responses={
            400: OpenApiResponse(description="Bad request — invalid ID."),
            401: OpenApiResponse(description="Unauthorized — authentication credentials were not provided or are invalid."),
            500: OpenApiResponse(description="Internal server error.")
        }
    ),
    create=extend_schema(
        summary="Create a Game Session",
        responses={
            400: OpenApiResponse(description="Bad request — validation error."),
            401: OpenApiResponse(description="Unauthorized — authentication credentials were not provided or are invalid."),
            500: OpenApiResponse(description="Internal server error.")
        }
    ),
    update=extend_schema(
        summary="Update a Game Session",
        responses={
            400: OpenApiResponse(description="Bad request — validation error."),
            401: OpenApiResponse(description="Unauthorized."),
            500: OpenApiResponse(description="Internal server error.")
        }
    ),
    destroy=extend_schema(
        summary="Delete a Game Session",
        responses={
            401: OpenApiResponse(description="Unauthorized."),
            500: OpenApiResponse(description="Internal server error.")
        }
    ),
)
class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer
    permission_classes = [GameSessionPermission]
    ordering_fields = ['id', 'status', 'session_date']
    search_fields = ['id', 'status', 'game__title', 'user__username']

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().select_related('game', 'user', 'user__company')
        if user.role == 'companyadmin':
            return queryset.filter(user__company=user.company)
        elif user.role == 'participant':
            return queryset.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GameResultViewSet(viewsets.ModelViewSet):
    queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer
    permission_classes = [GameResultPermission]
    ordering_fields = ['id', 'score', 'is_completed', 'result_date']
    search_fields = ['id', 'score', 'is_completed', 'session__game__title', 'session__user__username']

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().select_related(
            'session', 'session__game', 'session__user', 'session__user__company',
        )
        if user.role == 'companyadmin':
            return queryset.filter(session__user__company=user.company)
        elif user.role == 'participant':
            return queryset.filter(session__user=user)
        return queryset

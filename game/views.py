from rest_framework import viewsets, generics
# from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView
from user_account.permissions import IsParticipant, IsCompanyAdmin, IsSuperAdmin, RoleBasedPermission
from game.models import GameSession
from game.serializers import GameSessionSerializer


class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer
    permission_classes = [RoleBasedPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().select_related('game', 'user')
        if user.role == 'companyadmin':
            return queryset.filter(user__company=user.company)
        elif user.role == 'participant':
            return queryset.filter(user=user)
        return queryset

class GameSessionParticipantView(generics.ListCreateAPIView):
    permission_classes = [IsParticipant]
    queryset = GameSession.objects.all()
    serializer_class = ...

    def perform_create(self, serializer):
        # Custom logic for creating a game participant
        serializer.save(user=self.request.user)
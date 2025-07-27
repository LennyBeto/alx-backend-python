
#!/usr/bin/env python3
"""
Django REST Framework views for the chats application.

This module defines ViewSets for handling API requests related to
Conversations and Messages.
"""

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from .permissions import IsParticipant # Import your custom permission


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Conversation instances.

    Provides actions for:
    - Listing all conversations the authenticated user is a part of.
    - Retrieving a single conversation.
    - Creating a new conversation.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipant] # Use your custom permission

    def get_queryset(self):
        """
        Filters conversations to only show those the authenticated user is a participant of.
        """
        user = self.request.user
        if user.is_authenticated:
            return Conversation.objects.filter(participants=user).distinct()
        return Conversation.objects.none() # No conversations for unauthenticated users

    def create(self, request, *args, **kwargs):
        """
        Creates a new conversation.

        Expects 'participant_ids' in the request data, which should be a list
        of user IDs to include in the conversation. The authenticated user
        is automatically added as a participant.
        """
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        participant_ids = request.data.get('participant_ids', [])
        if not isinstance(participant_ids, list):
            return Response(
                {"detail": "participant_ids must be a list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure the authenticated user is always a participant
        all_participant_ids = list(set(participant_ids + [str(request.user.id)]))

        # Fetch User instances for all participants
        try:
            participants = User.objects.filter(id__in=all_participant_ids)
            if participants.count() != len(all_participant_ids):
                # Some IDs were not found
                return Response(
                    {"detail": "One or more participant IDs are invalid."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {"detail": "Invalid UUID format for participant IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):

#!/usr/bin/env python3
"""
Django REST Framework serializers for the chats application models.

This module defines serializers for User, Conversation, and Message models,
handling nested relationships for comprehensive API representation.
"""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.

    Serializes user data including ID, names, email, phone number, role,
    and creation timestamp.
    """
    class Meta:
        """Meta options for UserSerializer."""
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'phone_number', 'role', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'username']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.

    Serializes message data, including the sender's details (nested UserSerializer),
    message content, and sent timestamp.
    """
    sender = UserSerializer(read_only=True)  # Nested serializer for sender details

    class Meta:
        """Meta options for MessageSerializer."""
        model = Message
        fields = [
            'message_id', 'conversation', 'sender', 'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.

    Serializes conversation data, including participants (nested UserSerializer)
    and all messages within the conversation (nested MessageSerializer).
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        """Meta options for ConversationSerializer."""
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'messages', 'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at'] 


#!/usr/bin/env python3
"""
Django models for the chats application.

This module defines the database models for users, conversations, and messages
within the messaging application, adhering to the specified schema.
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser to include
    additional fields like phone_number and role.

    Attributes:
        id (UUIDField): Primary key for the user, automatically generated UUID.
                        (Inherited from AbstractUser, but implicitly handled
                        as the primary key for this custom user model).
        first_name (CharField): The first name of the user. (Inherited)
        last_name (CharField): The last name of the user. (Inherited)
        email (EmailField): The email address of the user, must be unique. (Inherited)
        password (CharField): Hashed password for the user. (Inherited)
        phone_number (CharField): Optional phone number for the user.
        role (CharField): The role of the user, chosen from predefined choices.
        created_at (DateTimeField): Timestamp when the user account was created.
                                    (Equivalent to date_joined in AbstractUser,
                                    but explicitly defined as per schema).
    """

    # Define choices for the 'role' field as per ENUM specification
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )

    # Django's AbstractUser already provides id (PK), first_name, last_name,
    # email (unique), password (hash), and date_joined (created_at equivalent).
    # We add fields not explicitly covered or to match specific naming/types.

    # Note: AbstractUser's 'id' is an AutoField. If a UUID primary key
    # 'user_id' is strictly required to replace the default 'id',
    # it would necessitate inheriting from AbstractBaseUser and
    # defining a custom UserManager. For "extension of AbstractUser",
    # we assume AbstractUser's 'id' serves as the primary key.

    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Optional phone number of the user."
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='guest',
        null=False,
        help_text="The role of the user (e.g., guest, host, admin)."
    )
    # AbstractUser already has 'date_joined' which serves as created_at.
    # Adding this explicitly if the schema strictly requires 'created_at' name.
    # If date_joined is sufficient, this field can be removed.
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the user account was created."
    )

    class Meta:
        """
        Meta options for the User model.
        """
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at'] # Order users by creation date

    def __str__(self) -> str:
        """
        String representation of the User instance.
        """
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """
    Model representing a conversation between multiple users.

    Attributes:
        conversation_id (UUIDField): Primary key for the conversation,
                                     automatically generated UUID.
        participants (ManyToManyField): Users involved in this conversation.
        created_at (DateTimeField): Timestamp when the conversation was created.
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the conversation."
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        help_text="Users participating in this conversation."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the conversation was created."
    )

    class Meta:
        """
        Meta options for the Conversation model.
        """
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-created_at'] # Order conversations by creation date

    def __str__(self) -> str:
        """
        String representation of the Conversation instance.
        """
        return f"Conversation {self.conversation_id} ({self.participants.count()} participants)"


class Message(models.Model):
    """
    Model representing a single message within a conversation.

    Attributes:
        message_id (UUIDField): Primary key for the message, automatically generated UUID.
        conversation (ForeignKey): The conversation this message belongs to.
        sender (ForeignKey): The user who sent this message.
        message_body (TextField): The content of the message.
        sent_at (DateTimeField): Timestamp when the message was sent.
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the message."
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message belongs to."
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent this message."
    )
    message_body = models.TextField(
        null=False,
        help_text="The content of the message."
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the message was sent."
    )

    class Meta:
        """
        Meta options for the Message model.
        """
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['sent_at'] # Order messages by sent time

    def __str__(self) -> str:
        """
        String representation of the Message instance.
        """
        return f"Message from {self.sender.username} in {self.conversation.conversation_id}"


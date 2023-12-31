from django.db import models

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email, and password.

        Args:
            username (str): The username for the new user.
            email (str): The email address for the new user.
            password (str): The password for the new user.
            is_staff (bool): Whether the new user is a staff member.
            is_superuser (bool): Whether the new user is a superuser.
            **extra_fields: Additional fields to be saved in the new user object.

        Returns:
            User: The newly created user object.
        """
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        #using refers to the database to use.
        user.save(using=self.db)
        return user


    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email, and password.

        Args:
            username (str): The username for the new user.
            email (str): The email address for the new user.
            password (str, optional): The password for the new user. Defaults to None.
            **extra_fields: Additional fields to be saved in the User model.

        Returns:
            User: The newly created User object.
        """
        return self._create_user(username, email, password, False, False, False, **extra_fields)


    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, email, and password.

        Args:
            username (str): The username for the superuser.
            email (str): The email address for the superuser.
            password (str, optional): The password for the superuser. Defaults to None.
            **extra_fields: Additional fields to be saved in the superuser model.

        Returns:
            User: The newly created superuser.
        """
        return self._create_user(username, email, password, True, True, True, **extra_fields)
    

    def validate_user_code(self, user_id, code):
        """
        Validates the given registration code for the user with the given ID.

        Args:
            user_id (int): The ID of the user to validate the code for.
            code (str): The registration code to validate.

        Returns:
            bool: True if the code is valid for the user, False otherwise.
        """
        if self.filter(id=user_id, register_code=code).exists():
            return True
        return False

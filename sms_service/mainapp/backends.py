from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import Account

class AccountsBackend(ModelBackend):
    """
    Authenticate against the account table
    """

    def authenticate(self, request, username=None, password=None):

        matching_users = Account.objects.filter(username=username)
        login_valid = (len(matching_users) == 1)
        pwd_valid = len(matching_users.filter(auth_id=password)) == 1
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user.
                id = matching_users[0].id
                user = User(username=username, password=password,first_name=id)
                user.save()
            return user
        return None

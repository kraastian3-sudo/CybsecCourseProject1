# A07:2025 - AUTHENTICATION FAILURES
# This custom authentication backend directly compares the
# password supplied by the user with the plaintext password
# stored in Unsafe_user.password.
#
# FIX:
# Use Djangos User model and its default authentication system.
# Comment or delete everything in this file
# Remember to change settings.py also

# from .models import Unsafeuser


# class UnsafeAuthBackend:

#     def authenticate(self, request, username=None, password=None):
#         try:
#             return Unsafeuser.objects.get(
#                 username=username,
#                 password=password
#             )
#         except Unsafeuser.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return Unsafeuser.objects.get(pk=user_id)
#         except Unsafeuser.DoesNotExist:
#             return None
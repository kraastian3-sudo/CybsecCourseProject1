# Vulnerable backend. To fix this you need to just use the default django login function without creating your own authentication.

# from .models import Unsafe_user
#
# class UnsafeAuthBackend:
#
#     def authenticate(self, request, username=None, password=None):
#         try:
#             return Unsafe_user.objects.get(
#                 username=username,
#                 password=password
#             )
#         except Unsafe_user.DoesNotExist:
#             return None
#
#     def get_user(self, user_id):
#         try:
#             return Unsafe_user.objects.get(pk=user_id)
#         except Unsafe_user.DoesNotExist:
#             return None
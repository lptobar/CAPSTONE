from .models import Usuario

class Backend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = Usuario.objects.get(username=username)
            if user.password == password:
                return user
            
            return None
        except Usuario.DoesNotExist:
            return None
    
    def get_user(self, username):
        try:
            user = Usuario.objects.get(username=username)
            return user
        except Usuario.DoesNotExist:
            return None
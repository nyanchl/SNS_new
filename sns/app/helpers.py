from django.contrib.sessions.models import Session

from accounts.models import AuthUser

def get_current_user(request=None):
    if not request:
        return None

    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key).get_decoded()
    uid = session.get('_auth_user_id')

    return AuthUser.objects.get(name=uid)
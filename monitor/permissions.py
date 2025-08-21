
from rest_framework.permissions import BasePermission
from django.conf import settings

class HasAgentApiKey(BasePermission):
    message = 'Invalid API key'

    def has_permission(self, request, view):
        header = request.headers.get('Authorization', '') or request.headers.get('X-API-Key', '')
        token = ''
        if header.startswith('Api-Key '):
            token = header.split(' ',1)[1].strip()
        elif header.startswith('Bearer '):
            token = header.split(' ',1)[1].strip()
        elif header:
            token = header.strip()
        return token in set(settings.AGENT_API_KEYS)

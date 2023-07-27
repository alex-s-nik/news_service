from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.services.auth import logout_user


@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def logout(request):
    logout_user(request.user)
    return Response(status=status.HTTP_204_NO_CONTENT)

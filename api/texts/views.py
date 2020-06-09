from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Credentials


# Create your views here.
class Credential(APIView):

    def put(self, request):
        print(request.data)
        key = request.data.get('key', None)
        shared_secret = request.data.get('shared_secret', None)

        # Validate the request
        if key is None or shared_secret is None:
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        if Credentials.objects.filter(key=key).exists():
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        else:
            new_credential = Credentials(key=key, shared_secret=shared_secret)
            new_credential.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

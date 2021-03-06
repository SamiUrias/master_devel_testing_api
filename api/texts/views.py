from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Credentials, Messages
from .serializers import MessagesSerializer
from .utilities.authentication import authenticate as custom_auth


# Create your views here.
class Credential(APIView):

    def put(self, request):
        print(request.data)
        key = request.data.get('key', None)
        shared_secret = request.data.get('shared_secret', None)

        # Validate the request
        if key is None or shared_secret is None:
            return Response({"message": "Invalid request"},
                            status=status.HTTP_400_BAD_REQUEST)

        if Credentials.objects.filter(key=key).exists():
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        else:
            new_credential = Credentials(key=key, shared_secret=shared_secret)
            new_credential.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)


class Message(APIView):
    def post(self, request):
        # Authentication
        if not custom_auth(self.request.META, request.data):
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        msg = request.data.get('msg', None)
        tag = request.data.get('tag', None)

        if msg is None or tag is None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        new_message = Messages(msg=msg, tag=tag)
        new_message.save()

        return Response({"id": new_message.pk}, status=status.HTTP_200_OK)

    def get(self, request, id=None):
        if id is None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # Authentication
        if not custom_auth(self.request.META, request.data):
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        messages = Messages.objects.filter(pk=id)
        serializer = MessagesSerializer(messages, many=True)
        return Response({"messages": serializer.data},
                        status=status.HTTP_200_OK)


class MessagesWithTag(APIView):
    def get(self, request, tag=None):
        if tag is None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # Authentication
        if not custom_auth(self.request.META, request.data):
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        messages = Messages.objects.filter(tag=tag)
        serializer = MessagesSerializer(messages, many=True)
        return Response({"messages": serializer.data},
                        status=status.HTTP_200_OK)

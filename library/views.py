from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
#probando api
@api_view(['GET'])
def test_api(request):
    return Response({"message": "API funcionando"})




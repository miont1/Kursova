from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AutosModelSerializer
from autos.models import AutosModel, AutoComment, Tag


@api_view(['GET', 'POST'])
def getRoutes(request):
    routes = [
        {'GET': '/api/autos'},
        {'GET': '/api/autos/id'},
        {'POST': '/api/autos/id/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]

    return Response(routes)


@api_view(['GET'])
def getAutos(request):
    autos = AutosModel.objects.all()
    serializer = AutosModelSerializer(autos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getAuto(request, pk):
    auto = AutosModel.objects.get(id=pk)
    serializer = AutosModelSerializer(auto)
    return Response(serializer.data)


@api_view(['POST'])
def autoVote(request, pk):
    auto = AutosModel.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    comment, created = AutoComment.objects.get_or_create(
        from_user=user,
        auto=auto,
    )
    comment.value = data['value']
    comment.save()
    auto.getVoteCount

    serializer = AutosModelSerializer(auto, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    autoId = request.data['auto']

    auto = AutosModel.objects.get(id=autoId)
    tag = Tag.objects.get(id=tagId)

    auto.tags.remove(tag)

    return Response('Tag was deleted')

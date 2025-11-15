from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Reviews


class ReviewCreateSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Reviews
        # fields = ["rating", "description"]
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        # fields = ["uuid", "rating", "description", "created", "modified"]
        fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    # len_name = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ["id", "name", "description"]
        # exclude = ["active"]

    # def get_len_name(self, object):
    #    length = len(object.name)
    #    return length


# URL HyperlinkedModelSerializer
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')
    class Meta:
        model = StreamPlatform
        fields = "__all__"


"""
def description_length(value):
    if len(value) < 2:
        raise serializers.ValidationError('Description too short')

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(
        validators=[description_length]
    )
    active = serializers.BooleanField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('Title and Description should be different')
        return data
        
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Name too short')
        return value
"""

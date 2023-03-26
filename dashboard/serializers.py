from rest_framework import serializers
from dashboard.models import Data

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('d_id', 'stream_id', 'title', 'text')
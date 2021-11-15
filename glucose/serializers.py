from rest_framework import serializers

class GlucoseLevelSerializer(serializers.ModelSerializer):
     class Meta:
        model = "GlucoseLevel"
        fields = ["value"]
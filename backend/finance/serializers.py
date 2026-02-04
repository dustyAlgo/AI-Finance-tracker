from rest_framework import serializers
from .models import Transaction
from .models import Category

class TransactionSerializer(serializers.ModelSerializer):
    predicted_category = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    anomaly_z_score = serializers.FloatField(
        read_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'type',
            'category',
            'predicted_category',
            'amount',
            'date',
            'note',
            'anomaly_z_score',
        ]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
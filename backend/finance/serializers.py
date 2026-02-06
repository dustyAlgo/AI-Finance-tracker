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

    def create(self, validated_data):
        """
        If user provides category → keep it as final.
        Else → assign predicted category.
        """
        transaction = super().create(validated_data)

        if not transaction.category and transaction.predicted_category:
            transaction.category = transaction.predicted_category
            transaction.save(update_fields=["category"])

        return transaction

    def update(self, instance, validated_data):
        """
        If user updates category → it overrides prediction.
        """
        transaction = super().update(instance, validated_data)

        if transaction.category:
            # User override: keep predicted as reference only
            pass
        elif transaction.predicted_category:
            transaction.category = transaction.predicted_category
            transaction.save(update_fields=["category"])

        return transaction



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
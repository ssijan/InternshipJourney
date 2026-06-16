from rest_framework import serializers
from .models import Transaction

class TransactionListSerializer(serializers.ListSerializer):

    def create(self,validated_data):

        objs = [Transaction(**item) for item in validated_data]

        return Transaction.objects.bulk_create(objs)
    
    def update(self, instance, validated_data):
        instance_map = {obj.id: obj for obj in instance}

        res = []

        for i in validated_data:
            obj = i.get("id")
            val = instance_map.get(obj)
            if val:
                res.append(self.child.update(val, i))

        return res
    
class TransactionBulkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"
        list_serializer_class = TransactionListSerializer
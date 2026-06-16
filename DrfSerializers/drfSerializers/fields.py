from decimal import Decimal

from rest_framework import serializers


class MoneyField(serializers.Field):

    RATE = 122.0

    def to_representation(self, value):
        return round(value * self.RATE, 2)

    def to_internal_value(self, data):

        try:
            amount_bdt = Decimal(str(data))

        except:
            raise serializers.ValidationError(
                "Invalid amount"
            )

        return amount_bdt / self.RATE
    

class MaskedCardField(serializers.Field):

    def to_representation(self, value):

        return f"**** **** **** {value[-4:]}"


    def to_internal_value(self, data):

        card = str(data).replace(" ", "")

        if not card.isdigit():
            raise serializers.ValidationError(
                "Card must contain digits only"
            )

        if len(card) != 16:
            raise serializers.ValidationError(
                "Card must be 16 digits"
            )

        return card
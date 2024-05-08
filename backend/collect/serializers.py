from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from collect.models import GOALS, Collect, Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    donator = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Payment
        fields = (
            'amount',
            'comment',
            'donator',
            'date'
        )


class FeedSerializer(serializers.ModelSerializer):
    donator = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username',
    )

    class Meta:
        model = Payment
        fields = (
            'amount',
            'donator',
            'date'
        )


class CollectListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.CharField()
    image = Base64ImageField(required=True)
    goal = serializers.CharField()
    goal_amount = serializers.IntegerField(read_only=False)
    due_to = serializers.DateTimeField()
    donators = serializers.IntegerField()
    collected = serializers.IntegerField()

    class Meta:
        model = Collect
        fields = (
            'id',
            'title',
            'author',
            'image',
            'goal',
            'goal_amount',
            'due_to',
            'donators',
            'collected',
        )


class CollectSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    title = serializers.CharField()
    image = Base64ImageField(required=True)
    goal = serializers.ChoiceField(choices=GOALS)
    goal_amount = serializers.IntegerField(read_only=False)
    due_to = serializers.DateTimeField()
    description = serializers.CharField()

    donators = serializers.IntegerField()
    collected = serializers.IntegerField()
    payments = FeedSerializer(many=True, read_only=True)

    class Meta:
        model = Collect
        fields = (
            'id',
            'title',
            'author',
            'image',
            'goal',
            'goal_amount',
            'due_to',
            'description',
            'donators',
            'collected',
            'payments',
        )

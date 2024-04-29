from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from djoser.serializers import UserSerializer

from api.models import Collect, Payment, GOALS


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
    donator = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            'amount',
            'donator',
            'date'
        )


class CollectListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(required=True)

    goal = serializers.CharField()
    goal_amount = serializers.IntegerField(read_only=False)
    due_to = serializers.DateTimeField()
    collected = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collect
        fields = (
            'title',
            'author',
            'image',
            'goal',
            'goal_amount',
            'collected',
            'due_to',
        )


class CollectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    donations = FeedSerializer(many=True, read_only=True)

    image = Base64ImageField(required=True)
    goal = serializers.ChoiceField(choices=GOALS)
    goal_amount = serializers.IntegerField(read_only=False)
    due_to = serializers.DateTimeField()
    description = serializers.SerializerMethodField()

    donators = serializers.SerializerMethodField()
    collected = serializers.SerializerMethodField()

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
            'donations'
        )

    @staticmethod
    def get_description(obj):
        return obj.formatted_text()

    def get_donators(self, obj):
        donations_list = obj.donations.values('donator').distinct()
        donations_count = donations_list.count()
        return donations_count

    def get_collected(self, obj):
        donations = obj.donations.all()
        collected = sum(donation.amount for donation in donations)
        return collected

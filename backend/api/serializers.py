from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from api.models import Collect, Payment, Goal, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'donations'
        )


class GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = (
            'id',
            'name',
        )


class PaymentSerializer(serializers.ModelSerializer):
    donator = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    donations_to = serializers.PrimaryKeyRelatedField(
        queryset=Collect.objects.all(),
        source='collect.id'
    )

    class Meta:
        model = Payment
        fields = (
            'amount',
            'comment',
            'donator',
            'donations_to',
            'date'
        )


class CollectSerializer(serializers.ModelSerializers):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    donations = PaymentSerializer(many=True, read_only=True)

    image = Base64ImageField(required=True)
    goal = GoalsSerializer(many=False)
    goal_amount = serializers.IntegerField(read_only=False)
    description = serializers.SerializerMethodField()
    due_to = serializers.DateTimeField()

    donators = serializers.IntegerField(read_only=True)
    collected = serializers.IntegerField(read_only=True)

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
            'donations'
        )

    @staticmethod
    def get_description(obj):
        return obj.formatted_text()

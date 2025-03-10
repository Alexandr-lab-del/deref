from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import youtube_url_validator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[youtube_url_validator])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lessons_set')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

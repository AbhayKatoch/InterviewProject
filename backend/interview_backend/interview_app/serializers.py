from rest_framework import serializers
from .models import Candidate, InterviewSession, QuestionAttempt

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "resume",
            "raw_resume_text",
            "ai_parsed_fields",
            "created_at",
            "final_score",
            "final_summary",
        )
        read_only_fields = ("created_at", "final_score", "final_summary")

class QuestionAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAttempt
        fields = (
            "id",
            "session",
            "question_text",
            "index",
            "difficulty",
            "answer_text",
            "score",
            "evaluation",
            "started_at",
            "submitted_at",
        )
        read_only_fields = ("score", "evaluation", "started_at", "submitted_at")

class InterviewSessionSerializer(serializers.ModelSerializer):
    question_attempts = QuestionAttemptSerializer(many=True, read_only=True)

    class Meta:
        model = InterviewSession
        fields = (
            "id",
            "candidate",
            "status",
            "questions",
            "current_index",
            "question_plan_version",
            "created_at",
            "updated_at",
            "question_attempts",
        )
        read_only_fields = ("created_at", "updated_at", "question_attempts")
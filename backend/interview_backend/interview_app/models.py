from django.db import models
from django.utils import timezone

DIFFICULTY_LEVELS = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),           
]
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]   

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    raw_resume_text = models.TextField(blank=True, null=True)
    ai_parsed_resume = models.JSONField(default=dict)

    final_score = models.FloatField(default=0.0)
    final_summary = models.TextField(blank=True)
    def __str__(self):
        return self.name or self.email or f"Candidate {self.id}"
    
class InterviewSession(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='interview_sessions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    questions = models.JSONField(default=list)  # List of questions
    current_index = models.IntegerField(default=0)
    question_plan_version = models.CharField(max_length=50, default='v1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuestionAttempt(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='question_attempts')
    question_text = models.TextField()
    index = models.IntegerField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)

    answer_text = models.TextField(blank=True, null=True)

    score = models.FloatField(default=0.0)
    evaluation = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('session', 'index')
    
    def __str__(self):
        return f"Q{self.index} ({self.difficulty}) for Session {self.session.id}"
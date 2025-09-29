from django.urls import path
from .views import UploadResumeView, StartInterviewView, SubmitAnswerView, CandidatesListAPIView, CandidateDetailAPIView

urlpatterns = [
    path('upload_resume/', UploadResumeView.as_view(), name='upload_resume'),
    path('start_interview/', StartInterviewView.as_view(), name='start_interview'),
    path('submit_answer/', SubmitAnswerView.as_view(), name='submit_answer'),
    path('candidates/', CandidatesListAPIView.as_view(), name='candidates_list'),
    path('candidates/<int:candidate_id>/', CandidateDetailAPIView.as_view(), name='candidate_detail'),
]

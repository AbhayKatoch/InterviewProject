from django.urls import path
from .views import UploadResumeAPIView, StartInterviewAPIView, SubmitAnswerAPIView, CandidatesListAPIView, CandidateDetailAPIView

urlpatterns = [
    path('upload_resume/', UploadResumeAPIView.as_view(), name='upload_resume'),
    path('start_interview/', StartInterviewAPIView.as_view(), name='start_interview'),
    path('submit_answer/', SubmitAnswerAPIView.as_view(), name='submit_answer'),
    path('candidates/', CandidatesListAPIView.as_view(), name='candidates_list'),
    path('candidates/<int:candidate_id>/', CandidateDetailAPIView.as_view(), name='candidate_detail'),
]

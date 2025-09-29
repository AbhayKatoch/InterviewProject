from django.shortcuts import render
import os, uuid, datetime
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, InterviewSession, QuestionAttempt
from .serializers import CandidateSerializer, InterviewSessionSerializer, QuestionAttemptSerializer
from .serivices.ai_service import extract_resume_fields, generate_all_questions, evaluate_answer, generate_summary
from .utils.parser import text_from_pdf, text_from_docx
import requests
TIME_LIMITS = {
    "easy": 20,
    "medium": 60,
    "hard": 120,
}

class UploadResumeView(APIView):
    def post(self,request):
        file = requests.FILES.get('resume')
        if not file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        
        ext = os.path.splitext(file.name)[1].lower()
        tmp_path = default_storage.save(f'tmp/{uuid.uuid4()}{ext}', file)
        file_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

        if ext == '.pdf':
            raw_text = text_from_pdf(file_path)

        elif ext in ['.docx', '.doc']:
            raw_text = text_from_docx(file_path)
        else:
            default_storage.delete(tmp_path)
            return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)
        
        fields= extract_resume_fields(raw_text)
        candidate = Candidate.objects.create(
            resume=tmp_path,
            raw_resume_text=raw_text,
            ai_parsed_fields=fields.dict(),
            name=fields.name,
            email=fields.email,
            phone=fields.phone,
        )
        return Response(CandidateSerializer(candidate).data, status=status.HTTP_201_CREATED)

class StartInterviewView(APIView):

    def post(self, request):
        candidate_id = request.data.get("candidate_id")
        try:
            candidate= Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)
        
        session = InterviewSession.objects.create(candidate=candidate, status='in_progress')    
        q_list = generate_all_questions(role="Full Stack Developer")

        questions_meta = []

        for q in q_list:
            index = q.get("index")
            difficulty = q.get("difficulty", "easy").lower()
            text = q.get("question","").strip()

            meta = {
                "index":index,
                "difficulty": difficulty,
                "text": text,
                "time_limit": TIME_LIMITS.get(difficulty, 20)
            }
            questions_meta.append(meta)
            QuestionAttempt.objects.create(
                session=session,
                question_text=text,
                index=index,
                difficulty=difficulty
            )
        session.questions = questions_meta
        session.save()
        return Response(InterviewSessionSerializer(session).data, status=status.HTTP_201_CREATED)
    
class SubmitAnswerView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        index = int(request.data.get("index", -1))
        answer = request.data.get("answer", "")

        try:
            session = InterviewSession.objects.get(id=session_id)
        except InterviewSession.DoesNotExist:
            return Response({"error": "Interview session not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            attempt = QuestionAttempt.objects.get(index=index)
        except QuestionAttempt.DoesNotExist:
            return Response({"error": "Question attempt not found."}, status=status.HTTP_404_NOT_FOUND)
        
        attempt.answer_text = answer
        attempt.submitted_at = datetime.datetime.now()
        attempt.save()

        result = evaluate_answer(attempt.question_text, answer, attempt.difficulty)
        attempt.score = result.get("score",0)
        attempt.evaluation = result.get("evaluation","")
        attempt.save()

        total_qs = session.attempts.count()
        if index >= total_qs:
            # Interview finished
            attempts = [
                {
                    "question": a.question_text,
                    "answer": a.answer_text,
                    "score": a.score or 0,
                    "difficulty": a.difficulty,
                }
                for a in session.attempts.all().order_by("index")
            ]

            summary = generate_summary(session.candidate.name or "Candidate", attempts)
            final_score = summary.get("final_score", 0)
            final_summary = summary.get("summary", "")

            session.status = "completed"
            session.save()

            cand = session.candidate
            cand.final_score = final_score
            cand.final_summary = final_summary
            cand.save()

            return Response(
                {"finished": True, "final_score": final_score, "summary": final_summary}
            )
        
        next_q = session.questions[index]
        return Response(
            {
                "finished": False,
                "next_question": next_q,
            }
        )

class CandidatesListAPIView(APIView):
    def get(self, request):
        qs = Candidate.objects.all().order_by('-final_score')
        ser = CandidateSerializer(qs, many=True)
        return Response(ser.data)

class CandidateDetailAPIView(APIView):
    def get(self, request, candidate_id):
        try:
            cand = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response({"error":"candidate not found"}, status=404)
        sessions = cand.sessions.all().order_by('-created_at')
        session_ser = InterviewSessionSerializer(sessions, many=True)
        cand_ser = CandidateSerializer(cand)
        return Response({'candidate': cand_ser.data, 'sessions': session_ser.data})
        
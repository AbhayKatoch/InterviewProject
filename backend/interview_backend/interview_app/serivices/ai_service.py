import os, json
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from typing import List, Annotated
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, EmailStr, conint, constr
from dotenv import load_dotenv
load_dotenv()


model = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature = 0.4
)


class ResumeFields(BaseModel):
    name: Annotated[str, Field(description="Candidate full name")] = ""
    email: Annotated[str, Field(description="Candidate email address")] = ""
    phone: Annotated[str, Field(description="Candidate phone number")] = ""

class Question(BaseModel):
    index: Annotated[int, Field(ge=1, le=6, description="Question index 1–6")]
    difficulty: Annotated[str, Field(pattern="^(easy|medium|hard)$", description="Difficulty level")]
    question: Annotated[str, Field(description="Question text")]

class QuestionsList(BaseModel):
    questions: list[Question]

class AnswerEvaluation(BaseModel):
    score: Annotated[int, Field(ge=0, le=10, description="Score 0–10")]
    reason: Annotated[str, Field(description="Reason for score")]

class InterviewSummary(BaseModel):
    final_score: Annotated[int, Field(ge=0, le=100, description="Final score 0–100")]
    summary: Annotated[str, Field(description="Summary of interview")]

resume_parser = PydanticOutputParser(pydantic_object=ResumeFields)
RESUME_PROMPT= PromptTemplate(
    input_variables=["resume_text"],
    template=(
        "Extract the following fields from the resume:\n"
        "- Full Name\n- Email\n- Phone Number\n\n"
        "If missing, leave empty.\n\n"
        "Resume text:\n{resume_text}\n\n"
        "{format_instructions}"
    ),
    partial_variables = {"format_instructions": resume_parser.get_format_instructions()}
)

def extract_resume_fields(resume_text:str)-> ResumeFields:
    chain = RESUME_PROMPT | model | resume_parser
    result = chain.invoke({"resume_text": resume_text}) 
    return result

question_parser = PydanticOutputParser(pydantic_object=QuestionsList)
QUESTION_PROMPT= PromptTemplate(
    input_variables=["role"],
    template=(
        "You are an interviewer for a {role} position (React + Node).\n"
        "Generate EXACTLY 6 interview questions:\n"
        "- 2 Easy\n- 2 Medium\n- 2 Hard\n\n"
        "{format_instructions}"
    ),
    partial_variables = {"format_instructions": question_parser.get_format_instructions()}
)

def generate_all_questions(role = "Full Stack Developer") -> List[Question]:
    chain = QUESTION_PROMPT | model | question_parser
    result = chain.invoke({"role": role}) 
    return result

eval_parser = PydanticOutputParser(pydantic_object=AnswerEvaluation)
EVAL_PROMPT= PromptTemplate(
    input_variables=["question", "answer"],
    template=(
        "Evaluate the candidate's answer to the interview question.\n"
        "QUESTION: {question}\nANSWER: {answer}\nDifficulty: {difficulty}\n\n"
        "Return only JSON.\n\n{format_instructions}"
    ),
    partial_variables = {"format_instructions": eval_parser.get_format_instructions()}
)

def evaluate_answer(question: str, answer: str, difficulty: str="easy") -> AnswerEvaluation:
    chain = EVAL_PROMPT | model | eval_parser
    result = chain.invoke({"question": question.question, "answer": answer, "difficulty": difficulty}) 
    return result

summary_parser = PydanticOutputParser(pydantic_object=InterviewSummary)
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["candidate_name", "attempts"],
    template=(
        "Candidate: {candidate_name}\n"
        "Attempts JSON: {attempts}\n\n"
        "Summarize in max 80 words and compute final score (0-100).\n"
        "{format_instructions}"
    ),
    partial_variables={"format_instructions": summary_parser.get_format_instructions()},
)

def generate_summary(candidate_name: str, attempts: list) -> InterviewSummary:
    chain = SUMMARY_PROMPT | model | summary_parser
    result = chain.invoke({"candidate_name": candidate_name, "attempts": attempts}) 
    return result



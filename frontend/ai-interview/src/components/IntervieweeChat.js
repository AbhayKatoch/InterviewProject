import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { uploadResume } from "../store/candidateSlice";
import { startInterview, submitAnswer, tick } from "../store/sessionSlice";
import { Button, Input, Upload, Card, Typography, Progress } from "antd";

export default function IntervieweeChat() {
  const dispatch = useDispatch();
  const candidate = useSelector((s) => s.candidate.data);
  const session = useSelector((s) => s.session.session);
  const currentQuestion = useSelector((s) => s.session.currentQuestion);
  const timeRemaining = useSelector((s) => s.session.timeRemaining);

  const [answer, setAnswer] = useState("");

  // Timer logic
  useEffect(() => {
    if (!currentQuestion || timeRemaining === null) return;

    if (timeRemaining <= 0) {
      // Auto-submit current answer
      dispatch(
        submitAnswer({
          sessionId: session.id,
          index: currentQuestion.index,
          answer,
        })
      );
      setAnswer("");
      return;
    }

    const interval = setInterval(() => {
      dispatch(tick());
    }, 1000);

    return () => clearInterval(interval);
  }, [dispatch, timeRemaining, currentQuestion, session, answer]);

  // Upload resume handler
  const handleUpload = (file) => {
    dispatch(uploadResume(file));
    return false; // prevent auto upload by antd
  };

  // Step 1: Upload Resume
  if (!candidate) {
    return (
      <Upload beforeUpload={handleUpload}>
        <Button type="primary">Upload Resume</Button>
      </Upload>
    );
  }

  // Step 2: Start Interview
  if (!session) {
    return (
      <Button type="primary" onClick={() => dispatch(startInterview(candidate.id))}>
        Start Interview
      </Button>
    );
  }

  // Step 3: Interview Completed
  if (session.status === "completed") {
    return (
      <Card>
        <Typography.Title level={4}>Interview Finished</Typography.Title>
        <p><b>Score:</b> {session.final_score}</p>
        <p><b>Summary:</b> {session.final_summary}</p>
      </Card>
    );
  }

  // Step 4: Active Question
  return (
    <Card>
      <Typography.Title level={5}>
        Q{currentQuestion.index}: {currentQuestion.text}
      </Typography.Title>

      {/* Timer Progress */}
      <Progress
        percent={(timeRemaining / currentQuestion.time_limit) * 100}
        format={() => `${timeRemaining}s`}
        status={timeRemaining <= 5 ? "exception" : "active"}
      />

      {/* Answer Box */}
      <Input.TextArea
        rows={3}
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
        placeholder="Type your answer..."
        style={{ marginTop: "10px" }}
      />

      {/* Submit Button */}
      <Button
        type="primary"
        style={{ marginTop: "10px" }}
        onClick={() => {
          dispatch(
            submitAnswer({
              sessionId: session.id,
              index: currentQuestion.index,
              answer,
            })
          );
          setAnswer("");
        }}
      >
        Submit
      </Button>
    </Card>
  );
}

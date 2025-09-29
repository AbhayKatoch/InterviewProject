import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchCandidates, fetchCandidateDetail } from "../store/dashboardSlice";
import { Table, Drawer } from "antd";

export default function InterviewerDashboard() {
  const dispatch = useDispatch();
  const candidates = useSelector((s) => s.dashboard.list);
  const selected = useSelector((s) => s.dashboard.selected);

  useEffect(() => {
    dispatch(fetchCandidates());
  }, [dispatch]);

  const columns = [
    { title: "Name", dataIndex: "name" },
    { title: "Email", dataIndex: "email" },
    { title: "Score", dataIndex: "final_score" },
  ];

  return (
    <>
      <Table
        rowKey="id"
        columns={columns}
        dataSource={candidates}
        onRow={(record) => ({
          onClick: () => dispatch(fetchCandidateDetail(record.id)),
        })}
      />
      <Drawer
        title="Candidate Details"
        open={!!selected}
        onClose={() => dispatch(fetchCandidateDetail(null))}
        width={500}
      >
        {selected && (
          <>
            <p><b>Name:</b> {selected.candidate.name}</p>
            <p><b>Email:</b> {selected.candidate.email}</p>
            <p><b>Summary:</b> {selected.candidate.final_summary}</p>
            <h4>Attempts:</h4>
            {selected.sessions[0]?.attempts.map((a) => (
              <div key={a.id}>
                <p>Q{a.index}: {a.question_text}</p>
                <p>A: {a.answer_text}</p>
                <p>Score: {a.score} — {a.evaluator_reason}</p>
              </div>
            ))}
          </>
        )}
      </Drawer>
    </>
  );
}

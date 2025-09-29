import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Tabs, Modal } from "antd";
import { setShowWelcomeBack } from "./store/uiSlice";
import IntervieweeChat from "./components/IntervieweeChat";
import InterviewerDashboard from "./components/InterviewerDashboard";
import { persistStore } from "redux-persist";
import { store } from "./store";

function App() {
  const dispatch = useDispatch();
  const session = useSelector((s) => s.session.session);
  const showWelcomeBack = useSelector((s) => s.ui.showWelcomeBack);

  // Detect unfinished session on load
  useEffect(() => {
    if (session && session.status === "in_progress") {
      dispatch(setShowWelcomeBack(true));
    }
  }, [session, dispatch]);

  // Restart interview = purge Redux + reload
  const handleRestart = () => {
    persistStore(store).purge();
    window.location.reload();
  };

  return (
    <>
      <Tabs defaultActiveKey="1" centered>
        <Tabs.TabPane tab="Interviewee" key="1">
          <IntervieweeChat />
        </Tabs.TabPane>
        <Tabs.TabPane tab="Interviewer" key="2">
          <InterviewerDashboard />
        </Tabs.TabPane>
      </Tabs>

      {/* Welcome Back Modal */}
      <Modal
        title="Welcome Back"
        open={showWelcomeBack}
        onCancel={handleRestart}
        onOk={() => dispatch(setShowWelcomeBack(false))}
        okText="Resume Interview"
        cancelText="Start Over"
      >
        <p>You have an unfinished interview. Would you like to resume where you left off?</p>
      </Modal>
    </>
  );
}

export default App;

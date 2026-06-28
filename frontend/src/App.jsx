import { useState } from "react";
import Header from "./components/Header";
import Login from "./components/Login";
import Homepage from "./components/Homepage";
import CaseInput from "./components/CaseInput";
import LoadingPanel, { STEPS } from "./components/LoadingPanel";
import ProgressBar from "./components/ProgressBar";
import StatusBanner from "./components/StatusBanner";
import ResultsDashboard from "./components/ResultsDashboard";
import WhatIfSimulator from "./components/WhatIfSimulator";
import { useAuth } from "./context/AuthContext";
import { runWorkflow } from "./api/workflowApi";

function App() {
  const { currentUser, rememberMe } = useAuth();
  const [view, setView] = useState("homepage"); // homepage | login | app
  const [status, setStatus] = useState("idle"); // idle | loading | success | showingResult | error | whatIf
  const [result, setResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState("");
  const [currentStep, setCurrentStep] = useState(0);

  function goToHomepage() {
    setView("homepage");
  }

  function handleGetStarted() {
    if (currentUser && rememberMe) {
      setView("app");
    } else {
      setView("login");
    }
  }

  function handleLoginSuccess() {
    setView("app");
  }

  function handleLogout() {
    setView("homepage");
    setStatus("idle");
    setResult(null);
    setErrorMsg("");
  }

  if (view === "homepage") {
    return <Homepage onGetStarted={handleGetStarted} />;
  }

  if (view === "login") {
    return <Login onSuccess={handleLoginSuccess} />;
  }

  async function handleRun(caseId) {
    setStatus("loading");
    setResult(null);
    setErrorMsg("");
    setCurrentStep(0);

    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => Math.min(prev + 1, STEPS.length - 1));
    }, 350);

    const minimumLoadingTime = new Promise((resolve) =>
      setTimeout(resolve, STEPS.length * 350)
    );

    try {
      const [data] = await Promise.all([
        runWorkflow(caseId),
        minimumLoadingTime,
      ]);
      clearInterval(stepInterval);
      setCurrentStep(STEPS.length);
      setResult(data);
      setStatus("success");

      setTimeout(() => {
        setStatus("showingResult");
      }, 1000);
    } catch (err) {
      clearInterval(stepInterval);
      setErrorMsg(err.message);
      setStatus("error");
    }
  }

  function handleReset() {
    setStatus("idle");
    setResult(null);
    setErrorMsg("");
  }

  function handleOpenWhatIf() {
    setStatus("whatIf");
  }

  function handleBackFromWhatIf() {
    setStatus("showingResult");
  }

  return (
    <div className="min-h-screen bg-white dark:bg-slate-950 overflow-y-auto">
      <Header onLogoClick={goToHomepage} onLogout={handleLogout} />

      {status === "loading" && <LoadingPanel currentStep={currentStep} />}

      {(status === "idle" || status === "error") && (
        <CaseInput onRun={handleRun} disabled={false} />
      )}

      {status === "loading" && <ProgressBar currentStep={currentStep} />}

      {status === "success" && (
        <StatusBanner type="success" message="Analysis completed successfully" />
      )}

      {status === "showingResult" && (
        <ResultsDashboard
          result={result}
          onReset={handleReset}
          onOpenWhatIf={handleOpenWhatIf}
        />
      )}

      {status === "whatIf" && (
        <WhatIfSimulator caseId={result.case_id} onBack={handleBackFromWhatIf} />
      )}
    </div>
  );
}

export default App;
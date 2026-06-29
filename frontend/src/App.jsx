import { useState } from "react";
import Header from "./components/Header";
import Login from "./components/Login";
import Homepage from "./components/Homepage";
import CaseInput from "./components/CaseInput";
import LoadingPanel, { STEPS } from "./components/LoadingPanel";
import ProgressBar from "./components/ProgressBar";
import StatusBanner from "./components/StatusBanner";
import ResultsDashboard from "./components/ResultsDashboard";
import ReviewScreen from "./components/ReviewScreen";
import { useAuth } from "./context/AuthContext";
import { analyzeIncident } from "./api/workflowApi";

function App() {
  const { currentUser, rememberMe } = useAuth();
  const [view, setView] = useState("homepage"); // homepage | login | app
  const [status, setStatus] = useState("idle"); // idle | loading | success | showingResult | waitingForReview | error
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

  async function handleRun(incident, mode) {
    setStatus("loading");
    setResult(null);
    setErrorMsg("");
    setCurrentStep(0);

    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => Math.min(prev + 1, STEPS.length - 1));
    }, 350);

    try {
      const data = await analyzeIncident(incident, mode);
      clearInterval(stepInterval);
      setCurrentStep(STEPS.length);
      setResult(data);

      if (data.status === "WAITING_FOR_HUMAN_REVIEW") {
        setStatus("waitingForReview");
      } else {
        setStatus("success");
        setTimeout(() => {
          setStatus("showingResult");
        }, 1000);
      }
    } catch (err) {
      clearInterval(stepInterval);
      setErrorMsg(err.message);
      setStatus("error");
    }
  }

  function handleReviewSubmitted(updatedData) {
    setResult(updatedData);
    setStatus("showingResult");
  }

  function handleReset() {
    setStatus("idle");
    setResult(null);
    setErrorMsg("");
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

      {status === "error" && (
        <>
          <StatusBanner type="error" message="Analysis failed" />
          <p className="text-center text-red-500 -mt-12">{errorMsg}</p>
        </>
      )}

      {status === "waitingForReview" && (
        <ReviewScreen
          result={result}
          onReviewSubmitted={handleReviewSubmitted}
          onBack={handleReset}
        />
      )}

      {status === "showingResult" && (
        <ResultsDashboard result={result} onReset={handleReset} />
      )}
    </div>
  );
}

export default App;
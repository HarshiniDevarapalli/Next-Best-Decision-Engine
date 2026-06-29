import { useState } from "react";
import { motion } from "framer-motion";
import { AlertCircle } from "lucide-react";
import { useAuth } from "../context/AuthContext";

function Login({ onSuccess }) {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    const success = login(username, password, remember);
    if (success) {
      onSuccess();
    } else {
      setError("Invalid username or password.");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-white dark:bg-slate-950 px-4">
      <motion.form
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        onSubmit={handleSubmit}
        className="w-full max-w-sm bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl shadow-sm p-8 flex flex-col gap-5"
      >
        <div className="flex items-center gap-2.5 mb-1">
          <div className="w-10 h-10 rounded-xl bg-brand-darkest dark:bg-brand-light flex items-center justify-center text-white dark:text-slate-900 font-bold text-lg">
            N
          </div>
          <span className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
            NBDE
          </span>
        </div>

        <p className="text-sm text-slate-500 dark:text-slate-400 -mt-2">
          Sign in to access the dashboard
        </p>

        <div>
          <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
            Username
          </label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="mt-1.5 w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-dark transition"
            placeholder="Enter username"
          />
        </div>

        <div>
          <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1.5 w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-dark transition"
            placeholder="Enter password"
          />
        </div>

        <label className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={remember}
            onChange={(e) => setRemember(e.target.checked)}
            className="w-4 h-4 rounded border-slate-300 dark:border-slate-600 text-brand-darkest focus:ring-brand-dark"
          />
          Remember me
        </label>

        {error && (
          <p className="flex items-center gap-1.5 text-sm text-red-500">
            <AlertCircle size={15} />
            {error}
          </p>
        )}

        <button
          type="submit"
          className="mt-1 bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900 py-2.5 rounded-xl font-semibold hover:opacity-90 transition"
        >
          Sign In
        </button>
      </motion.form>
    </div>
  );
}

export default Login;
import { useState } from "react";
import { Settings, ChevronDown } from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { useAuth } from "../context/AuthContext";

function Header({ onLogoClick, onLogout }) {
  const { theme, toggleTheme } = useTheme();
  const { currentUser, logout } = useAuth();
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);

  const displayName =
    currentUser.charAt(0).toUpperCase() + currentUser.slice(1);

  function handleLogout() {
    logout();
    onLogout();
  }

  return (
    <header className="relative w-full flex items-center justify-between px-6 py-4 bg-white dark:bg-slate-950 border-b border-slate-100 dark:border-slate-800">
      <button
        onClick={onLogoClick}
        className="flex items-center gap-2.5 hover:opacity-80 transition"
      >
        <div className="w-8 h-8 rounded-lg bg-brand-darkest dark:bg-brand-light flex items-center justify-center text-white dark:text-slate-900 font-bold">
          N
        </div>
        <span className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
          NBDE
        </span>
      </button>

      <div className="flex items-center gap-3">
        <button
          onClick={() => {
            setSettingsOpen(!settingsOpen);
            setProfileOpen(false);
          }}
          className="w-9 h-9 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition"
        >
          <Settings size={17} />
        </button>

        <button
          onClick={() => {
            setProfileOpen(!profileOpen);
            setSettingsOpen(false);
          }}
          className="flex items-center gap-1.5 pl-1 pr-2 py-1 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition"
        >
          <span className="w-7 h-7 rounded-full bg-brand-darkest dark:bg-brand-light flex items-center justify-center text-white dark:text-slate-900 font-semibold text-sm">
            {displayName.charAt(0)}
          </span>
          <ChevronDown size={14} className="text-slate-400" />
        </button>
      </div>

      {settingsOpen && (
        <div className="absolute right-6 top-16 w-64 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl shadow-lg p-4 flex flex-col gap-4 z-50">
          <div>
            <p className="text-sm font-semibold text-slate-900 dark:text-white mb-2">
              Appearance
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => theme !== "light" && toggleTheme()}
                className={`flex-1 py-2 rounded-lg text-sm font-medium transition ${
                  theme === "light"
                    ? "bg-brand-darkest text-white"
                    : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
                }`}
              >
                Light
              </button>
              <button
                onClick={() => theme !== "dark" && toggleTheme()}
                className={`flex-1 py-2 rounded-lg text-sm font-medium transition ${
                  theme === "dark"
                    ? "bg-brand-light text-slate-900"
                    : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
                }`}
              >
                Dark
              </button>
            </div>
          </div>

          <div className="border-t border-slate-100 dark:border-slate-800 pt-3">
            <button
              onClick={handleLogout}
              className="w-full text-left text-sm text-red-500 font-medium"
            >
              Log out
            </button>
          </div>
        </div>
      )}

      {profileOpen && (
        <div className="absolute right-6 top-16 w-64 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl shadow-lg p-4 flex items-center gap-3 z-50">
          <div className="w-11 h-11 rounded-full bg-brand-darkest dark:bg-brand-light flex items-center justify-center text-white dark:text-slate-900 font-semibold text-lg">
            {displayName.charAt(0)}
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-900 dark:text-white">
              {displayName}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              {currentUser}@nbde.com
            </p>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;
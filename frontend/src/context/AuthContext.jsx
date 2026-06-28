import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

const USERS = [
  { username: "ishitha", password: "Ishitha06" },
  { username: "praneeth", password: "Praneeth05" },
  { username: "harshini", password: "Harshini05" },
];

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [rememberMe, setRememberMe] = useState(false);

  function login(username, password, remember) {
    const match = USERS.find(
      (u) => u.username === username.toLowerCase() && u.password === password
    );

    if (match) {
      setCurrentUser(match.username);
      setRememberMe(remember);
      return true;
    }

    return false;
  }

  function logout() {
    setCurrentUser(null);
    setRememberMe(false);
  }

  return (
    <AuthContext.Provider value={{ currentUser, rememberMe, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
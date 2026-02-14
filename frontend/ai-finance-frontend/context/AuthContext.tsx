"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { loginUser } from "@/lib/api";
import { useRouter } from "next/navigation";

interface AuthContextType {
  accessToken: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      setAccessToken(token);
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    const data = await loginUser(email, password);

    localStorage.setItem("accessToken", data.access);
    localStorage.setItem("refreshToken", data.refresh);

    setAccessToken(data.access);
    router.push("/dashboard");
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setAccessToken(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider
      value={{
        accessToken,
        login,
        logout,
        isAuthenticated: !!accessToken,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};

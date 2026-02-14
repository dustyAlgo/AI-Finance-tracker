"use client";

import axios from "axios";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { registerUser } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await registerUser(username, email, password);

      // After successful registration → redirect to login
      router.push("/login?registered=true");

    } catch (err: unknown) {
        if (axios.isAxiosError(err) && err.response?.data) {
          setError(JSON.stringify(err.response.data));
        } else {
          setError("Registration failed");
        }
      } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-lg shadow-md w-96"
      >
        <h2 className="text-2xl text-black font-bold mb-6 text-center">
          Register
        </h2>

        {error && (
          <p className="text-red-500 text-sm mb-4">{error}</p>
        )}

        <input
          type="text"
          placeholder="Username"
          className="w-full text-gray-400 p-2 mb-4 border rounded"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          type="email"
          placeholder="Email"
          className="w-full text-gray-400 p-2 mb-4 border rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full text-gray-400 p-2 mb-6 border rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-2 rounded text-white transition ${
            loading
              ? "bg-blue-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "Creating account..." : "Register"}
        </button>
      </form>
    </div>
  );
}

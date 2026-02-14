"use client";

import axios from "axios";
import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import { getUserProfile, changePassword } from "@/lib/api";
import Sidebar from "@/components/Sidebar";

export default function ProfilePage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");

  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const [loadingProfile, setLoadingProfile] = useState(true);
  const [loadingPassword, setLoadingPassword] = useState(false);

  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const data = await getUserProfile();
      setUsername(data.username);
      setEmail(data.email);
    } catch (error) {
      console.error("Failed to fetch profile", error);
    } finally {
      setLoadingProfile(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");
    setLoadingPassword(true);

    try {
      const response = await changePassword(oldPassword, newPassword);
      setSuccessMessage(response.detail);
      setOldPassword("");
      setNewPassword("");
    } catch (err: unknown) {
        if (axios.isAxiosError(err) && err.response?.data) {
            setErrorMessage(JSON.stringify(err.response.data));
        } else {
            setErrorMessage("Registration failed");
        }
      } finally {
      setLoadingPassword(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="flex min-h-screen bg-black">
        {/* Sidebar */}
        <Sidebar />
      <div className="min-h-screen p-8 space-y-8">
        <h1 className="text-3xl font-bold">Profile</h1>

        {loadingProfile ? (
          <p>Loading profile...</p>
        ) : (
          <div className="bg-white p-6 rounded shadow space-y-4">
            <div>
              <label className="block text-gray-400 font-semibold">Username</label>
              <input
                type="text"
                value={username}
                disabled
                className="w-full border p-2 rounded bg-blue-400"
              />
            </div>

            <div>
              <label className="block text-gray-400 font-semibold">Email</label>
              <input
                type="email"
                value={email}
                disabled
                className="w-full border p-2 rounded bg-blue-400"
              />
            </div>
          </div>
        )}

        {/* Change Password Section */}
        <div className="bg-white p-6 rounded shadow space-y-4">
          <h2 className="text-xl text-black font-semibold">Change Password</h2>

          {successMessage && (
            <p className="text-green-600 text-sm">{successMessage}</p>
          )}

          {errorMessage && (
            <p className="text-red-600 text-sm">{errorMessage}</p>
          )}

          <form onSubmit={handleChangePassword} className="space-y-4">
            <input
              type="password"
              placeholder="Old Password"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              required
              className="w-full text-gray-400 border p-2 rounded"
            />

            <input
              type="password"
              placeholder="New Password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              className="w-full text-gray-400 border p-2 rounded"
            />

            <button
              type="submit"
              disabled={loadingPassword}
              className={`px-4 py-2 rounded text-white ${
                loadingPassword
                  ? "bg-blue-400 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              {loadingPassword ? "Updating..." : "Update Password"}
            </button>
          </form>
        </div>
      </div>
      </div>
    </ProtectedRoute>
  );
}

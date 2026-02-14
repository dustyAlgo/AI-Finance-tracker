import axios from "axios";

const axiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});
console.log("API BASE URL:", process.env.NEXT_PUBLIC_API_URL);

axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");

  const publicEndpoints = [
    "/api/auth/login",
    "/api/auth/register",
  ];

  const isPublic = publicEndpoints.some((url) =>
    config.url?.includes(url)
  );

  if (token && !isPublic) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default axiosInstance;

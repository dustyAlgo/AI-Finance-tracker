import axiosInstance from "./axiosInstance";

// Auth
export const loginUser = async (email: string, password: string) => {
  const response = await axiosInstance.post("/api/auth/login/", {
    email,
    password,
  });
  return response.data;
};

export const registerUser = async (
  username: string,
  email: string,
  password: string
) => {
  const response = await axiosInstance.post("/api/auth/register/", {
    username,
    email,
    password,
  });
  return response.data;
};
// Categories
export const getCategories = async () => {
    const response = await axiosInstance.get("/api/finance/categories/");
    return response.data;
  };
  
  export const createCategory = async (name: string) => {
    const response = await axiosInstance.post("/api/finance/categories/", {
      name,
    });
    return response.data;
  };
// Transactions
export const getTransactions = async () => {
    const response = await axiosInstance.get("/api/finance/transactions/");
    return response.data;
  };
  
  export const createTransaction = async (data: {
    type: string;
    category: number;
    amount: string;
    date: string;
    note: string;
  }) => {
    const response = await axiosInstance.post(
      "/api/finance/transactions/",
      data
    );
    return response.data;
  };
  
  export const deleteTransaction = async (id: number) => {
    await axiosInstance.delete(`/api/finance/transactions/${id}/`);
  };
  
  // AI Category Prediction
  export const predictCategory = async (note: string) => {
    const response = await axiosInstance.post(
      "/api/finance/transactions/predict-category/",
      { note }
    );
    return response.data;
  };
  // Dashboard
export const getMonthlySummary = async (year: number, month: number) => {
    const response = await axiosInstance.get(
      `/api/finance/monthly-summary/?year=${year}&month=${month}`
    );
    return response.data;
  };
  
  export const getCategoryBreakdown = async (year: number, month: number) => {
    const response = await axiosInstance.get(
      `/api/finance/category-breakdown/?year=${year}&month=${month}`
    );
    return response.data;
  };
  // AI Monthly Summary
export const generateAIMonthlySummary = async (
    year: number,
    month: number
  ) => {
    const response = await axiosInstance.post(
      "/api/finance/ai/monthly-summary/",
      {
        year,
        month,
      }
    );
  
    return response.data;
  };
  
  // Profile
export const getUserProfile = async () => {
  const response = await axiosInstance.get("/api/auth/profile/");
  return response.data;
};

export const changePassword = async (
  old_password: string,
  new_password: string
) => {
  const response = await axiosInstance.post(
    "/api/auth/change-password/",
    {
      old_password,
      new_password,
    }
  );

  return response.data;
};

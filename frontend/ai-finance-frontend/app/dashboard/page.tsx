"use client";

import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import {
  getMonthlySummary,
  getCategoryBreakdown,
  generateAIMonthlySummary,
} from "@/lib/api";
import Sidebar from "@/components/Sidebar";


import {
  PieChart,
  Pie,
  Tooltip,
  ResponsiveContainer,
  Cell,
  Legend,
} from "recharts";

interface Summary {
  income: number;
  expenses: number;
  savings: number;
}

interface ChartData {
  name: string;
  value: number;
}

export default function DashboardPage() {
  const today = new Date();

  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);

  const [summary, setSummary] = useState<Summary | null>(null);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [aiReport, setAiReport] = useState<string | null>(null);

  const [loading, setLoading] = useState(false);
  const [loadingAI, setLoadingAI] = useState(false);

  // ✅ Define colors for each category
const COLORS = [
  '#0088FE',  // Blue
  '#00C49F',  // Green  
  '#FFBB28',  // Yellow
  '#FF8042',  // Orange
  '#8884d8',  // Purple
  '#82ca9d',  // Light Green
  '#ffc658',  // Light Orange
  '#ff7c7c',  // Light Red
];


  useEffect(() => {
    fetchDashboardData();
  }, [year, month]);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const summaryData = await getMonthlySummary(year, month);
      const breakdownData = await getCategoryBreakdown(year, month);

      setSummary(summaryData.summary);

      const formatted = Object.entries(breakdownData.breakdown).map(
        ([name, value]) => ({
          name,
          value: value as number,
        })
      );
      

      setChartData(formatted);
    } catch (error) {
      console.error("Dashboard fetch failed", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAI = async () => {
    setLoadingAI(true);
    try {
      const result = await generateAIMonthlySummary(year, month);
      console.log("AI API response:", result);
      setAiReport(result.summary);
    } catch (error) {
      console.error("AI generation failed:", error);
    } finally {
      setLoadingAI(false);
    }
  };
  

  return (
    <ProtectedRoute>
      <div className="flex min-h-screen bg-black">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <div className="flex-1 p-8 space-y-8">

        <h1 className="text-3xl font-bold">Dashboard</h1>

        {/* Month Selector */}
        <div className="flex gap-4">
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(Number(e.target.value))}
            className="border p-2 rounded"
          />

          <input
            type="number"
            min="1"
            max="12"
            value={month}
            onChange={(e) => setMonth(Number(e.target.value))}
            className="border p-2 rounded"
          />
        </div>

        {loading ? (
          <p>Loading dashboard...</p>
        ) : (
          <>
            {/* Summary Cards */}
            {summary && (
              <div className="grid grid-cols-3 gap-6">
                <div className="bg-green-100 text-black p-6 rounded shadow">
                  <h3 className="font-semibold">Income</h3>
                  <p className="text-xl">₹{summary.income}</p>
                </div>

                <div className="bg-red-100 text-black p-6 rounded shadow">
                  <h3 className="font-semibold">Expenses</h3>
                  <p className="text-xl">₹{summary.expenses}</p>
                </div>

                <div className="bg-blue-100 text-black p-6 rounded shadow">
                  <h3 className="font-semibold">Savings</h3>
                  <p className="text-xl">₹{summary.savings}</p>
                </div>
              </div>
            )}

            {/* Pie Chart */}
            <div className="h-96 bg-white text-blue-300 p-6 rounded shadow">
              <h3 className="mb-4 font-semibold">Expense Breakdown</h3>

              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chartData}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={120}
                    label
                  >
                    {/* ✅ ADD COLORS ARRAY */}
                    {chartData.map((entry, index) => (
                      <Cell 
                        key={`cell-${index}`} 
                        fill={COLORS[index % COLORS.length]} 
                      />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* AI Section */}
            <div className="bg-gray-100 p-6 text-purple-400 rounded shadow space-y-4">
              <h3 className="font-semibold">
                🤖 AI Financial Analysis
              </h3>

              <button
                onClick={handleGenerateAI}
                disabled={loadingAI}
                className={`px-4 py-2 rounded text-white font-medium flex items-center gap-2 transition-all ${
                  loadingAI 
                    ? "bg-gray-400 cursor-not-allowed" 
                    : "bg-purple-600 hover:bg-purple-700"
                }`}
              >
                {loadingAI ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Generating...
                  </>
                ) : (
                  "Generate AI Report"
                )}
              </button>


              {loadingAI && <p>Generating AI insights...</p>}

              {aiReport && (
                <div className="bg-white p-4 text-black rounded whitespace-pre-wrap">
                  {aiReport}
                </div>
              )}
            </div>
          </>
            )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
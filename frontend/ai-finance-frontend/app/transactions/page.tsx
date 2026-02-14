"use client";

import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import Sidebar from "@/components/Sidebar";
import {
  getTransactions,
  createTransaction,
  deleteTransaction,
  getCategories,
  predictCategory,
} from "@/lib/api";

interface Category {
  id: number;
  name: string;
}

interface Transaction {
  id: number;
  type: string;
  category: number;
  amount: string;
  date: string;
  note: string;
}

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);

  const [type, setType] = useState("EXPENSE");
  const [category, setCategory] = useState<number | null>(null);
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState("");
  const [note, setNote] = useState("");

  const fetchData = async () => {
    const tx = await getTransactions();
    const cats = await getCategories();
    setTransactions(tx);
    setCategories(cats);
  };
  useEffect(() => {
    fetchData();
  }, []);

// Auto AI Category Prediction (FIXED)
console.log("Categories available:", categories.map(c => ({id: c.id, name: c.name})));
useEffect(() => {
    const debounce = setTimeout(async () => {
      if (note.length > 3 && categories.length > 0) {
        try {
          const prediction = await predictCategory(note);
          console.log("Searching for category matching:", prediction.predicted_category);
          
          console.log("API Response:", prediction);
          
          const predictedName = prediction.predicted_category;
          
          // FIXED: Proper case-insensitive match
          const matched = categories.find(cat => 
            cat.name.toLowerCase() === predictedName.toLowerCase()
          );
          
          console.log("Matched category:", matched); // ← This will show truth now
          
          if (matched) {
            console.log("Setting category:", matched.id, matched.name);
            setCategory(matched.id);
          } else {
            console.log("No match found. Available:", categories.map(c => c.name));
          }
        } catch (err) {
          console.error("Prediction failed", err);
        }
      }
    }, 500);
  
    return () => clearTimeout(debounce);
  }, [note, categories]);
  
  
  

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!category) return;

    const newTx = await createTransaction({
      type,
      category,
      amount,
      date,
      note,
    });

    setTransactions((prev) => [...prev, newTx]);

    setAmount("");
    setDate("");
    setNote("");
  };

  const handleDelete = async (id: number) => {
    await deleteTransaction(id);
    setTransactions((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <ProtectedRoute>
      <div className="flex min-h-screen bg-black">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <div className="flex-1 p-8 space-y-8">
        <h1 className="text-3xl font-bold mb-6">Transactions</h1>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4 mb-8">
          <select
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="border p-2 rounded w-full"
          >
            <option value="EXPENSE">Expense</option>
            <option value="INCOME">Income</option>
          </select>

          <select
            value={category || ""}
            onChange={(e) => setCategory(Number(e.target.value))}
            className="border p-2 rounded w-full"
          >
            <option value="">Select Category</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>

          <input
            type="number"
            placeholder="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="border p-2 rounded w-full"
            required
          />

          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="border p-2 rounded w-full"
            required
          />

          <input
            type="text"
            placeholder="Note"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            className="border p-2 rounded w-full"
          />

          <button className="bg-blue-600 text-black px-4 py-2 rounded">
            Add Transaction
          </button>
        </form>

        {/* Transactions List */}
        <ul className="space-y-3">
          {transactions.map((tx) => (
            <li
              key={tx.id}
              className="p-4 bg-blue-300 rounded flex justify-between"
            >
              <div>
                <p>
                  {tx.type} - ₹{tx.amount}
                </p>
                <p className="text-sm text-black-100">
                  {tx.note}
                </p>
              </div>

              <button
                onClick={() => handleDelete(tx.id)}
                className="text-red-500"
              >
                Delete
              </button>
            </li>
          ))}
                </ul>
      </div>
    </div>
    </ProtectedRoute>
  );
}

"use client";

import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import { getCategories, createCategory } from "@/lib/api";
import Sidebar from "@/components/Sidebar";

interface Category {
  id: number;
  name: string;
}

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [newCategory, setNewCategory] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data);
    } catch (error) {
      console.error("Failed to fetch categories", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCategory.trim()) return;

    try {
      const created = await createCategory(newCategory);
      setCategories((prev) => [...prev, created]);
      setNewCategory("");
    } catch (error) {
      console.error("Failed to create category", error);
    }
  };

  return (
    <ProtectedRoute>
      <div className="flex min-h-screen bg-black">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <div className="flex-1 p-8 space-y-8">
        <h1 className="text-3xl font-bold mb-6">Categories</h1>

        <form onSubmit={handleAddCategory} className="mb-6 flex gap-4">
          <input
            type="text"
            placeholder="New category"
            className="border p-2 rounded w-64"
            value={newCategory}
            onChange={(e) => setNewCategory(e.target.value)}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Add
          </button>
        </form>

        {loading ? (
          <p>Loading...</p>
        ) : (
          <ul className="space-y-2">
            {categories.map((cat) => (
              <li
                key={cat.id}
                className="p-3 bg-black-100 rounded"
              >
                {cat.name}
              </li>
            ))}
          </ul>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function Sidebar() {
  const pathname = usePathname();
  const { logout } = useAuth();

  const navItems = [
    { name: "Dashboard", href: "/dashboard" },
    { name: "Transactions", href: "/transactions" },
    { name: "Categories", href: "/categories" },
    { name: "Profile", href: "/profile" },
  ];

  return (
    <div className="h-screen w-64 bg-black border-r flex flex-col justify-between p-6">
      {/* Top Section */}
      <div>
        <h2 className="text-xl font-bold mb-8">
          FinBOT- @YourPersonalAI
        </h2>

        <nav className="space-y-4">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`block px-3 py-2 rounded transition ${
                pathname === item.href
                  ? "bg-black text-white"
                  : "text-gray-400 hover:bg-gray-100"
              }`}
            >
              {item.name}
            </Link>
          ))}
        </nav>
      </div>

      {/* Bottom Section */}
      <button
        onClick={logout}
        className="mt-8 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
      >
        Logout
      </button>
    </div>
  );
}

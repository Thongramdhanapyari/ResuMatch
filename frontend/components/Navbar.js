"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    localStorage.removeItem("auth");
    window.location.reload();
  };

  return (
    <header className="sticky top-0 z-50 border-b border-[var(--muted)]/30 bg-[#64748B]/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        
        <h1 className="text-xl font-semibold tracking-tight text-[var(--foreground)]">
          <span>Resu</span>
          <span className="text-[var(--accent)]">Match</span>
        </h1>

        <nav className="flex gap-8">
          <a href="#features" className="text-sm text-white/80 hover:text-white transition">
            Features
          </a>
          <a href="#faq" className="text-sm text-white/80 hover:text-white transition">
            FAQ
          </a>
          <a href="#how-it-works" className="text-sm text-white/80 hover:text-white transition">
            How it works
          </a>
        </nav>

        {user ? (
          <div className="flex items-center gap-4">
            <span className="text-sm text-white">
              Welcome, <span className="font-semibold">{user.name}</span>
            </span>
            <button
              onClick={handleLogout}
              className="rounded-xl bg-[var(--accent)] px-4 py-2 text-sm font-medium text-[var(--background)] hover:opacity-80 transition"
            >
              Logout
            </button>
          </div>
        ) : (
          <Link
            href="/login"
            className="rounded-xl bg-[var(--accent)] px-4 py-2 text-sm font-medium text-[var(--background)] hover:opacity-80 transition"
          >
            Sign In
          </Link>
        )}
      </div>
    </header>
  );
}
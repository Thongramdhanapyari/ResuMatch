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
      <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 sm:px-6 md:flex-row md:items-center md:justify-between md:px-8 md:py-5">
        
        <h1 className="text-center text-lg font-semibold tracking-tight text-[var(--foreground)] md:text-2xl">
          <span>Resu</span>
          <span className="text-[var(--accent)]">Match</span>
        </h1>

        <nav className="flex flex-wrap justify-center gap-4 md:gap-8">
          <a href="#features" className="text-sm text-white/80 transition hover:text-white md:text-base">
            Features
          </a>
          <a href="#faq" className="text-sm text-white/80 transition hover:text-white md:text-base">
            FAQ
          </a>
          <a href="#how-it-works" className="text-sm text-white/80 transition hover:text-white md:text-base">
            How it works
          </a>
        </nav>

        {user ? (
          <div className="flex flex-col items-center gap-3 sm:flex-row sm:justify-center md:gap-5">
            <span className="max-w-[180px] truncate text-sm text-white md:max-w-[220px] md:text-base">
              Welcome, <span className="font-semibold">{user.name}</span>
            </span>
            <button
              onClick={handleLogout}
              className="rounded-xl bg-[var(--accent)] px-4 py-2 text-sm font-medium text-[var(--background)] transition hover:opacity-80 md:px-5 md:py-2.5 md:text-base"
            >
              Logout
            </button>
          </div>
        ) : (
          <div className="flex justify-center">
            <Link
              href="/login"
              className="rounded-xl bg-[var(--accent)] px-4 py-2 text-sm font-medium text-[var(--background)] transition hover:opacity-80 md:px-5 md:py-2.5 md:text-base"
            >
              Sign In
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}
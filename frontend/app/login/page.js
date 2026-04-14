"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await response.json();

      if (!response.ok) {
        let message = "Something went wrong";

        if (Array.isArray(data.detail)) {
          message = "";

          data.detail.forEach((err) => {
            if (err.loc?.includes("email")) {
              message += "Enter a valid email address. ";
            }
            if (err.loc?.includes("password")) {
              message += "Password must be at least 6 characters. ";
            }
          });
        } else if (typeof data.detail === "string") {
          message = data.detail;
        }

        throw new Error(message);
      }

      localStorage.setItem("token", data.access_token);

      if (data.user) {
        localStorage.setItem("user", JSON.stringify(data.user));
      }

      localStorage.setItem("auth", "true");

      router.push("/");
    } catch (err) {
      setError(err.message || "Login failed");
    }
  };

  return (
    <main className="relative min-h-screen bg-[#E5E7EB] px-4 py-6 md:px-6 md:py-10">
      <Link
        href="/"
        className="absolute left-3 top-3 text-[11px] text-[#64748B] hover:text-[#1E293B]"
      >
        ← Back
      </Link>

      <div className="mx-auto flex min-h-[calc(100vh-2rem)] max-w-xs md:max-w-md items-center justify-center">
        <div className="w-full rounded-xl border border-[#D1D5DB] bg-white/70 p-4 md:p-6 shadow-sm backdrop-blur-sm">
          <span className="inline-flex text-[16px] md:text-[20px] font-medium text-[#1E293B] text-center w-full">
            Welcome back!
          </span>

          <h1 className="mt-3 text-xs md:text-sm font-semibold leading-tight text-[#64748B] text-center">
            <span>Log in to continue your resume journey.</span>
          </h1>

          <form className="mt-4 space-y-2.5 md:space-y-3" onSubmit={handleLogin}>
            <input
              type="email"
              name="email"
              placeholder="Email"
              onChange={handleChange}
              className="w-full rounded-xl border border-[#D1D5DB] bg-[#F8FAFC] p-2.5 md:p-3 text-[12px] md:text-sm outline-none focus:border-[#64748B]"
            />

            <input
              type="password"
              name="password"
              placeholder="Password"
              onChange={handleChange}
              className="w-full rounded-xl border border-[#D1D5DB] bg-[#F8FAFC] p-2.5 md:p-3 text-[12px] md:text-sm outline-none focus:border-[#64748B]"
            />

            {error && (
              <p className="text-[10px] text-red-500">{error}</p>
            )}

            <button
              type="submit"
              className="w-full rounded-xl bg-[#64748B] p-2.5 md:p-3 text-[12px] md:text-sm font-semibold text-white hover:bg-[#475569]"
            >
              Log In
            </button>
          </form>

          <p className="mt-4 text-center text-[11px] md:text-xs text-[#64748B]">
            Log in to analyze resumes and improve your match score.
          </p>

          <p className="mt-2 text-center text-[12px] md:text-sm text-[#64748B]">
            Don’t have an account?{" "}
            <Link href="/signup" className="font-semibold text-[#1E293B]">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </main>
  );
}
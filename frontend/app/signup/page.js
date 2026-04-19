"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const router = useRouter();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");

    if (!form.name.trim() || !form.email.trim() || !form.password.trim()) {
      setError("All fields are required");
      return;
    }

    const API_URL = process.env.NEXT_PUBLIC_API_URL;
    if (!API_URL) {
      setError("API not configured");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(`${API_URL}/api/auth/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: form.name.trim(),
          email: form.email.trim(),
          password: form.password,
        }),
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
            if (err.loc?.includes("name")) {
              message += "Name is required. ";
            }
          });

          if (!message.trim()) {
            message = "Invalid input";
          }
        } else if (typeof data.detail === "string") {
          message = data.detail;
        }

        throw new Error(message);
      }

      localStorage.setItem("token", data.access_token);

      if (data.user) {
        localStorage.setItem("user", JSON.stringify(data.user));
      }

      router.push("/");
    } catch (err) {
      setError(err.message || "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#E5E7EB] px-4 py-6 md:px-6 md:py-10">
      <div className="mx-auto grid max-w-6xl gap-10 lg:grid-cols-2 lg:items-center">
        <div className="ml-10 max-w-xl">
          <span className="inline-flex rounded-full border border-[#D1D5DB] bg-[#F3F4F6] px-2 py-1.5 text-xs font-medium text-[#64748B] shadow-sm md:text-sm">
            Create your account
          </span>

          <h1 className="mt-4 text-sm font-semibold leading-tight text-[#1E293B] md:text-xl">
            Start building a smarter
            <span className="block text-[#64748B]">resume strategy</span>
          </h1>

          <p className="mt-5 text-sm leading-5 text-[#64748B] md:text-base">
            Sign up to analyze resumes, compare them with job descriptions, and
            get practical suggestions to improve your chances.
          </p>

          <div className="mt-7 flex flex-wrap gap-4">
            <Link
              href="/"
              className="rounded-2xl border border-[#D1D5DB] px-6 py-2.5 text-xs font-semibold text-[#1E293B] transition hover:bg-[#F3F4F6] md:text-sm"
            >
              ← Back Home
            </Link>
          </div>
        </div>

        <div className="relative mr-15 flex justify-center lg:justify-end">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-[420px] w-[420px] rounded-full bg-[#60A5FA]/30 blur-[120px]" />
          </div>

          <div className="relative w-full max-w-xs rounded-[24px] border border-[#D1D5DB] bg-white/70 p-5 shadow-md backdrop-blur-sm md:max-w-md md:p-6">
            <p className="mt-2 text-xs text-[#64748B] md:text-sm">
              Create your account to get started.
            </p>

            <form
              className="mt-4 space-y-3 mr-3 md:space-y-4"
              onSubmit={handleSignup}
            >
              <input
                type="text"
                name="name"
                placeholder="Full name"
                value={form.name}
                onChange={handleChange}
                required
                className="w-full rounded-xl border border-[#D1D5DB] bg-[#F8FAFC] p-3 text-xs text-[#1E293B] outline-none transition placeholder:text-[#94A3B8] focus:border-[#64748B] md:p-3.5 md:text-sm"
              />

              <input
                type="email"
                name="email"
                placeholder="Email address"
                value={form.email}
                onChange={handleChange}
                required
                className="w-full rounded-xl border border-[#D1D5DB] bg-[#F8FAFC] p-3 text-xs text-[#1E293B] outline-none transition placeholder:text-[#94A3B8] focus:border-[#64748B] md:p-3.5 md:text-sm"
              />

              <input
                type="password"
                name="password"
                placeholder="Password"
                value={form.password}
                onChange={handleChange}
                required
                className="w-full rounded-xl border border-[#D1D5DB] bg-[#F8FAFC] p-3 text-xs text-[#1E293B] outline-none transition placeholder:text-[#94A3B8] focus:border-[#64748B] md:p-3.5 md:text-sm"
              />

              {error && <p className="text-[10px] text-red-500">{error}</p>}

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-xl bg-[#64748B] px-3 py-3 text-xs font-semibold text-white transition hover:bg-[#475569] disabled:cursor-not-allowed disabled:opacity-70 md:py-3.5 md:text-sm"
              >
                {loading ? "Signing Up..." : "Sign Up"}
              </button>
            </form>

            <p className="mt-6 text-center text-xs text-[#64748B] md:text-sm">
              Already have an account?{" "}
              <Link href="/login" className="font-semibold text-[#1E293B]">
                Log in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
"use client";

import { useEffect, useState } from "react";

export default function HistorySection() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/history`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!res.ok) {
          throw new Error("Failed to fetch history");
        }

        const data = await res.json();

        const parsed = data.map((item) => ({
          ...item,
          matched_skills: JSON.parse(item.matched_skills || "[]"),
          missing_skills: JSON.parse(item.missing_skills || "[]"),
          suggestions: JSON.parse(item.suggestions || "[]"),
        }));

        setHistory(parsed);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchHistory();
  }, []);

  return (
    <section id="history" className="mt-10 scroll-mt-28">
      <h2 className="text-lg font-semibold text-[#1E293B] mb-4">
        Analysis History
      </h2>

      {error && (
        <p className="text-sm text-red-500 mb-4">{error}</p>
      )}

      {!history.length ? (
        <p className="text-sm text-[#64748B]">No history yet.</p>
      ) : (
        <div className="space-y-4">
          {history.map((item) => (
            <div
              key={item.id}
              className="border rounded-xl p-4 bg-white shadow-sm"
            >
              <p className="text-sm text-[#64748B]">
                {new Date(item.created_at).toLocaleString()}
              </p>

              <p className="font-semibold text-[#1E293B] mt-1">
                {item.job_title}
              </p>

              <p className="text-sm mt-2">
                Match Score: <strong>{item.match_score}%</strong>
              </p>

              <div className="mt-2 text-sm">
                <p>
                  <strong>Matched:</strong>{" "}
                  {item.matched_skills.join(", ")}
                </p>
                <p>
                  <strong>Missing:</strong>{" "}
                  {item.missing_skills.join(", ")}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
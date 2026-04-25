"use client";

import { useState } from "react";
import JobMatchForm from "./JobMatchForm";
import ResumeQualityForm from "./ResumeQualityForm";
import ResultsPanel from "./ResultsPanel";

export default function AnalyzerPage() {
  const [mode, setMode] = useState(null);

  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const resetMode = () => {
    setMode(null);
    setResume(null);
    setJobDescription("");
    setResult(null);
    setError("");
  };

  const handleAnalyze = async () => {
    if (!resume) {
      setError("Please upload a resume");
      return;
    }

    if (mode === "job" && !jobDescription.trim()) {
      setError("Please enter job description");
      return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
      setError("Please login first");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("resume", resume);

      if (mode === "job") {
        formData.append("job_description", jobDescription);
      }

      const endpoint =
        mode === "quality"
          ? "/api/analyze/resume-quality"
          : "/api/analyze/job-match";

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}${endpoint}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error("Analysis failed");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Failed");
    } finally {
      setLoading(false);
    }
  };

  if (!mode) {
    return (
      <section
        id="analyzer"
        className="flex min-h-[520px] w-full items-center bg-white py-12 md:py-16"
      >
        <div className="w-full px-4 md:px-8">
          <div className="text-center">
            <h2 className="text-sm font-bold text-[#1E293B] md:text-2xl">
              Resume Analyzer
            </h2>

            <p className="mt-3 text-xs text-[#64748B] md:mt-4 md:text-base">
              Choose how you want to analyze your resume.
            </p>
          </div>

          <div className="mt-8 flex flex-col items-center gap-8 sm:flex-row sm:justify-center sm:gap-12 md:mt-10 md:gap-16">
            <button
              onClick={() => setMode("quality")}
              className="flex h-40 w-40 flex-col items-center justify-center gap-3 rounded-[30px] border-2 border-dashed border-[#CBD5E1] bg-[#F8FAFC] text-center shadow-sm transition hover:border-[#94A3B8] hover:bg-white md:h-52 md:w-52 md:gap-4 md:rounded-[36px]"
            >
              <span className="rounded-xl bg-[#64748B] px-3 py-1.5 text-xs font-semibold text-white md:px-4 md:py-2 md:text-sm">
                Resume Quality
              </span>

              <p className="px-3 text-[10px] leading-tight text-[#64748B] md:px-4 md:text-xs">
                ATS score, skills, formatting.
              </p>
            </button>

            <button
              onClick={() => setMode("job")}
              className="flex h-40 w-40 flex-col items-center justify-center gap-3 rounded-[30px] border-2 border-dashed border-[#CBD5E1] bg-[#F8FAFC] text-center shadow-sm transition hover:border-[#94A3B8] hover:bg-white md:h-52 md:w-52 md:gap-4 md:rounded-[36px]"
            >
              <span className="rounded-xl bg-[#64748B] px-3 py-1.5 text-xs font-semibold text-white md:px-4 md:py-2 md:text-sm">
                Job Match
              </span>

              <p className="px-3 text-[10px] leading-tight text-[#64748B] md:px-4 md:text-xs">
                Compare with job description.
              </p>
            </button>
          </div>

          <p className="mx-auto mt-5 max-w-md text-center text-xs text-[#64748B] md:mt-6 md:text-sm">
            Get a detailed analysis of your resume with insights on ATS performance, skills, and job readiness.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section
      id="analyzer"
      className="flex min-h-[520px] w-full items-center bg-white py-12 md:py-16"
    >
      <div className="w-full px-4 md:px-8">
        <div className="mb-4">
          <button
            onClick={resetMode}
            className="text-sm text-[#475569] hover:underline"
          >
            ← Back
          </button>
        </div>

        {mode === "quality" && (
          <ResumeQualityForm
            resume={resume}
            setResume={setResume}
            handleAnalyze={handleAnalyze}
            loading={loading}
            error={error}
          />
        )}

        {mode === "job" && (
          <JobMatchForm
            resume={resume}
            setResume={setResume}
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            handleAnalyze={handleAnalyze}
            loading={loading}
            error={error}
          />
        )}

        {loading && <p className="mt-6 text-center">Analyzing...</p>}

        {result && <ResultsPanel result={result} />}
      </div>
    </section>
  );
}
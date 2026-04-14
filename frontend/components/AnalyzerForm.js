"use client";

import { useState } from "react";
import { Upload, FileText } from "lucide-react";

export default function AnalyzerForm({
  resume,
  setResume,
  jobDescription,
  setJobDescription,
  handleAnalyze,
  loading,
  error,
}) {
  const [fileName, setFileName] = useState("");

  return (
    <section
      id="analyzer"
      className="mb-10 -mx-6 mt-5 bg-white px-6 py-12"
    >
      <div className="mx-auto max-w-3xl">
        <div className="text-center">
          <h2 className="text-sm font-bold text-[#1E293B] md:text-2xl">
            Resume Analyzer
          </h2>
          <p className="mt-2 text-xs text-[#64748B] md:text-base">
            Compare your resume against a job description.
          </p>
        </div>

        <div className="mt-5 flex flex-col items-center gap-8 sm:flex-row sm:justify-center sm:gap-12">
          
          {/* Upload Resume */}
          <div className="flex flex-col items-center">
            <label className="relative flex h-40 w-40 cursor-pointer flex-col items-center justify-center gap-3 rounded-[30px] border-2 border-dashed border-[#CBD5E1] bg-[#F8FAFC] text-center shadow-sm transition hover:border-[#94A3B8] hover:bg-white">

              <input
                type="file"
                accept=".pdf,.docx"
                onChange={(e) => {
                  const file = e.target.files?.[0] || null;
                  setResume(file);
                  setFileName(file ? file.name : "");
                }}
                className="hidden"
              />

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#E2E8F0] text-[#64748B]">
                <Upload size={18} strokeWidth={1.5} />
              </div>

              <span className="rounded-xl bg-[#64748B] px-3 py-1.5 text-xs font-semibold text-white">
                {fileName ? "File Chosen" : "Upload Resume"}
              </span>

              <p className="px-3 text-[10px] leading-tight text-[#64748B]">
                {fileName ? fileName : "PDF or DOCX only"}
              </p>

              <span className="rounded-md bg-[#EEF2F7] px-2 py-[3px] text-[9px] font-medium text-[#64748B]">
                Safe upload
              </span>
            </label>
          </div>

          {/* Job Description */}
          <div className="flex flex-col items-center">
            <div className="flex h-40 w-40 flex-col items-center justify-center gap-3 rounded-[30px] border-2 border-dashed border-[#CBD5E1] bg-[#F8FAFC] text-center shadow-sm transition hover:border-[#94A3B8] hover:bg-white">

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#E2E8F0] text-[#64748B]">
                <FileText size={18} strokeWidth={1.5} />
              </div>

              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Job description..."
                className="h-12 w-28 resize-none bg-transparent text-center text-xs text-[#1E293B] outline-none placeholder:text-[#9CA3AF]"
              />

              <p className="text-[10px] text-[#64748B]">
                Paste here
              </p>
            </div>
          </div>

        </div>

        <div className="mt-5 flex justify-center">
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="rounded-full bg-[#E2E8F0] px-12 py-4 text-sm font-semibold text-[#475569] shadow-[8px_8px_18px_rgba(148,163,184,0.35),-8px_-8px_18px_rgba(255,255,255,0.9)] transition hover:scale-[1.02] disabled:opacity-60"
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </div>

        {error && (
          <div className="mx-auto mt-6 max-w-md rounded-2xl border border-red-200 bg-red-50 p-3 text-center text-xs text-red-600">
            {error}
          </div>
        )}
      </div>
    </section>
  );
}
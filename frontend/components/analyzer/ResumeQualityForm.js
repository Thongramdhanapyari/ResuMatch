"use client";

import { useState } from "react";
import { Upload } from "lucide-react";

export default function ResumeQualityForm({
  resume,
  setResume,
  handleAnalyze,
  loading,
  error,
}) {
  const [fileName, setFileName] = useState("");

  return (
    <div className="w-full">
      <div className="w-full px-4 md:px-8">
        <div className="text-center">
          <h2 className="text-sm font-bold text-[#1E293B] md:text-2xl">
            Resume Analyzer
          </h2>

          <p className="mt-3 text-xs text-[#64748B] md:mt-4 md:text-base">
            Check ATS score, skills, spelling and formatting.
          </p>
        </div>

        <div className="mt-10 flex flex-col items-center justify-center">
          <div className="flex flex-col items-center">
            <label className="relative flex h-40 w-40 cursor-pointer flex-col items-center justify-center gap-3 rounded-[30px] border-2 border-dashed border-[#CBD5E1] bg-[#F8FAFC] text-center shadow-sm transition hover:border-[#94A3B8] hover:bg-white md:h-52 md:w-52 md:gap-4 md:rounded-[36px]">

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

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#E2E8F0] text-[#64748B] md:h-12 md:w-12">
                <Upload size={18} strokeWidth={1.5} />
              </div>

              <span className="rounded-xl bg-[#64748B] px-3 py-1.5 text-xs font-semibold text-white md:px-4 md:py-2 md:text-sm">
                {fileName ? "File Chosen" : "Upload Resume"}
              </span>

              <p className="px-3 text-[10px] leading-tight text-[#64748B] md:px-4 md:text-xs">
                {fileName ? fileName : "PDF or DOCX only"}
              </p>

              <span className="rounded-md bg-[#EEF2F7] px-2 py-[3px] text-[9px] font-medium text-[#64748B] md:px-3 md:py-1 md:text-[10px]">
                Safe upload
              </span>
            </label>
          </div>
        </div>

        <div className="mt-5 flex justify-center md:mt-8">
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="rounded-full bg-[#E2E8F0] px-12 py-4 text-sm font-semibold text-[#475569] shadow-[8px_8px_18px_rgba(148,163,184,0.35),-8px_-8px_18px_rgba(255,255,255,0.9)] transition hover:scale-[1.02] disabled:opacity-60 md:px-16 md:py-4 md:text-base"
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </div>

        {error && (
          <div className="mx-auto mt-6 max-w-md rounded-2xl border border-red-200 bg-red-50 p-3 text-center text-xs text-red-600 md:mt-8 md:max-w-lg md:text-sm">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
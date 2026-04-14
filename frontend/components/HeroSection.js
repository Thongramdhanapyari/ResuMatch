import { BarChart3, Search, Lightbulb } from "lucide-react";

export default function HeroSection() {
  return (
    <section className="grid gap-10 pt-10 pb-12 lg:grid-cols-2 lg:items-center -mt-5 ml-5">

      {/* LEFT SIDE */}
      <div className="max-w-xl">
        <span className="inline-flex rounded-full border border-[#D1D5DB] bg-[#F3F4F6] px-2 py-1.5 text-xs font-medium text-[#64748B] shadow-sm">
          AI-powered resume analysis
        </span>

        <h1 className="mt-4 text-sm font-semibold leading-tight text-[#1E293B] md:text-xl">
          Understand how your resume
          <span className="block text-[#64748B]">matches real jobs</span>
        </h1>

        <p className="mt-5 text-sm leading-5 text-[#64748B]">
          Upload your resume, paste a job description, and instantly get a match
          score, missing skills, and practical suggestions to improve your chances.
        </p>

        <div className="mt-7 flex flex-wrap gap-4">
          <a
            href="#analyzer"
            className="rounded-2xl bg-[#64748B] px-6 py-2.5 text-xs font-semibold text-white transition hover:bg-[#475569]"
          >
            Analyze Resume
          </a>

          <a
            href="#how-it-works"
            className="rounded-2xl border border-[#D1D5DB] px-6 py-2.5 text-xs font-semibold text-[#1E293B] transition hover:bg-[#F3F4F6]"
          >
            Learn More
          </a>
        </div>

        {/* 🔥 TIGHTENED FEATURE CARDS */}
        <div className="mt-8 grid gap-4 sm:grid-cols-3">
          <div className="flex items-start gap-2">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[#EEF2F7] text-[#64748B]">
              <BarChart3 size={16} />
            </div>
            <div>
              <h4 className="text-xs font-semibold text-[#1E293B] leading-4">
                Match Score
              </h4>
              <p className="text-[11px] text-[#64748B] leading-4">
                Resume fit instantly
              </p>
            </div>
          </div>

          <div className="flex items-start gap-2">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[#EEF2F7] text-[#64748B]">
              <Search size={16} />
            </div>
            <div>
              <h4 className="text-xs font-semibold text-[#1E293B] leading-4">
                Missing Skills
              </h4>
              <p className="text-[11px] text-[#64748B] leading-4">
                Detect gaps fast
              </p>
            </div>
          </div>

          <div className="flex items-start gap-2">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[#EEF2F7] text-[#64748B]">
              <Lightbulb size={16} />
            </div>
            <div>
              <h4 className="text-xs font-semibold text-[#1E293B] leading-4">
                Suggestions
              </h4>
              <p className="text-[11px] text-[#64748B] leading-4">
                Improve resume
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* RIGHT SIDE IMAGE */}
      <div className="relative flex justify-center lg:justify-end">

        {/* OUTER = glow (not clipped) */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="h-[420px] w-[420px] rounded-full bg-[#60A5FA]/40 blur-[120px]" />
        </div>

        {/*  INNER = FULL ROUNDED */}
        <div className="relative w-[260px] h-[260px] rounded-full bg-[#F8FAFC] overflow-hidden flex items-center justify-center shadow-lg mr-15 mt-10">
          
          <img
            src="/heroSection.png"
            alt="Resume Analysis"
            className="w-full h-full object-cover"
          />
          
        </div>
      </div>
    </section>
  );
}
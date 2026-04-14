export default function ResultsPanel({ result }) {
  if (!result) {
    return (
      <section className="flex min-h-[200px] flex-col items-center justify-center rounded-3xl border border-[#D1D5DB] bg-white shadow-lg p-4 md:p-6 mb-10 mt-10 text-center mx-4 md:mx-20">
        <h3 className="text-lg md:text-xl font-semibold text-[#1E293B]">Analysis Results</h3>
        <p className="mt-3 text-sm md:text-base text-[#64748B]">
          Your resume insights will appear here after analysis.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded-3xl border border-[#D1D5DB] bg-[#F3F4F6] p-3 md:p-8 shadow-lg mb-10 mt-10 mx-4 md:mx-0">
      <div className="space-y-6 md:space-y-8">
        <div className="rounded-2xl bg-[#64748B] p-6 md:p-7 text-white">
          <p className="text-xs md:text-sm font-medium text-[#E2E8F0]">Match Score</p>
          <div className="mt-3 flex items-end justify-between gap-4">
            <h3 className="text-xl md:text-2xl font-bold text-white">{result.match_score}%</h3>
            <span className="rounded-full bg-white/15 px-3 py-1 text-[11px] md:text-xs text-[#F8FAFC]">
              Resume vs Job Description
            </span>
          </div>

          <div className="mt-5 h-3 w-full overflow-hidden rounded-full bg-white/20">
            <div
              className="h-full rounded-full bg-[#E2E8F0]"
              style={{ width: `${Math.min(result.match_score, 100)}%` }}
            />
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2 md:gap-8">
          <div className="rounded-2xl border border-[#D1D5DB] bg-white p-5 md:p-6">
            <h3 className="text-sm md:text-base font-semibold text-[#1E293B]">Matched Skills</h3>
            <ol className="mt-4 space-y-1 text-[11px] md:text-sm text-[#334155] list-decimal ml-5">
              {result.matched_skills.length > 0 ? (
                result.matched_skills.map((skill, index) => (
                  <li key={index}>{skill}</li>
                ))
              ) : (
                <p className="text-xs md:text-sm text-[#64748B]">No matched skills found.</p>
              )}
            </ol>
          </div>

          <div className="rounded-2xl border border-[#D1D5DB] bg-white p-5 md:p-6">
            <h3 className="text-sm md:text-base font-semibold text-[#1E293B]">Missing Skills</h3>
            <ol className="mt-4 space-y-1 text-[11px] md:text-sm text-[#475569] list-decimal ml-5">
              {result.missing_skills.length > 0 ? (
                result.missing_skills.map((skill, index) => (
                  <li key={index}>{skill}</li>
                ))
              ) : (
                <p className="text-xs md:text-sm text-[#64748B]">No missing skills found.</p>
              )}
            </ol>
          </div>
        </div>

        <div className="rounded-2xl border border-[#D1D5DB] bg-white p-5 md:p-6">
          <h3 className="text-sm md:text-base font-semibold text-[#1E293B]">Suggestions</h3>
          <div className="mt-4 space-y-3">
            {result.suggestions.length > 0 ? (
              result.suggestions.map((item, index) => (
                <div
                  key={index}
                  className="rounded-xl bg-[#F8FAFC] p-4 text-xs md:text-sm text-[#334155]"
                >
                  {item}
                </div>
              ))
            ) : (
              <p className="text-sm md:text-base text-[#64748B]">No suggestions available.</p>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
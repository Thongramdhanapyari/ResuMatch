import jsPDF from "jspdf";

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

  const skillsScore = result.skills_score ?? 0;
  const contentScore = result.content_score ?? 0;
  const atsScore = result.ats_score ?? 0;

  const downloadPDF = () => {
    const doc = new jsPDF();

    doc.setFontSize(16);
    doc.text("Resume Analysis Report", 20, 20);

    doc.setFontSize(12);
    doc.text(`Match Score: ${result.match_score}%`, 20, 40);
    doc.text(`Skills Score: ${skillsScore}%`, 20, 50);
    doc.text(`Content Score: ${contentScore}%`, 20, 60);
    doc.text(`ATS Score: ${atsScore}%`, 20, 70);

    doc.text("Matched Skills:", 20, 90);
    (result.matched_skills || []).slice(0, 10).forEach((s, i) => {
      doc.text(`- ${s}`, 25, 100 + i * 6);
    });

    let y = 100 + (result.matched_skills?.length || 0) * 6 + 10;

    doc.text("Missing Skills:", 20, y);
    (result.missing_skills || []).slice(0, 10).forEach((s, i) => {
      doc.text(`- ${s}`, 25, y + 10 + i * 6);
    });

    y = y + 10 + (result.missing_skills?.length || 0) * 6 + 10;

    doc.text("Suggestions:", 20, y);
    (result.suggestions || []).slice(0, 10).forEach((s, i) => {
      doc.text(`- ${s}`, 25, y + 10 + i * 6);
    });

    doc.save("resume-analysis.pdf");
  };

  return (
    <section className="rounded-3xl border border-[#D1D5DB] bg-[#F3F4F6] p-3 md:p-8 shadow-lg mb-10 mt-10 mx-4 md:mx-0">
      <div className="space-y-6 md:space-y-8">

        <div className="rounded-2xl bg-[#64748B] p-6 md:p-7 text-white">
          <p className="text-xs md:text-sm font-medium text-[#E2E8F0]">Match Score</p>
          <div className="mt-3 flex items-end justify-between gap-4">
            <h3 className="text-xl md:text-2xl font-bold">{result.match_score}%</h3>
            <button
              onClick={downloadPDF}
              className="rounded-full bg-white/20 px-3 py-1 text-[11px] md:text-xs"
            >
              Download PDF
            </button>
          </div>

          <div className="mt-5 h-3 w-full rounded-full bg-white/20">
            <div
              className="h-full rounded-full bg-[#E2E8F0]"
              style={{ width: `${Math.min(result.match_score, 100)}%` }}
            />
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-xl bg-white p-4 text-center">
            <p className="text-xs text-[#64748B]">Skills Match</p>
            <h4 className="text-lg font-bold text-[#1E293B]">{skillsScore}%</h4>
          </div>

          <div className="rounded-xl bg-white p-4 text-center">
            <p className="text-xs text-[#64748B]">Content Quality</p>
            <h4 className="text-lg font-bold text-[#1E293B]">{contentScore}%</h4>
          </div>

          <div className="rounded-xl bg-white p-4 text-center">
            <p className="text-xs text-[#64748B]">ATS Score</p>
            <h4 className="text-lg font-bold text-[#1E293B]">{atsScore}%</h4>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2">

          <div className="rounded-2xl bg-white p-5">
            <h3 className="text-sm font-semibold text-[#1E293B]">Matched Skills</h3>
            <div className="mt-4 flex flex-wrap gap-2">
              {(result.matched_skills || []).length > 0 ? (
                result.matched_skills.map((skill, i) => (
                  <span
                    key={i}
                    className="rounded-full bg-green-100 px-3 py-1 text-xs text-green-700"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <p className="text-xs text-[#64748B]">No matched skills</p>
              )}
            </div>
          </div>

          <div className="rounded-2xl bg-white p-5">
            <h3 className="text-sm font-semibold text-[#1E293B]">Missing Skills</h3>
            <div className="mt-4 flex flex-wrap gap-2">
              {(result.missing_skills || []).length > 0 ? (
                result.missing_skills.map((skill, i) => (
                  <span
                    key={i}
                    className="rounded-full bg-red-100 px-3 py-1 text-xs text-red-700"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <p className="text-xs text-[#64748B]">No missing skills</p>
              )}
            </div>
          </div>
        </div>

        <div className="rounded-2xl bg-white p-5">
          <h3 className="text-sm font-semibold text-[#1E293B]">Suggestions</h3>
          <div className="mt-4 space-y-3">
            {(result.suggestions || []).length > 0 ? (
              result.suggestions.map((item, i) => (
                <div key={i} className="rounded-xl bg-[#F8FAFC] p-3 text-xs">
                  {item}
                </div>
              ))
            ) : (
              <p className="text-sm text-[#64748B]">No suggestions</p>
            )}
          </div>
        </div>

      </div>
    </section>
  );
}
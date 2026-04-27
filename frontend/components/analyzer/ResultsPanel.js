import jsPDF from "jspdf";

export default function ResultsPanel({ result }) {
  if (!result) return null;

  const breakdown = result.score_breakdown || {};
  const isQuality = result.analysis_type === "resume_quality";

  const mainTitle = isQuality ? "Resume Quality Score" : "Match Score";

  const parsedSections = result.parsed_sections || {};
  const sectionConfidence = result.section_confidence || {};

  const atsChecklist = isQuality
    ? {
        email: result.email_present ?? null,
        phone: result.phone_present ?? null,
        skills: parsedSections.skills ? true : false,
        education: parsedSections.education ? true : false,
        projects: parsedSections.projects ? true : false,
        experience: parsedSections.experience ? true : false,
      }
    : null;

  const scoreCards = isQuality
    ? [
        ["ATS Score", breakdown.ats_score ?? result.ats_score ?? 0],
        ["Semantic Strength", breakdown.semantic_strength ?? 0],
        ["Spelling Quality", breakdown.spelling_quality ?? 0],
        ["Content Quality", breakdown.content_quality ?? result.content_score ?? 0],
      ]
    : [
        ["Semantic Match", breakdown.semantic_match ?? 0],
        ["Skill Match", breakdown.skill_match ?? result.skills_score ?? 0],
        ["ATS Score", breakdown.ats_score ?? result.ats_score ?? 0],
        ["Experience Relevance", breakdown.experience_relevance ?? 0],
      ];

  const downloadPDF = () => {
    const doc = new jsPDF();

    doc.setFontSize(16);
    doc.text("Resume Analysis Report", 20, 20);

    doc.setFontSize(12);
    doc.text(`${mainTitle}: ${result.match_score}%`, 20, 40);

    let y = 55;

    scoreCards.forEach(([label, value]) => {
      doc.text(`${label}: ${value}%`, 20, y);
      y += 10;
    });

    y += 10;
    doc.text("Missing Skills / Sections:", 20, y);

    (result.missing_skills || []).slice(0, 10).forEach((s, i) => {
      doc.text(`- ${s}`, 25, y + 10 + i * 6);
    });

    y += 80;
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
          <p className="text-xs md:text-sm font-medium text-[#E2E8F0]">
            {mainTitle}
          </p>

          <div className="mt-3 flex items-end justify-between gap-4">
            <h3 className="text-xl md:text-2xl font-bold">
              {result.match_score}%
            </h3>

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
              style={{ width: `${Math.min(result.match_score || 0, 100)}%` }}
            />
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-4">
          {scoreCards.map(([label, value], i) => (
            <div key={i} className="rounded-xl bg-white p-4 text-center">
              <p className="text-xs text-[#64748B]">{label}</p>
              <h4 className="text-lg font-bold text-[#1E293B]">{value}%</h4>
            </div>
          ))}
        </div>

        {!isQuality && (
          <div className="grid gap-6 md:grid-cols-2">
            <div className="rounded-2xl bg-white p-5">
              <h3 className="text-sm font-semibold text-[#1E293B]">
                Matched Skills
              </h3>

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
              <h3 className="text-sm font-semibold text-[#1E293B]">
                Missing Skills
              </h3>

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
        )}

        {isQuality && (
          <div className="grid gap-6 md:grid-cols-2">
            <div className="rounded-2xl bg-white p-5">
              <h3 className="text-sm font-semibold text-[#1E293B]">
                ATS Checklist
              </h3>

              <div className="mt-4 space-y-2 text-sm">
                {atsChecklist &&
                  Object.entries(atsChecklist).map(([key, value], i) => (
                    <div key={i} className="flex justify-between">
                      <span className="text-[#475569] capitalize">{key}</span>
                      <span className={value ? "text-green-600" : "text-red-500"}>
                        {value ? "✔" : "✘"}
                      </span>
                    </div>
                  ))}
              </div>
            </div>

            <div className="rounded-2xl bg-white p-5">
              <h3 className="text-sm font-semibold text-[#1E293B]">
                Section Confidence
              </h3>

              <div className="mt-4 space-y-2 text-sm">
                {Object.keys(sectionConfidence).length > 0 ? (
                  Object.entries(sectionConfidence).map(([sec, val], i) => (
                    <div key={i} className="flex justify-between">
                      <span className="text-[#475569] capitalize">{sec}</span>
                      <span className="text-[#1E293B]">{val}%</span>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-[#64748B]">
                    No section data available
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

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
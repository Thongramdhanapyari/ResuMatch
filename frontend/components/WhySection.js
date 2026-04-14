export default function WhySection() {
  return (
    <section
      id="why"
      className="grid gap-6 py-4 md:grid-cols-2 items-start md:gap-8 md:py-8"
    >
      <div className="rounded-xl">
        <img
          src="/temp.png"
          alt="Why ResuMatch"
          className="h-full w-full object-cover rounded-xl"
        />
      </div>

      <div className="rounded-3xl border border-[#D1D5DB] bg-white p-8 md:p-12 shadow-sm">
        <h2 className="text-xl md:text-2xl font-bold text-[#1E293B]">
          Why this app matters
        </h2>

        <p className="mt-4 text-xs md:text-sm leading-5 md:leading-6 text-[#475569]">
          Many candidates apply with resumes that are not aligned with the actual role.
          This project helps users understand how well their resume matches a target job
          description and where they need improvement.
        </p>

        <p className="mt-4 text-xs md:text-sm leading-5 md:leading-6 text-[#475569]">
          Instead of guessing what to change, users get structured feedback on missing
          skills, matched terms, and practical ways to strengthen their application.
        </p>
      </div>

      <div className="rounded-3xl border border-[#D1D5DB] bg-white p-8 md:p-12 shadow-sm">
        <h3 className="text-xl md:text-2xl font-semibold text-[#1E293B]">
          Who it helps
        </h3>

        <ul className="mt-5 text-xs md:text-sm space-y-5 text-[#475569]">
          <li>Students applying for internships</li>
          <li>Job seekers targeting specific roles</li>
          <li>Candidates improving ATS relevance</li>
          <li>Anyone who wants clearer resume feedback</li>
        </ul>
      </div>

      <div className="p-4 md:p-8 mt-0">
        <img
          src="/how_will_benefit.png"
          alt="who itHelps"
          className="w-full h-auto"
        />
      </div>
    </section>
  );
}
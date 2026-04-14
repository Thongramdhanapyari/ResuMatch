export default function FeaturesSection() {
  const features = [
    {
      title: "Match Score",
      description: "See how closely your resume aligns with the job description.",
      image: "/matchScore.png",
    },
    {
      title: "Skill Gap Detection",
      description: "Quickly identify important skills missing from your resume.",
      image: "/skillGapDetection.png",
    },
    {
      title: "Actionable Suggestions",
      description: "Get practical recommendations to improve resume quality.",
      image: "/actionableSuggestion.png",
    },
    {
      title: "Simple Workflow",
      description: "Upload, paste, analyze, and improve in a few seconds.",
      image: "/stepsHowToWork.png",
    },
  ];

  return (
    <section id="features" className="pt-0 pb-6">
      
      {/* Heading */}
      <div className="mb-6 -mx-6 inline-block bg-[#64748B]/50 backdrop-blur text-black pl-10 py-3 pr-40
                      [clip-path:polygon(0_0,90%_0,100%_50%,90%_100%,0_100%)]">
        
        <h2 className="text-lg font-semibold">
          Features
        </h2>

        <p className="text-xs mt-1 opacity-90">
          Designed to make resume analysis simple, useful, and recruiter-focused
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 pt-8">
        {features.map((feature) => (
          <div
            key={feature.title}
            className="group overflow-hidden rounded-2xl border border-[#E2E8F0] bg-white shadow-sm transition duration-300 hover:shadow-md"
          >
            {/* IMAGE */}
            <div className="relative h-[110px] w-full overflow-hidden">
              <img
                src={feature.image}
                alt={feature.title}
                className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
              />

              <div className="absolute inset-0 bg-[#0F172A]/0 transition duration-500" />
            </div>

            {/* CONTENT */}
            <div className="px-4 py-4 text-center">
              <h3 className="text-[13px] font-semibold text-[#1E293B] transition duration-300 group-hover:text-black">
                {feature.title}
              </h3>

              <p className="mt-2 text-[11px] leading-4 text-[#475569] opacity-0 transition duration-500 group-hover:opacity-100 group-hover:text-slate-800">
                {feature.description}
              </p>
            </div>

            {/* BOTTOM LINE */}
            <div className="h-[2px] w-full bg-[#64748B]/30 transition-all duration-300 group-hover:bg-[#64748B]" />
          </div>
        ))}
      </div>

    </section>
  );
}
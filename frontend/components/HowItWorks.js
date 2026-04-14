export default function HowItWorks() {
  const steps = [
    {
      step: "01",
      title: "Upload Resume",
      description: "Upload your resume in PDF or DOCX format.",
    },
    {
      step: "02",
      title: "Paste Job Description",
      description: "Provide the role description you want to target.",
    },
    {
      step: "03",
      title: "Get Insights",
      description: "Receive a score, missing skills, and improvement suggestions.",
    },
  ];

  return (
    <section id="how-it-works" className="py-12 -mt-5">
      <div className="rounded-3xl border border-[#CBD5E1] bg-[#F3F4F6] p-8 shadow-lg">

        <h2 className="text-xl font-bold text-[#1E293B]">
          How it works
        </h2>

        <p className="mt-3 text-xs text-[#64748B]">
          A simple three-step workflow for resume optimization.
        </p>

        <div className="mt-8 grid gap-6 md:grid-cols-3">
          {steps.map((item) => (
            <div
              key={item.step}
              className="rounded-2xl border border-[#D1D5DB] bg-white p-6 shadow-md transition hover:scale-[1.02]"
            >
              <p className="text-xs font-bold text-[#64748B]">
                {item.step}
              </p>

              <h3 className="mt-3 text-sm font-semibold text-[#1E293B]">
                {item.title}
              </h3>

              <p className="mt-3 text-xs leading-7 text-[#475569]">
                {item.description}
              </p>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
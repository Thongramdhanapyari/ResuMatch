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
    <section id="how-it-works" className="py-12 -mt-5 md:py-16">
      <div className="rounded-3xl border border-[#CBD5E1] bg-[#F3F4F6] p-8 md:p-10 shadow-lg">

        <h2 className="text-xl md:text-2xl font-bold text-[#1E293B]">
          How it works
        </h2>

        <p className="mt-3 text-xs md:text-sm text-[#64748B]">
          A simple three-step workflow for resume optimization.
        </p>

        <div className="mt-8 grid gap-6 md:grid-cols-3 md:gap-8">
          {steps.map((item) => (
            <div
              key={item.step}
              className="rounded-2xl border border-[#D1D5DB] bg-white p-6 md:p-7 shadow-md transition hover:scale-[1.02]"
            >
              <p className="text-xs md:text-sm font-bold text-[#64748B]">
                {item.step}
              </p>

              <h3 className="mt-3 text-sm md:text-base font-semibold text-[#1E293B]">
                {item.title}
              </h3>

              <p className="mt-3 text-xs md:text-sm leading-7 md:leading-6 text-[#475569]">
                {item.description}
              </p>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
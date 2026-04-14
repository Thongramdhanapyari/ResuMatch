"use client";
import { useState } from "react";

export default function FAQSection() {
  const [openItems, setOpenItems] = useState({});

  const faqs = [
    {
      q: "What file formats are supported?",
      a: "You can upload PDF and DOCX files.",
    },
    {
      q: "How is the match score calculated?",
      a: "It compares your resume with the job description using skills and keywords.",
    },
    {
      q: "Is my resume stored permanently?",
      a: "No, your resume is not stored permanently.",
    },
    {
      q: "Can I use the same resume for different job roles?",
      a: "Yes, but customizing it gives better results.",
    },
  ];

  const toggleFAQ = (index) => {
    setOpenItems((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  return (
    <section id="faq" className="py-15 px-4 md:px-6 md:py-20">
      <div className="mx-auto max-w-3xl md:max-w-4xl rounded-3xl border border-[#D1D5DB] bg-[#F3F4F6] p-6 md:p-8 shadow-lg">
        <h2 className="text-xl md:text-2xl font-bold text-[#1E293B]">
          Frequently Asked Questions
        </h2>

        <div className="mt-3 space-y-2 md:mt-5 md:space-y-3">
          {faqs.map((faq, index) => {
            const isOpen = openItems[index];

            return (
              <div
                key={index}
                onClick={() => toggleFAQ(index)}
                className="cursor-pointer rounded-2xl border border-[#D1D5DB] bg-white p-4 md:p-5 text-[11px] md:text-sm text-[#475569] transition hover:bg-[#F9FAFB]"
              >
                <p className="font-medium text-[#1E293B] md:text-base">
                  {isOpen ? "−" : "+"} {faq.q}
                </p>

                <div
                  className={`overflow-hidden transition-all duration-300 ease-in-out ${
                    isOpen ? "mt-2 max-h-40 opacity-100" : "max-h-0 opacity-0"
                  }`}
                >
                  <p className="text-[#475569] md:text-sm">{faq.a}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
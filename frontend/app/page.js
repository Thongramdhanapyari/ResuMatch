"use client";

import { useState } from "react";
import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import AnalyzerForm from "../components/AnalyzerForm";
import ResultsPanel from "../components/ResultsPanel";
import WhySection from "../components/WhySection";
import FeaturesSection from "../components/FeaturesSection";
import FAQSection from "../components/FAQSection";
import HowItWorks from "../components/HowItWorks";
import Footer from "../components/Footer";

export default function Home() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!resume) {
      setError("Please upload a resume.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
      setError("Please login first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("resume", resume);
      formData.append("job_description", jobDescription);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/analyze`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string" ? data.detail : "Something went wrong"
        );
      }

      setResult({
        match_score: data.match_score ?? 0,
        skills_score: data.skills_score ?? 0,
        content_score: data.content_score ?? 0,
        ats_score: data.ats_score ?? 0,
        matched_skills: Array.isArray(data.matched_skills) ? data.matched_skills : [],
        missing_skills: Array.isArray(data.missing_skills) ? data.missing_skills : [],
        suggestions: Array.isArray(data.suggestions) ? data.suggestions : [],
      });
    } catch (err) {
      setError(err.message || "Failed to analyze resume");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen overflow-x-hidden">
      <Navbar />

      <div className="mx-auto max-w-7xl px-6">
        <HeroSection />
      </div>
        <AnalyzerForm
          resume={resume}
          setResume={setResume}
          jobDescription={jobDescription}
          setJobDescription={setJobDescription}
          handleAnalyze={handleAnalyze}
          loading={loading}
          error={error}
          result={result}
        />
      <div className="mx-auto max-w-7xl px-6">
        <ResultsPanel result={result} />
        <WhySection />
        <FeaturesSection />
        <FAQSection />
        <HowItWorks />
      </div>

      <Footer />
    </main>
  );
}
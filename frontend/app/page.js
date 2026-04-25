"use client";

import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import AnalyzerPage from "../components/analyzer/AnalyzerPage";
import WhySection from "../components/WhySection";
import FeaturesSection from "../components/FeaturesSection";
import FAQSection from "../components/FAQSection";
import HowItWorks from "../components/HowItWorks";
import Footer from "../components/Footer";
import HistorySection from "../components/HistorySection";

export default function Home() {
  return (
    <main className="min-h-screen overflow-x-hidden">
      <Navbar />

      <div className="mx-auto max-w-7xl px-6">
        <HeroSection />
      </div>

      <AnalyzerPage />

      <div className="mx-auto max-w-7xl px-6">
        <HistorySection />
        <WhySection />
        <FeaturesSection />
        <FAQSection />
        <HowItWorks />
      </div>

      <Footer />
    </main>
  );
}
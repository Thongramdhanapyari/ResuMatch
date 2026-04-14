import "./globals.css";

export const metadata = {
  title: "AI Resume Analyzer",
  description: "Analyze resumes against job descriptions using AI-powered insights.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
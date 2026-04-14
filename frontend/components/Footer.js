export default function Footer() {
  return (
    <footer className="mt-12 border-t border-white/20 bg-[#64748B] backdrop-blur md:mt-16">
      <div className="mx-auto grid max-w-7xl gap-8 px-6 py-10 md:grid-cols-3 md:px-8 md:py-12">
        
        <div>
          <h3 className="text-xl md:text-2xl font-bold text-black">
            Resu<span className="text-[var(--accent)]">Match</span>
          </h3>

          <p className="mt-3 text-xs md:text-sm leading-5 md:leading-6 text-[#E2E8F0]">
            An AI-powered resume analyzer built to help users
            improve resume relevance for real job descriptions.
          </p>
        </div>

        <div>
          <h4 className="text-sm md:text-base font-semibold uppercase tracking-wide text-[#E2E8F0]">
            Navigation
          </h4>

          <ul className="mt-4 space-y-3 text-xs md:text-sm">
            <li>
              <a href="#why" className="text-[#E2E8F0] hover:text-white transition">
                Why
              </a>
            </li>
            <li>
              <a href="#features" className="text-[#E2E8F0] hover:text-white transition">
                Features
              </a>
            </li>
            <li>
              <a href="#faq" className="text-[#E2E8F0] hover:text-white transition">
                FAQ
              </a>
            </li>
            <li>
              <a href="#how-it-works" className="text-[#E2E8F0] hover:text-white transition">
                How it works
              </a>
            </li>
          </ul>
        </div>

        <div>
          <h4 className="text-sm md:text-base font-semibold uppercase tracking-wide text-[#E2E8F0]">
            Project
          </h4>

          <ul className="mt-4 space-y-3 text-xs md:text-sm text-[#E2E8F0]">
            <li>Built for portfolio and interview showcase</li>
            <li></li>
            <li></li>
          </ul>
        </div>

      </div>
    </footer>
  );
}
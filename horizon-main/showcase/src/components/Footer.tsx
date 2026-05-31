export default function Footer() {
  return (
    <footer className="border-t border-[var(--border-color)] bg-[var(--bg-tertiary)] py-12 px-6">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
        <div>
          <h2 className="text-2xl font-bold font-['Space_Grotesk'] text-white">Horizon</h2>
          <p className="text-sm text-[var(--text-secondary)] mt-1">AI Recruiter Copilot Showcase</p>
        </div>
        
        <div className="text-sm text-[var(--text-tertiary)] flex flex-col md:flex-row gap-4 items-center">
          <span>Best Idea Award — Composio Hackathon</span>
          <span className="hidden md:inline">•</span>
          <a href="https://github.com/AshParmar/horizon" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
            GitHub Repository
          </a>
        </div>
      </div>
    </footer>
  );
}

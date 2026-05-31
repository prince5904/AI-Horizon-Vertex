"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, Code } from "lucide-react";

const navLinks = [
  { id: "hero", label: "Overview" },
  { id: "pipeline", label: "Architecture" },
  { id: "demo", label: "Live Demo" },
  { id: "integrations", label: "Integrations" },
];

export default function Navbar() {
  const [activeSection, setActiveSection] = useState("hero");
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      // Check if scrolled down for blur effect
      setIsScrolled(window.scrollY > 20);

      // Section tracking
      const sections = navLinks.map(link => document.getElementById(link.id));
      const scrollPosition = window.scrollY + 150; // offset

      for (let i = sections.length - 1; i >= 0; i--) {
        const section = sections[i];
        if (section && section.offsetTop <= scrollPosition) {
          setActiveSection(navLinks[i].id);
          break;
        }
      }
    };

    window.addEventListener("scroll", handleScroll);
    handleScroll(); // Initial check
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollTo = (id: string) => {
    setIsMobileMenuOpen(false);
    
    // special case for hero which doesn't have an ID assigned
    if (id === "hero") {
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }

    const element = document.getElementById(id);
    if (element) {
      window.scrollTo({
        top: element.offsetTop - 80, // Offset for navbar height
        behavior: "smooth"
      });
    }
  };

  return (
    <>
      <header
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          isScrolled
            ? "py-3 bg-black/60 backdrop-blur-xl border-b border-[var(--border-color)] shadow-xl"
            : "py-5 bg-transparent"
        }`}
      >
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
          
          {/* Logo */}
          <div 
            className="flex items-center gap-2 cursor-pointer group"
            onClick={() => scrollTo("hero")}
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[var(--accent-primary)] to-[var(--accent-secondary)] flex items-center justify-center font-bold text-white shadow-lg group-hover:scale-105 transition-transform">
              H
            </div>
            <span className="font-['Space_Grotesk'] font-bold text-xl tracking-tight hidden sm:block">
              Horizon
            </span>
          </div>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1 p-1 rounded-full border border-[var(--border-color)] bg-black/30 backdrop-blur-md">
            {navLinks.map((link) => (
              <button
                key={link.id}
                onClick={() => scrollTo(link.id)}
                className={`relative px-5 py-2 text-sm font-medium transition-colors rounded-full ${
                  activeSection === link.id
                    ? "text-white"
                    : "text-[var(--text-secondary)] hover:text-white"
                }`}
              >
                {activeSection === link.id && (
                  <motion.div
                    layoutId="active-nav-pill"
                    className="absolute inset-0 bg-white/10 border border-white/20 rounded-full"
                    transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                  />
                )}
                <span className="relative z-10">{link.label}</span>
              </button>
            ))}
          </nav>

          {/* Github Link / Mobile Toggle */}
          <div className="flex items-center gap-4">
            <a
              href="https://github.com/AshParmar/horizon"
              target="_blank"
              rel="noopener noreferrer"
              className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-full border border-[var(--border-color)] bg-white/5 hover:bg-white/10 transition-colors text-sm font-medium"
            >
              <Code className="w-4 h-4" />
              <span>GitHub</span>
            </a>
            
            {/* Mobile Menu Button */}
            <button 
              className="md:hidden p-2 text-white"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? <X /> : <Menu />}
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 z-40 bg-black/95 backdrop-blur-xl md:hidden pt-24 px-6 flex flex-col gap-6"
          >
            {navLinks.map((link) => (
              <button
                key={link.id}
                onClick={() => scrollTo(link.id)}
                className={`text-2xl font-bold text-left py-2 ${
                  activeSection === link.id ? "text-[var(--accent-primary)]" : "text-white"
                }`}
              >
                {link.label}
              </button>
            ))}
            <a
              href="https://github.com/AshParmar/horizon"
              target="_blank"
              rel="noopener noreferrer"
              className="mt-8 flex items-center gap-3 text-xl font-medium text-gray-400 py-4 border-t border-gray-800"
            >
              <Code /> GitHub Repository
            </a>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

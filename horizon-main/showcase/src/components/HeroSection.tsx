"use client";

import { motion } from "framer-motion";
import { Award, ArrowRight, Code } from "lucide-react";

export default function HeroSection() {
  return (
    <section id="hero" className="relative min-h-screen flex flex-col items-center justify-center pt-24 pb-16 px-6 overflow-hidden">
      {/* Background patterns */}
      <div className="absolute inset-0 bg-dot-pattern opacity-30 z-0"></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vw] h-[60vw] max-w-[800px] max-h-[800px] bg-blue-500/10 blur-[120px] rounded-full z-0 pointer-events-none"></div>

      <div className="relative z-10 w-full max-w-5xl mx-auto text-center flex flex-col items-center">
        
        {/* Award Badge */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8 inline-flex items-center gap-2 px-4 py-2 rounded-full glass-panel border border-yellow-500/30 bg-yellow-500/5 text-yellow-200 text-sm font-medium shadow-[0_0_15px_rgba(234,179,8,0.1)]"
        >
          <Award className="w-4 h-4 text-yellow-400" />
          <span>Best Idea Award Winner — Composio Agents in Production Hackathon</span>
        </motion.div>

        {/* Headline */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="space-y-6 mb-10"
        >
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-gradient">
            Horizon
          </h1>
          <h2 className="text-3xl md:text-5xl font-semibold text-gradient-accent pb-2">
            AI Recruiter Copilot
          </h2>
          <p className="max-w-2xl mx-auto text-lg md:text-xl text-[var(--text-secondary)]">
            An intelligent recruitment automation pipeline built with LangGraph & Composio. 
            From monitoring Gmail to scoring candidates and scheduling interviews.
          </p>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="flex flex-col sm:flex-row gap-4 mb-20"
        >
          <a href="#pipeline" className="group relative inline-flex items-center gap-2 px-8 py-3.5 bg-white text-black font-semibold rounded-lg hover:bg-gray-100 transition-colors">
            See How It Works
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </a>
          <a href="https://github.com/AshParmar/horizon" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-8 py-3.5 glass-panel text-white font-medium rounded-lg hover:bg-white/5 transition-colors">
            <Code className="w-5 h-5" />
            View Source
          </a>
        </motion.div>

        {/* Video Embed */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 30 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="w-full max-w-4xl mx-auto aspect-video rounded-xl glow-box glass-panel overflow-hidden p-2"
        >
          <div className="w-full h-full bg-black rounded-lg flex items-center justify-center relative overflow-hidden">
            <iframe 
              src="https://drive.google.com/file/d/16FhRULImue3iqeGql0NhtgweNcF57EfY/preview" 
              className="w-full h-full absolute inset-0"
              allow="autoplay"
              allowFullScreen
            ></iframe>
          </div>
        </motion.div>

      </div>
    </section>
  );
}

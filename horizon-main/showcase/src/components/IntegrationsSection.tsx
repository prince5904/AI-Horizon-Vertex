"use client";

import { motion } from "framer-motion";

const integrations = [
  { name: "Gmail", color: "text-red-500", desc: "Automated Resume Monitoring" },
  { name: "LinkedIn", color: "text-blue-500", desc: "API Data Enrichment" },
  { name: "Google Calendar", color: "text-blue-400", desc: "Interview Event Scheduling" },
  { name: "Google Sheets", color: "text-green-500", desc: "Structured Master Database" },
  { name: "Groq Llama 3.1", color: "text-orange-500", desc: "High-speed AI Scoring & Parsing" },
  { name: "LangGraph", color: "text-emerald-500", desc: "State Machine Orchestration" },
];

export default function IntegrationsSection() {
  return (
    <section id="integrations" className="py-24 px-6 bg-[var(--bg-primary)] border-t border-[var(--border-color)]">
      <div className="max-w-6xl mx-auto text-center">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">Powered by Composio & Groq</h2>
        <p className="text-[var(--text-secondary)] max-w-2xl mx-auto mb-16">
          Horizon connects directly to real-world applications using Composio's authenticated toolsets, ensuring secure and reliable automation.
        </p>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
          {integrations.map((tool, i) => (
            <motion.div
              key={tool.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="glass-panel p-6 rounded-xl hover:bg-white/5 transition-colors group cursor-pointer border-[var(--border-color)]"
            >
              <h3 className={`text-xl font-bold mb-2 ${tool.color} group-hover:scale-105 transition-transform`}>
                {tool.name}
              </h3>
              <p className="text-sm text-[var(--text-secondary)]">{tool.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

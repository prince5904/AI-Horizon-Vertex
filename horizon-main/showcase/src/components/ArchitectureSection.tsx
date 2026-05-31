"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Mail, FileText, Users, BrainCircuit, GitBranch, CalendarDays, TableProperties, FileSpreadsheet } from "lucide-react";

const nodes = [
  { id: 1, icon: Mail, label: "Gmail-Monitor", desc: "Auto-downloads incoming resumes", type: "standard" },
  { id: 2, icon: FileText, label: ".pdf extractor", desc: "PDF/TXT parsed to structured data", type: "standard" },
  { id: 3, icon: Users, label: "LinkedIn + LLM Enricher", desc: "LinkedIn API + Groq LLM fallback", type: "standard" },
  { id: 4, icon: BrainCircuit, label: "Profile Scorer", desc: "Groq evaluates vs job criteria", type: "standard" },
  { id: 5, icon: GitBranch, label: "Recruitment Agent", desc: "Evaluates condition: Score > 6.5", type: "decision" },
  { id: 6, icon: CalendarDays, label: "Scheduler", desc: "Creates Google Calendar events", type: "branch-yes" },
  { id: 7, icon: TableProperties, label: "G Sheet 1 (All Candidates)", desc: "Export to Database / JSON", type: "branch-no" },
  { id: 8, icon: FileSpreadsheet, label: "G Sheet 2 & G Calendar", desc: "Scheduled Interview output", type: "branch-yes" },
];

export default function ArchitectureSection() {
  const [xml, setXml] = useState("");

  useEffect(() => {
    // Fetch the draw.io XML data
    fetch("/architecture.drawio")
      .then((res) => res.text())
      .then((data) => {
        setXml(data);
        
        // Inject the draw.io viewer script only after the XML is ready
        if (!document.getElementById("drawio-viewer-script")) {
          const script = document.createElement("script");
          script.id = "drawio-viewer-script";
          script.src = "https://viewer.diagrams.net/js/viewer-static.min.js";
          script.type = "text/javascript";
          document.body.appendChild(script);
        } else {
          if (window.GraphViewer) {
            window.GraphViewer.processElements();
          }
        }
      });
  }, []);

  return (
    <section id="pipeline" className="py-24 px-6 relative border-t border-[var(--border-color)] bg-[var(--bg-secondary)]">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">System Architecture</h2>
          <p className="text-[var(--text-secondary)] max-w-2xl mx-auto">
            Powered by LangGraph, the pipeline executes an 8-node state machine with conditional routing, orchestrating 4 Composio toolsets and Groq LLM inference.
          </p>
        </div>

        {/* 1. High Level Animated Pipeline Visualization */}
        <div className="relative max-w-4xl mx-auto py-10 mb-24">
          <h3 className="text-xl font-bold mb-10 text-center text-[var(--accent-primary)]">1. LangGraph State Machine</h3>
          <div className="flex flex-col items-center gap-6 relative z-10">
            {/* Sequential Steps (1-4) */}
            {nodes.slice(0, 4).map((node, i) => (
              <motion.div
                key={node.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="node-connector flex flex-col items-center w-full max-w-md"
              >
                <div className="w-full glass-panel rounded-xl p-5 flex items-center gap-4 relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-r from-[var(--accent-primary)]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  <div className="w-12 h-12 rounded-lg bg-[var(--bg-tertiary)] flex items-center justify-center border border-[var(--border-highlight)] shrink-0 text-[var(--accent-primary)]">
                    <node.icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">{node.id}. {node.label}</h3>
                    <p className="text-sm text-[var(--text-secondary)]">{node.desc}</p>
                  </div>
                </div>
              </motion.div>
            ))}

            {/* Decision Node (5) */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.4 }}
              className="mt-6 node-connector flex flex-col items-center w-full max-w-md"
            >
              <div className="w-full relative glass-panel rounded-xl p-5 flex items-center justify-center border-yellow-500/30 bg-yellow-500/5">
                <div className="absolute -left-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-yellow-500/20 border border-yellow-500/50 rounded flex items-center justify-center rotate-45"></div>
                <div className="absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-yellow-500/20 border border-yellow-500/50 rounded flex items-center justify-center rotate-45"></div>
                
                <div className="text-center">
                  <GitBranch className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
                  <h3 className="font-semibold text-yellow-100">{nodes[4].label}</h3>
                  <p className="text-sm text-yellow-200/70">{nodes[4].desc}</p>
                </div>
              </div>
            </motion.div>

            {/* Branches Container */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full mt-12 relative">
              {/* Connecting SVG lines for branches */}
              <svg className="hidden md:block absolute -top-12 left-0 w-full h-12 pointer-events-none" preserveAspectRatio="none">
                <path d="M 50% 0 L 50% 20 L 25% 20 L 25% 48" fill="none" stroke="var(--accent-success)" strokeWidth="2" strokeDasharray="4 4" />
                <path d="M 50% 0 L 50% 20 L 75% 20 L 75% 48" fill="none" stroke="var(--text-tertiary)" strokeWidth="2" strokeDasharray="4 4" />
              </svg>

              {/* YES Branch */}
              <div className="flex flex-col gap-6">
                <div className="text-center font-mono text-sm text-[var(--accent-success)] mb-2 bg-[var(--accent-success)]/10 rounded-full py-1 px-3 w-max mx-auto border border-[var(--accent-success)]/20">
                  ✅ Score &gt; 6.5 (Shortlist)
                </div>
                {[nodes[5], nodes[7]].map((node, i) => (
                  <motion.div
                    key={node.id}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.5 + (i * 0.1) }}
                    className="w-full glass-panel rounded-xl p-5 flex items-center gap-4 border-[var(--accent-success)]/30 bg-[var(--accent-success)]/5"
                  >
                    <div className="w-10 h-10 rounded-lg bg-[var(--bg-tertiary)] flex items-center justify-center border border-[var(--border-highlight)] shrink-0 text-[var(--accent-success)]">
                      <node.icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-semibold">{node.id}. {node.label}</h3>
                      <p className="text-sm text-[var(--text-secondary)]">{node.desc}</p>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* NO Branch */}
              <div className="flex flex-col gap-6">
                <div className="text-center font-mono text-sm text-[var(--text-tertiary)] mb-2 bg-white/5 rounded-full py-1 px-3 w-max mx-auto border border-white/10">
                  ❌ Score &lt;= 6.5 (Reject)
                </div>
                {(() => {
                  const NodeIcon = nodes[6].icon;
                  return (
                    <motion.div
                      initial={{ opacity: 0, x: 20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.6 }}
                      className="w-full glass-panel rounded-xl p-5 flex items-center gap-4 opacity-70"
                    >
                      <div className="w-10 h-10 rounded-lg bg-[var(--bg-tertiary)] flex items-center justify-center border border-[var(--border-highlight)] shrink-0 text-[var(--text-secondary)]">
                        <NodeIcon className="w-5 h-5" />
                      </div>
                      <div>
                        <h3 className="font-semibold">{nodes[6].id}. {nodes[6].label}</h3>
                        <p className="text-sm text-[var(--text-secondary)]">{nodes[6].desc}</p>
                      </div>
                    </motion.div>
                  );
                })()}
                <div className="text-center mt-4 text-sm text-[var(--text-secondary)] italic">
                  * Skips scheduling, goes directly to DB export.
                </div>
              </div>

            </div>
          </div>
        </div>

        {/* 2. Detailed Interactive Draw.io Viewer */}
        <div className="relative pt-16 border-t border-[var(--border-color)]">
          <h3 className="text-xl font-bold mb-6 text-center text-white">2. Detailed Systems Diagram</h3>
          <p className="text-sm text-gray-400 text-center mb-10">
            Interactive system design. You can pan, zoom, and inspect the different components.
          </p>
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="relative w-full h-[550px] max-w-[780px] mx-auto rounded-xl overflow-hidden shadow-[0_0_40px_rgba(255,255,255,0.05)] border border-gray-800 group flex items-center justify-center bg-white"
          >
            {xml ? (
              // We force a white background so that the invert filter correctly flips it to pitch black with visible grid lines.
              <div 
                className="mxgraph w-full h-full" 
                style={{ backgroundColor: "#ffffff", filter: "invert(1) hue-rotate(180deg)" }}
                data-mxgraph={JSON.stringify({
                  highlight: "#3b82f6",
                  nav: false,
                  resize: true,
                  xml: xml
                })}
              ></div>
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400 font-mono text-sm">
                <div className="animate-pulse flex items-center gap-2">
                  <div className="w-4 h-4 rounded-full border-2 border-t-[var(--accent-primary)] animate-spin"></div>
                  Loading interactive diagram...
                </div>
              </div>
            )}
          </motion.div>
        </div>

      </div>
    </section>
  );
}

// Add TypeScript declaration for the global GraphViewer object injected by Draw.io
declare global {
  interface Window {
    GraphViewer?: {
      processElements: () => void;
    };
  }
}

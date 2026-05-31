"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Terminal, Play, CheckCircle2, XCircle, Calendar, Table } from "lucide-react";

const terminalLogs = [
  "Initializing AI Recruiter Pipeline...",
  "Loading Composio credentials...",
  "[STEP 1] Scanning Gmail for unread resumes...",
  "→ Found 6 emails with PDF attachments",
  "→ Downloaded 6 resumes to /incoming_resumes",
  "[STEP 2] Extracting PDF content & parsing via Groq...",
  "→ Extracted 6 candidate profiles",
  "[STEP 3] Enriching profiles with LinkedIn Data...",
  "→ Enriched 6 profiles (4 via Composio API, 2 via LLM fallback)",
  "[STEP 4] AI Scoring against 'Senior Software Engineer' criteria...",
  "→ Candidate A: 8.5/10 (Strong LangChain experience)",
  "→ Candidate B: 4.2/10 (Lacks required Python experience)",
  "[STEP 5] Decision Routing...",
  "→ 4 candidates shortlisted (Score >= 5.0)",
  "→ 2 candidates rejected",
  "[STEP 6] Scheduling Interviews via Google Calendar...",
  "→ Created 4 calendar events",
  "[STEP 7] Exporting Master Database to Google Sheets...",
  "→ Created 'AI_Recruiter_Database'",
  "[STEP 8] Exporting Interview Schedule...",
  "→ Created 'Interview Schedule' sheet",
  "✅ Pipeline execution finished with status: complete",
];

export default function DemoSection() {
  const [logs, setLogs] = useState<string[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [completed, setCompleted] = useState(false);

  const runDemo = () => {
    if (isRunning) return;
    setLogs([]);
    setIsRunning(true);
    setCompleted(false);

    let currentLog = 0;
    const interval = setInterval(() => {
      if (currentLog < terminalLogs.length) {
        setLogs(prev => [...prev, terminalLogs[currentLog]]);
        currentLog++;
      } else {
        clearInterval(interval);
        setIsRunning(false);
        setCompleted(true);
      }
    }, 400); // 400ms per line
  };

  return (
    <section id="demo" className="py-24 px-6 relative">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Pipeline Execution</h2>
          <p className="text-[var(--text-secondary)] max-w-2xl mx-auto">
            Watch the automated recruitment pipeline run in real-time, executing the complete process from email reading to scheduling.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Terminal Window */}
          <div className="glass-panel rounded-xl overflow-hidden flex flex-col h-[500px] border-[var(--border-color)]">
            {/* Terminal Header */}
            <div className="bg-[#1a1a1a] px-4 py-3 flex items-center justify-between border-b border-[#333]">
              <div className="flex items-center gap-2">
                <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                </div>
                <span className="ml-2 font-mono text-xs text-gray-400">powershell - python ai_recruiter_pipeline.py</span>
              </div>
              <button 
                onClick={runDemo}
                disabled={isRunning}
                className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-semibold transition-colors ${
                  isRunning ? "bg-gray-700 text-gray-400 cursor-not-allowed" : "bg-[var(--accent-primary)] hover:bg-blue-600 text-white"
                }`}
              >
                {isRunning ? (
                  <span className="animate-pulse">Running...</span>
                ) : (
                  <>
                    <Play className="w-3 h-3" /> Run Demo
                  </>
                )}
              </button>
            </div>

            {/* Terminal Body */}
            <div className="p-4 font-mono text-sm overflow-y-auto flex-1 bg-[#0a0a0a]">
              {!isRunning && logs.length === 0 && (
                <div className="text-gray-500 h-full flex flex-col items-center justify-center">
                  <Terminal className="w-12 h-12 mb-2 opacity-20" />
                  <p>Click "Run Demo" to start the pipeline simulation</p>
                </div>
              )}
              
              {logs.map((log, idx) => (
                <div 
                  key={idx} 
                  className={`mb-1.5 ${
                    log?.includes('✅') ? 'text-green-400' :
                    log?.includes('❌') ? 'text-red-400' :
                    log?.includes('→') ? 'text-blue-300 ml-4' :
                    log?.startsWith('[') ? 'text-purple-400 mt-3 font-semibold' :
                    'text-gray-300'
                  }`}
                >
                  {log}
                </div>
              ))}
              
              {isRunning && (
                <div className="animate-pulse w-2 h-4 bg-gray-400 mt-2"></div>
              )}
            </div>
          </div>

          {/* Results Display */}
          <div className="flex flex-col gap-6">
            <h3 className="text-xl font-semibold mb-2">Automated Outputs</h3>
            
            <div className={`glass-panel p-6 rounded-xl border-l-4 ${completed ? 'border-l-[var(--accent-success)]' : 'border-l-gray-700'} transition-colors duration-500`}>
              <div className="flex items-center gap-4 mb-4">
                <div className={`p-3 rounded-lg ${completed ? 'bg-green-500/10 text-green-400' : 'bg-gray-800 text-gray-500'}`}>
                  <Table className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-semibold text-lg">Master Candidate Database</h4>
                  <p className="text-sm text-[var(--text-secondary)]">Google Sheets Integration</p>
                </div>
              </div>
              <p className="text-sm text-[var(--text-tertiary)] bg-black/30 p-3 rounded-md font-mono line-clamp-2">
                {completed ? "https://docs.google.com/spreadsheets/d/1BxiMVs0X..." : "Waiting for pipeline execution..."}
              </p>
            </div>

            <div className={`glass-panel p-6 rounded-xl border-l-4 ${completed ? 'border-l-blue-500' : 'border-l-gray-700'} transition-colors duration-500`}>
              <div className="flex items-center gap-4 mb-4">
                <div className={`p-3 rounded-lg ${completed ? 'bg-blue-500/10 text-blue-400' : 'bg-gray-800 text-gray-500'}`}>
                  <Calendar className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-semibold text-lg">Interview Scheduling</h4>
                  <p className="text-sm text-[var(--text-secondary)]">Google Calendar Integration</p>
                </div>
              </div>
              <p className="text-sm text-[var(--text-tertiary)] bg-black/30 p-3 rounded-md font-mono line-clamp-2">
                {completed ? "4 Calendar invites sent successfully with Google Meet links attached." : "Waiting for pipeline execution..."}
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-auto">
              <div className="glass-panel p-4 rounded-xl text-center">
                <div className="text-3xl font-bold text-[var(--accent-success)]">{completed ? "4" : "-"}</div>
                <div className="text-sm text-[var(--text-secondary)] mt-1 flex items-center justify-center gap-1"><CheckCircle2 className="w-3 h-3"/> Shortlisted</div>
              </div>
              <div className="glass-panel p-4 rounded-xl text-center">
                <div className="text-3xl font-bold text-red-400">{completed ? "2" : "-"}</div>
                <div className="text-sm text-[var(--text-secondary)] mt-1 flex items-center justify-center gap-1"><XCircle className="w-3 h-3"/> Rejected</div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}

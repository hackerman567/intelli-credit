import { useState, useEffect, useRef } from 'react';
import { Activity, Database, Search, BrainCircuit, CheckCircle2, FileText, ShieldAlert, Cpu } from 'lucide-react';

const steps = [
  { id: 'extract', label: 'Financial Data Extraction', icon: Database },
  { id: 'validate', label: 'Financial Integrity Validation', icon: Search },
  { id: 'governance', label: 'Promoter Governance Analysis', icon: ShieldAlert },
  { id: 'liquidity', label: 'Liquidity Stress Evaluation', icon: Activity },
  { id: 'news', label: 'News & Reputation Scan', icon: FileText },
  { id: 'reasoning', label: 'AI Risk Calculation', icon: BrainCircuit },
  { id: 'report', label: 'Final Report Generation', icon: Cpu },
];

const terminalLogs = [
  "Initializing secure isolated environment...",
  "Extracting tables from financial documents...",
  "Normalizing revenue streams via AI model...",
  "Calculating debt-to-equity ratios...",
  "Connecting to financial databases for validation...",
  "Checking statutory filings and tax compliance...",
  "Scanning global news for company sentiment...",
  "Analyzing liquidity under stress scenarios...",
  "Detecting potential risk signals...",
  "Compiling final risk scorecard...",
  "Generating professional CAM report..."
];

export function AnalysisProgress() {
  const [currentStep, setCurrentStep] = useState(0);
  const [logs, setLogs] = useState<string[]>([]);
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Step progression
    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => Math.min(prev + 1, steps.length - 1));
    }, 1200);

    // Terminal log streaming
    let logIndex = 0;
    const logInterval = setInterval(() => {
      if (logIndex < terminalLogs.length) {
        setLogs(prev => [...prev, terminalLogs[logIndex]]);
        logIndex++;
      } else {
        clearInterval(logInterval);
      }
    }, 500);

    return () => {
      clearInterval(stepInterval);
      clearInterval(logInterval);
    };
  }, []);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  return (
    <div className="flex flex-col items-center justify-center w-full max-w-5xl mx-auto mt-8">
      <div className="text-center mb-16">
        <div 
          className="w-20 h-20 rounded-2xl bg-white border border-slate-200 flex items-center justify-center mx-auto mb-8 shadow-sm relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-slate-50" />
          <Activity className="w-8 h-8 text-corporate-blue relative z-10 animate-pulse" />
        </div>
        <h2 className="text-3xl md:text-4xl font-bold text-corporate-navy mb-4 tracking-tight">
          Automated Scrutiny <span className="text-corporate-blue">In Progress</span>
        </h2>
        <p className="text-corporate-muted text-base font-medium tracking-wide">The institutional engine is evaluating compliance and risk parameters.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 w-full">
        {/* Left: Step Nodes */}
        <div className="corporate-card p-10 relative overflow-hidden">
          <h3 className="text-xs font-bold text-corporate-muted uppercase tracking-widest mb-10 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-corporate-blue" />
            Assessment Workflow
          </h3>
          
          <div className="space-y-8 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px before:h-full before:w-[2px] before:bg-slate-100">
            {steps.map((step, index) => {
              const isActive = index === currentStep;
              const isPast = index < currentStep;
              const Icon = step.icon;

              return (
                <div key={step.id} className="relative flex items-center group">
                  <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 shrink-0 transition-all duration-500 z-10 ${
                    isPast ? 'bg-success border-success text-white' : 
                    isActive ? 'bg-white border-corporate-blue text-corporate-blue shadow-lg shadow-corporate-blue/20' : 
                    'bg-white border-slate-100 text-slate-300'
                  }`}>
                    {isPast ? <CheckCircle2 className="w-5 h-5" /> : <Icon className="w-4 h-4" />}
                  </div>
                  <div className={`ml-6 w-full p-4 rounded-xl border transition-all duration-500 ${
                    isActive ? 'bg-slate-50 border-corporate-blue/30 shadow-sm' : 
                    isPast ? 'bg-white border-slate-100 opacity-60' : 
                    'bg-transparent border-transparent opacity-40'
                  }`}>
                    <div className="flex items-center justify-between">
                      <h4 className={`font-bold text-sm tracking-wide ${isActive ? 'text-corporate-navy' : 'text-corporate-muted'}`}>{step.label}</h4>
                      {isActive && (
                        <span className="flex h-2 w-2 relative">
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-corporate-blue opacity-75"></span>
                          <span className="relative inline-flex rounded-full h-2 w-2 bg-corporate-blue"></span>
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Audit Log */}
        <div className="corporate-card p-1 flex flex-col h-[520px] overflow-hidden group border-slate-200">
          <div className="bg-white rounded-[1.4rem] flex-1 flex flex-col relative z-10 overflow-hidden">
            <div className="flex items-center gap-3 px-6 py-5 border-b border-slate-100 bg-slate-50/50">
              <span className="text-xs font-bold text-corporate-muted tracking-widest uppercase">Institutional Audit Trail</span>
            </div>
            
            <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4">
              {logs.map((log, i) => (
                <div
                  key={i}
                  className="flex items-start gap-3 animate-fade-in"
                >
                  <span className="text-corporate-blue font-bold shrink-0 mt-1">
                    <Activity className="w-3 h-3" />
                  </span>
                  <span className="text-corporate-text font-medium text-sm leading-relaxed">{log}</span>
                </div>
              ))}
              <div ref={logsEndRef} className="h-4" />
            </div>
            
            <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-white to-transparent pointer-events-none" />
          </div>
        </div>
      </div>
    </div>
  );
}

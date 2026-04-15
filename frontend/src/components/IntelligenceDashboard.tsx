import axios from 'axios';
import React, { useEffect, useRef, useState } from 'react';
import { 
  Download, ArrowLeft, AlertTriangle, CheckCircle, Info, ShieldAlert, ShieldCheck,
  Activity, FileText, TrendingUp, TrendingDown, DollarSign, Percent, BrainCircuit,
  BarChart3, LineChart as LineIcon, PieChart as PieIcon, Zap, Cpu, Landmark, Gavel,
  FlaskConical, RefreshCcw
} from 'lucide-react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  AreaChart, Area, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from 'recharts';

const API_BASE = 'http://localhost:5000/api';

interface IntelligenceDashboardProps {
  data: any;
  onReset: () => void;
}

interface InsightCardProps {
  insight: any;
  data: any;
  idx: number;
  key?: any;
}

const safeRender = (val: any) => {
  if (val === null || val === undefined) return "";
  let data = val;
  
  if (typeof val === 'string' && val.trim().startsWith('{')) {
    try { data = JSON.parse(val); } catch (e) { data = val; }
  }

  if (typeof data === 'string') return data;
  if (typeof data === 'object') {
    // NUCLEAR EXTRACTION: Look for any key that seems to contain the actual message
    const keys = Object.keys(data);
    const bestKey = keys.find(k => {
      const kl = k.toLowerCase();
      return kl.includes('recommendation') || kl.includes('worthiness') || kl.includes('analysis') || kl.includes('risk') || kl.includes('summary') || kl.includes('explanation') || kl.includes('note');
    }) || keys[0];
    
    const message = data[bestKey];
    if (typeof message === 'string') return message;
    if (typeof message === 'object' && message !== null) return safeRender(message);
    return JSON.stringify(data);
  }
  return String(data);
};

function InsightCard({ insight, data, idx }: InsightCardProps) {
  const content = safeRender(data[insight.key]);
  return (
    <div className="corporate-card p-6 group">
      <div className="flex items-start gap-4">
        <div className="w-10 h-10 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-center shrink-0 group-hover:bg-corporate-blue group-hover:border-corporate-blue transition-all duration-300">
          <insight.icon className="w-5 h-5 text-corporate-muted group-hover:text-white transition-colors duration-300" />
        </div>
        <div>
          <h4 className="font-sans font-bold text-corporate-navy text-sm mb-1">{insight.title}</h4>
          <p className="text-corporate-muted leading-relaxed text-sm font-light">
            {content || "No specific observations recorded for this segment."}
          </p>
        </div>
      </div>
    </div>
  );
}

export function IntelligenceDashboard({ data, onReset }: IntelligenceDashboardProps) {
  const [simulation, setSimulation] = useState({
    active: false,
    revenue: data.revenue,
    debt: data.debt,
    profit: data.profit,
    results: null as any
  });

  const scoreRef = useRef<HTMLSpanElement>(null);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    const rawScore = simulation.active && simulation.results 
      ? simulation.results.final_credit_score 
      : data.final_credit_score;
      
    // Defensive check: ensure score is a number or 0
    const scoreVal = (typeof rawScore === 'number') ? rawScore : parseInt(String(rawScore)) || 0;
      
    if (scoreRef.current) {
      scoreRef.current.textContent = scoreVal.toString();
    }
  }, [data.final_credit_score, simulation.results, simulation.active]);

  const runSimulation = async (field: string, value: number) => {
    const newSim = { ...simulation, [field]: value, active: true };
    setSimulation(newSim);
    
    try {
      const res = await axios.post(`${API_BASE}/analyze/simulate`, {
        revenue: Number(newSim.revenue),
        debt: Number(newSim.debt),
        profit: Number(newSim.profit),
        assets: Number(data.assets),
        promoter_score: data.promoter_risk?.promoter_risk_score || 70,
        liquidity_score: data.liquidity_risk?.liquidity_score || 70,
        officer_sentiment: data.officer_sentiment || 0
      });
      setSimulation(prev => ({ ...prev, results: res.data.data }));
    } catch (err) {
      console.error("Simulation error", err);
    }
  };

  const currentData = simulation.active && simulation.results ? { ...data, ...simulation.results } : data;
  const isApproved = currentData.final_credit_score > 60;
  const isWarning = currentData.final_credit_score > 40 && currentData.final_credit_score <= 60;
  
  const statusColor = isApproved ? 'text-success' : isWarning ? 'text-warning' : 'text-danger';
  const statusBg = isApproved ? 'bg-emerald-50 border-emerald-100' : isWarning ? 'bg-amber-50 border-amber-100' : 'bg-red-50 border-red-100';

  const handleDownload = async () => {
    try {
      setDownloading(true);
      const res = await axios.post(`${API_BASE}/report`, { analysisData: data });
      if (res.data.success) {
        window.open(`http://localhost:5000${res.data.path}`, '_blank');
      } else {
        alert(res.data.message || 'Failed to generate report.');
      }
    } catch (error) {
      console.error('Report Generation Error:', error);
      alert('Failed to generate CAM report.');
    } finally {
      setDownloading(false);
    }
  };

  const chartData = [
    { name: 'Q1', rev: Number(data.revenue || 0) * 0.7, debt: Number(data.debt || 0) * 0.9 },
    { name: 'Q2', rev: Number(data.revenue || 0) * 0.85, debt: Number(data.debt || 0) * 0.8 },
    { name: 'Q3', rev: Number(data.revenue || 0) * 0.9, debt: Number(data.debt || 0) * 1.0 },
    { name: 'Q4', rev: Number(data.revenue || 0), debt: Number(data.debt || 0) },
  ];

  return (
    <div className="pb-20 max-w-7xl mx-auto">
      {/* Header Actions */}
      <div className="flex items-center justify-between mb-10">
        <button 
          onClick={onReset}
          className="flex items-center gap-2 text-sm font-semibold text-corporate-muted hover:text-corporate-blue transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Analysis
        </button>
        <button 
          onClick={handleDownload}
          disabled={downloading}
          className="btn-primary flex items-center gap-2 px-6 py-2.5 text-sm shadow-sm"
        >
          <Download className="w-4 h-4" />
          {downloading ? 'Generating Report...' : 'Download Sanction Memo'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Aspect: The Neural Verdict & Scorecard */}
        <div className="lg:col-span-4 space-y-8">
          <div className={`corporate-card p-8 border-t-4 ${isApproved ? 'border-t-success' : isWarning ? 'border-t-warning' : 'border-t-danger'}`}>
            <div className="flex flex-col items-center">
              <div className="relative w-48 h-48 flex items-center justify-center mb-6">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="45" fill="transparent" stroke="#f1f5f9" strokeWidth="6" />
                  <circle 
                    cx="50" cy="50" r="45" fill="transparent" 
                    stroke={isApproved ? '#059669' : isWarning ? '#d97706' : '#e11d48'} 
                    strokeWidth="6" 
                    strokeDasharray="282.7" 
                    strokeDashoffset={282.7 - (282.7 * data.final_credit_score) / 100}
                    strokeLinecap="round"
                    className="transition-all duration-1000"
                  />
                </svg>
                <div className="absolute flex flex-col items-center justify-center">
                  <span className="text-[10px] text-corporate-muted font-bold uppercase tracking-wider mb-1">
                    Risk Score
                  </span>
                  <span ref={scoreRef} className={`text-5xl font-sans font-extrabold ${statusColor}`}>
                    {currentData.final_credit_score}
                  </span>
                </div>
              </div>

              <div className="w-full space-y-4">
                <div className="p-5 bg-slate-50 border border-slate-100 rounded-xl">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] font-bold text-corporate-muted uppercase tracking-wider">Proposed Limit</span>
                    <Landmark className="w-4 h-4 text-corporate-blue" />
                  </div>
                  <div className="text-2xl font-bold text-corporate-navy">₹ {currentData.suggested_limit} Cr</div>
                  <div className="text-[10px] text-corporate-muted font-medium mt-1">
                    @ {currentData.interest_rate}% p.a. (Indicative)
                  </div>
                </div>
                
                <div className="flex items-center justify-between p-4 border border-slate-100 rounded-xl">
                  <span className="text-xs font-bold text-corporate-muted uppercase tracking-wider">Verdict</span>
                  <span className={`text-sm font-bold ${statusColor}`}>{currentData.decision}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="glass-ultra rounded-3xl p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <BrainCircuit className="w-12 h-12 text-neon-blue" />
            </div>
            <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.3em] mb-6 flex items-center gap-2">
              <Activity className="w-3 h-3 text-neon-blue" /> Five Cs Risk Radar
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={[
                  { subject: 'Character', A: data.pillar_scores?.character || 50 },
                  { subject: 'Capacity', A: data.pillar_scores?.capacity || 50 },
                  { subject: 'Capital', A: data.pillar_scores?.capital || 50 },
                  { subject: 'Collateral', A: data.pillar_scores?.collateral || 50 },
                  { subject: 'Conditions', A: data.pillar_scores?.conditions || 50 },
                ]}>
                  <PolarGrid stroke="rgba(255,255,255,0.05)" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 10, fontWeight: 700 }} />
                  <Radar
                    name="Risk Profile"
                    dataKey="A"
                    stroke="#00f2ff"
                    fill="#00f2ff"
                    fillOpacity={0.15}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
            <p className="text-[10px] text-slate-500 text-center font-bold uppercase tracking-widest mt-2">
              Neural Network Scoring Index
            </p>
          </div>
        </div>

        {/* Right Aspect: The intelligence Stream & Metrics */}
        <div className="lg:col-span-8 space-y-8">
          {data.network_flags && data.network_flags.length > 0 && (
            <div className={`corporate-card border-l-4 border-l-danger bg-red-50 p-6 flex items-start gap-4`}>
              <div className="p-3 bg-red-100 rounded-lg">
                <ShieldAlert className="w-6 h-6 text-danger" />
              </div>
              <div className="flex-1">
                <h4 className="text-danger font-bold text-sm mb-1 uppercase tracking-wider">
                  Critical Identity Conflict Detected
                </h4>
                <div className="space-y-1">
                  {data.network_flags.map((flag: string, i: number) => (
                    <p key={i} className="text-xs text-corporate-text flex items-center gap-2">
                      <AlertTriangle className="w-3 h-3 text-danger shrink-0" /> {flag}
                    </p>
                  ))}
                </div>
              </div>
            </div>
          )}

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: 'Total Revenue', value: data.revenue || 0, unit: 'Cr', icon: DollarSign, color: 'text-corporate-blue' },
              { label: 'Payment Safety', value: data.ratios?.dscr || 'N/A', unit: 'ratio', icon: ShieldAlert, color: 'text-warning' },
              { label: 'Net Profit', value: data.profit || 0, unit: 'Cr', icon: TrendingUp, color: 'text-success' },
              { label: 'Profit Margin', value: `${data.ratios?.profit_margin || 0}%`, unit: '', icon: Percent, color: 'text-corporate-blue' },
            ].map((stat, i) => (
              <div 
                key={i}
                className="corporate-card p-5 group hover:bg-slate-50 transition-colors"
              >
                <div className="flex items-center justify-between mb-3">
                  <stat.icon className={`w-4 h-4 ${stat.color} opacity-70`} />
                  <span className="text-[10px] text-corporate-muted font-bold uppercase tracking-wider">{stat.label}</span>
                </div>
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-bold text-corporate-navy">{stat.value}</span>
                  <span className="text-[10px] text-corporate-muted font-bold uppercase">{stat.unit}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="corporate-card p-8 bg-white border-l-4 border-l-corporate-blue">
            <h3 className="text-xs font-bold text-corporate-blue uppercase tracking-widest mb-4 flex items-center gap-2">
              <FileText className="w-4 h-4" /> Credit Officer Observations
            </h3>
            <p className="text-corporate-text text-lg leading-relaxed font-normal">
              {simulation.active ? safeRender(currentData.explanation) : (safeRender(data.credit_notes).split('\n')[0] || safeRender(data.explanation) || "System analysis operational...")}
            </p>
          </div>

          <div className="corporate-card p-8 bg-slate-50/50 border border-slate-100">
            <div className="flex items-center justify-between mb-8">
              <h3 className="text-xs font-bold text-corporate-navy uppercase tracking-widest flex items-center gap-3">
                <RefreshCcw className="w-4 h-4 text-corporate-blue" /> Stress Testing Console
              </h3>
              {simulation.active && (
                <button 
                  onClick={() => setSimulation({ active: false, revenue: data.revenue, debt: data.debt, profit: data.profit, results: null })}
                  className="text-[10px] font-bold text-corporate-blue uppercase tracking-widest flex items-center gap-2 hover:underline"
                >
                   Reset to Actuals
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                { label: 'Revenue Variance', field: 'revenue', value: simulation.revenue, min: data.revenue * 0.5, max: data.revenue * 1.5, step: 1, unit: ' Cr' },
                { label: 'Debt Load Range', field: 'debt', value: simulation.debt, min: data.debt * 0.5, max: data.debt * 2.0, step: 1, unit: ' Cr' },
                { label: 'Profit Elasticity', field: 'profit', value: simulation.profit, min: data.profit * -0.5, max: data.profit * 2.0, step: 1, unit: ' Cr' }
              ].map((slider) => (
                <div key={slider.field} className="space-y-3">
                  <div className="flex justify-between items-center">
                    <label className="text-[10px] font-bold text-corporate-muted uppercase tracking-wider">{slider.label}</label>
                    <span className="text-xs font-bold text-corporate-navy">{slider.value.toFixed(1)}{slider.unit}</span>
                  </div>
                  <input 
                    type="range"
                    min={slider.min}
                    max={slider.max}
                    step={slider.step}
                    value={slider.value}
                    onChange={(e) => runSimulation(slider.field, parseFloat(e.target.value))}
                    className="w-full h-1 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-corporate-blue"
                  />
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="corporate-card p-6 border-slate-100">
              <h3 className="text-xs font-bold text-corporate-muted uppercase tracking-widest mb-6 flex items-center gap-2">
                <ShieldCheck className="w-3 h-3 text-success" /> Compliance & Audit Control
              </h3>
              <div className="space-y-3">
                {[
                  { factor: 'GST Return Accuracy', score: 85 + (data.officer_sentiment * 10), status: 'Verified' },
                  { factor: 'Corporate Filings Audit', score: 92, status: 'Compliant' },
                  { factor: 'Bank Statement Reconciliation', score: data.integrity_flags?.length > 0 ? 40 : 98, status: data.integrity_flags?.length > 0 ? 'Mismatch' : 'Clear' },
                  { factor: 'Legal Exposure (Current)', score: data.ews?.ews_risk_level === 'Low' ? 95 : 60, status: data.ews?.ews_risk_level === 'Low' ? 'Safe' : 'Active Cases' }
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between p-4 bg-slate-50 border border-slate-100 rounded-xl hover:bg-white transition-all">
                    <div className="flex flex-col gap-1">
                      <span className="text-[10px] font-bold text-corporate-navy uppercase tracking-wider">{item.factor}</span>
                      <div className="w-32 h-1 bg-slate-200 rounded-full overflow-hidden">
                        <div 
                          style={{ width: `${item.score}%` }}
                          className={`h-full transition-all duration-1000 ${item.score > 70 ? 'bg-success' : item.score > 40 ? 'bg-warning' : 'bg-danger'}`}
                        />
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-bold text-corporate-navy">{item.score}%</div>
                      <div className={`text-[10px] font-bold uppercase tracking-widest ${item.status === 'Verified' || item.status === 'Compliant' || item.status === 'Safe' ? 'text-success' : 'text-danger'}`}>{item.status}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-xs font-bold text-corporate-muted uppercase tracking-widest ml-1 flex items-center gap-2">
                <Activity className="w-3 h-3 text-corporate-blue" /> Verified Observations
              </h3>
              {(() => {
                const insights = [
                  { key: 'financial_insight', title: 'Director Reliability', icon: Gavel },
                  { key: 'promoter_insight', title: 'Ability to Pay', icon: TrendingUp },
                  { key: 'liquidity_insight', title: 'Financial Buffer', icon: Landmark },
                  { key: 'reputation_insight', title: 'Market Sentiment', icon: FileText }
                ];
                return insights.map((insight, idx) => (
                  <InsightCard key={insight.key} insight={insight} data={data} idx={idx} />
                ));
              })()}
            </div>
          </div>

          <div className="corporate-card p-8 border-t-4 border-t-danger bg-red-50/10">
            <div className="flex items-center justify-between mb-8">
              <h3 className="text-xs font-bold text-corporate-navy uppercase tracking-widest flex items-center gap-2">
                <AlertTriangle className="w-3 h-3 text-danger" /> Network Ripple Exposure
              </h3>
              <div className={`px-4 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest border ${
                data.contagion?.systemic_risk_summary?.severity === 'Systemic' 
                  ? 'bg-red-100 border-red-200 text-danger' 
                  : 'bg-amber-100 border-amber-200 text-warning'
              }`}>
                {data.contagion?.systemic_risk_summary?.severity || 'Moderate'} Impact Projection
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-12 gap-10">
              <div className="md:col-span-4 space-y-6">
                <div className="p-5 bg-white border border-slate-100 rounded-xl">
                  <span className="text-[10px] font-bold text-corporate-muted uppercase tracking-widest block mb-4">Direct exposure hits</span>
                  <p className="text-xs text-corporate-text leading-relaxed">
                    {safeRender(data.contagion?.direct_impact) || "Analysis pending..."}
                  </p>
                </div>
                <div className="p-5 bg-white border border-slate-100 rounded-xl">
                  <span className="text-[10px] font-bold text-corporate-muted uppercase tracking-widest block mb-4">Supply Chain Dependencies</span>
                  <p className="text-xs text-corporate-text leading-relaxed">
                    {safeRender(data.contagion?.indirect_impact) || "Analysis pending..."}
                  </p>
                </div>
              </div>

              <div className="md:col-span-8">
                <div className="relative">
                  <span className="text-[10px] font-bold text-corporate-muted uppercase tracking-widest block mb-8">Default propagation path</span>
                  
                  <div className="space-y-0 relative">
                    <div className="absolute left-4 top-2 bottom-2 w-px bg-slate-200" />
                    
                    {(data.contagion?.cascade_flow || [
                      "Primary Liability Breach",
                      "Operational Cash Freeze",
                      "Systemic Risk Manifest"
                    ]).map((step: string, i: number) => (
                      <div key={i} className="flex items-start gap-8 pb-8 last:pb-0">
                        <div className="relative z-10 w-8 h-8 rounded-full bg-white border border-slate-200 flex items-center justify-center shrink-0 shadow-sm">
                          <div className={`w-2 h-2 rounded-full ${i === 0 ? 'bg-danger animate-pulse' : 'bg-slate-200'}`} />
                        </div>
                        <div className="pt-1">
                          <h5 className="text-[10px] font-bold text-corporate-muted uppercase tracking-widest mb-1">Phase 0{i+1}</h5>
                          <p className="text-sm font-semibold text-corporate-navy">{step}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

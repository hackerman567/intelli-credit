import { useState, useEffect } from 'react';
import { UploadNexus } from './components/UploadNexus';
import { AnalysisProgress } from './components/AnalysisProgress';
import { IntelligenceDashboard } from './components/IntelligenceDashboard';
import { Shield, Activity, Cpu, Lock } from 'lucide-react';
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

export default function App() {
  const [appState, setAppState] = useState<'upload' | 'analyzing' | 'dashboard'>('upload');
  const [analysisData, setAnalysisData] = useState<any>(null);


  const handleUpload = async (file: File, details: { companyName: string, promoterName: string, officerNotes: string, sector: string }) => {
    try {
      setAppState('analyzing');

      // 1. Upload Document
      const formData = new FormData();
      formData.append('document', file);
      
      const uploadRes = await axios.post(`${API_BASE}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (!uploadRes.data.success) throw new Error('Upload failed');
      const filename = uploadRes.data.filename;

      // 2. Trigger Analysis (Phase 12: Integrated Narrative)
      const analysisRes = await axios.post(`${API_BASE}/analyze`, {
        filename,
        company_name: details.companyName,
        promoter_name: details.promoterName,
        officer_notes: details.officerNotes,
        sector: details.sector
      });

      if (analysisRes.data.success) {
        setAnalysisData(analysisRes.data.data);
        setAppState('dashboard');
      } else {
        throw new Error(analysisRes.data.message || 'Analysis failed');
      }

    } catch (error: any) {
      console.error('Integration Error:', error);
      alert(error.response?.data?.message || error.message || 'System error during appraisal');
      setAppState('upload');
    }
  };

  const handleReset = () => {
    setAppState('upload');
    setAnalysisData(null);
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] selection:bg-corporate-blue/10 selection:text-corporate-blue overflow-x-hidden">
      {/* Subtle Corporate Background Pattern */}
      <div className="corporate-bg" />

      {/* Corporate Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-slate-200 px-6 py-4 shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer" onClick={handleReset}>
            <div className="w-10 h-10 bg-corporate-blue rounded-lg flex items-center justify-center shadow-lg shadow-corporate-blue/20">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div className="flex flex-col">
              <h1 className="text-xl font-bold text-corporate-navy tracking-tight">
                Intelli<span className="text-corporate-blue">Credit</span>
              </h1>
              <span className="text-[10px] font-bold text-corporate-muted uppercase tracking-widest leading-none">
              </span>
            </div>
          </div>
          <div className="hidden md:flex items-center gap-6">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-50 rounded-lg border border-slate-100">
              <Lock className="w-3.5 h-3.5 text-corporate-muted" />
              <span className="text-xs font-semibold text-corporate-muted">Secure Environment</span>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Experience Layer */}
      <main className="relative z-10 pt-28 px-6">
        <div className="max-w-7xl mx-auto pb-20">
          {appState === 'upload' && (
            <UploadNexus onUpload={handleUpload} />
          )}

          {appState === 'analyzing' && (
            <AnalysisProgress />
          )}

          {appState === 'dashboard' && analysisData && (
            <IntelligenceDashboard data={analysisData} onReset={handleReset} />
          )}
        </div>
      </main>

      {/* Security Disclaimer */}
      <footer className="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-md border-t border-slate-100 py-3 px-6 z-40">
        <div className="max-w-7xl mx-auto flex items-center justify-between text-[10px] font-semibold text-corporate-muted uppercase tracking-widest">
          <span>&copy; 2026 Intelli-Credit Banking Corp</span>
          <div className="flex gap-6">
            <span className="flex items-center gap-1.5"><Shield className="w-3 h-3" /> Encrypted Analysis</span>
            <span className="flex items-center gap-1.5"><Activity className="w-3 h-3" /> Real-time Validation</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

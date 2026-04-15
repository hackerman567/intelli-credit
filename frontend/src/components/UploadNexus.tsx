import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, CheckCircle2, ArrowLeft, ChevronRight, Lock, Zap } from 'lucide-react';

interface UploadNexusProps {
  onUpload: (file: File, details: { companyName: string, promoterName: string, officerNotes: string, sector: string }) => void;
}

export function UploadNexus({ onUpload }: UploadNexusProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [showDetails, setShowDetails] = useState(false);
  const [companyName, setCompanyName] = useState('');
  const [promoterName, setPromoterName] = useState('');
  const [officerNotes, setOfficerNotes] = useState('');
  const [sector, setSector] = useState('Manufacturing');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setShowDetails(true);
    }
  };

  const handleInitiate = () => {
    if (selectedFile && companyName && promoterName) {
      onUpload(selectedFile, { companyName, promoterName, officerNotes, sector });
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="corporate-card overflow-hidden">
        <div className="bg-slate-50 border-b border-slate-100 p-8">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-white border border-slate-200 rounded-xl flex items-center justify-center shadow-sm">
              <UploadCloud className="w-6 h-6 text-corporate-blue" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-corporate-navy">New Assessment</h2>
              <p className="text-xs font-semibold text-corporate-muted uppercase tracking-widest">Credit Scrutiny Portal</p>
            </div>
          </div>
        </div>

        <div className="p-8">
          {!showDetails ? (
            <div className="text-center py-12">
              <div 
                className="w-20 h-20 bg-slate-50 border-2 border-dashed border-slate-200 rounded-2xl flex items-center justify-center mx-auto mb-6 cursor-pointer hover:bg-white hover:border-corporate-blue transition-all"
                onClick={() => fileInputRef.current?.click()}
              >
                <FileText className="w-8 h-8 text-corporate-muted" />
              </div>
              <h3 className="text-lg font-bold text-corporate-navy mb-2">Upload Financial Statement</h3>
              <p className="text-sm text-corporate-muted mb-8 max-w-sm mx-auto">Please select the audited balance sheet or P&L statement in PDF format to begin the underwriting process.</p>
              
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                className="hidden" 
                accept=".pdf"
              />

              <button 
                onClick={() => fileInputRef.current?.click()}
                className="btn-primary px-8 py-3 text-sm flex items-center gap-2 mx-auto"
              >
                <UploadCloud className="w-4 h-4" />
                Select PDF Document
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="flex items-center justify-between p-4 bg-emerald-50 border border-emerald-100 rounded-xl mb-8">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-5 h-5 text-success" />
                  <div>
                    <span className="text-xs font-bold text-success block">Document Uploaded</span>
                    <span className="text-[10px] font-medium text-emerald-800">{selectedFile?.name}</span>
                  </div>
                </div>
                <button 
                  onClick={() => { setSelectedFile(null); setShowDetails(false); }}
                  className="text-[10px] font-bold text-corporate-muted underline hover:text-danger"
                >
                  Change file
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-[10px] font-bold text-corporate-muted uppercase tracking-widest">Company Name</label>
                  <input 
                    type="text"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    placeholder="E.g. Tata Steel Ltd"
                    className="w-full bg-white border border-slate-200 rounded-lg px-4 py-3 text-sm text-corporate-navy focus:outline-none focus:border-corporate-blue transition-all"
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-[10px] font-bold text-corporate-muted uppercase tracking-widest">Lead Director</label>
                  <input 
                    type="text"
                    value={promoterName}
                    onChange={(e) => setPromoterName(e.target.value)}
                    placeholder="E.g. N. Chandrasekaran"
                    className="w-full bg-white border border-slate-200 rounded-lg px-4 py-3 text-sm text-corporate-navy focus:outline-none focus:border-corporate-blue transition-all"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-[10px] font-bold text-corporate-muted uppercase tracking-widest">Industry Sector</label>
                <div className="relative">
                  <select 
                    value={sector}
                    onChange={(e) => setSector(e.target.value)}
                    className="w-full bg-white border border-slate-200 rounded-lg px-4 py-3 text-sm text-corporate-navy focus:outline-none focus:border-corporate-blue transition-all appearance-none cursor-pointer"
                  >
                    <option value="Manufacturing">Manufacturing</option>
                    <option value="NBFC / Fintech">NBFC / Fintech</option>
                    <option value="Retail & Trade">Retail & Trade</option>
                    <option value="Infrastructure">Infrastructure</option>
                    <option value="Service Industry">Service Industry</option>
                  </select>
                  <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-corporate-muted rotate-90 pointer-events-none" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-[10px] font-bold text-corporate-muted uppercase tracking-widest">Officer Observations</label>
                <textarea 
                  value={officerNotes}
                  onChange={(e) => setOfficerNotes(e.target.value)}
                  placeholder="Record site visit observations, facility status, or key management discussion..."
                  className="w-full bg-white border border-slate-200 rounded-lg px-4 py-3 text-sm text-corporate-navy focus:outline-none focus:border-corporate-blue transition-all h-24 resize-none"
                />
              </div>

              <div className="pt-6 flex items-center justify-between border-t border-slate-100">
                <button 
                  onClick={() => { setSelectedFile(null); setShowDetails(false); setCompanyName(''); setPromoterName(''); setOfficerNotes(''); }}
                  className="text-[10px] font-bold text-corporate-muted uppercase tracking-widest hover:text-danger transition-colors"
                >
                  Clear Form
                </button>
                
                <button 
                  onClick={handleInitiate}
                  disabled={!companyName || !promoterName || !officerNotes}
                  className="btn-primary py-3 px-10 text-sm flex items-center gap-2"
                >
                  Evaluate Risk
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

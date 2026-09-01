import { Download } from 'lucide-react';
import { downloadResults } from '../api/client';

export function DownloadButtons({ jobId }: { jobId: string }) {
  return <div className="downloads">{(['csv', 'json', 'xlsx'] as const).map((format) => <button key={format} onClick={() => void downloadResults(jobId, format)} title={`Download ${format.toUpperCase()}`}><Download size={14} />{format.toUpperCase()}</button>)}</div>;
}

import { LoaderCircle, CircleCheck, CircleAlert } from 'lucide-react';
import type { JobStatus } from '../types/product';

export function JobStatusBanner({ job, error }: { job: JobStatus | null; error: string | null }) {
  if (error) return <div className="status-banner error"><CircleAlert size={18} />{error}</div>;
  if (!job) return <div className="status-banner idle"><span className="status-dot" />Ready for a fresh product scan</div>;
  if (job.status === 'done') return <div className="status-banner success"><CircleCheck size={18} />Scan complete. Results are ready below.</div>;
  return <div className="status-banner"><LoaderCircle className="spin" size={18} /><span>{job.status === 'pending' ? 'Queued' : 'Comparing retailer listings'} <strong>{job.progress}%</strong></span><div className="progress"><i style={{ width: `${job.progress}%` }} /></div></div>;
}

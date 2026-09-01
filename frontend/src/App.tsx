import { ScanLine, MapPin, Clock3 } from 'lucide-react';
import { ScrapeForm } from './components/ScrapeForm';
import { JobStatusBanner } from './components/JobStatusBanner';
import { ResultsTable } from './components/ResultsTable';
import { DownloadButtons } from './components/DownloadButtons';
import { useScrapeJob } from './hooks/useScrapeJob';
import './styles.css';

export default function App() {
  const { job, products, error, start } = useScrapeJob();
  return <main><header className="topbar"><div className="brand"><span className="brand-mark"><ScanLine size={19} /></span><span>retail<span>radar</span></span></div><div className="top-meta"><span><MapPin size={14} /> India markets</span><span><Clock3 size={14} /> Live workspace</span></div></header><section className="hero"><div className="hero-copy"><span className="eyebrow">Product intelligence / 01</span><h1>Know the shelf<br /><em>before you shop.</em></h1><p>Compare quick-commerce listings across Blinkit and BigBasket, by city and query, in one clean scan.</p></div><div className="control-panel"><div className="panel-label">New product scan</div><ScrapeForm loading={job?.status === 'pending' || job?.status === 'running'} onSubmit={(platform, city, query) => void start(platform, city, query)} /></div></section><section className="workspace"><JobStatusBanner job={job} error={error ?? job?.error ?? null} />{job?.status === 'done' && <div className="results-head"><span>Scan output</span><DownloadButtons jobId={job.job_id} /></div>}<ResultsTable products={products} /></section><footer>RETAIL RADAR <span>Assignment build · FastAPI + React</span></footer></main>;
}

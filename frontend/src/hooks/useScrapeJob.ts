import { useEffect, useState } from 'react';
import { createScrape, getJobStatus, getResults } from '../api/client';
import type { JobStatus, Platform, Product } from '../types/product';

export function useScrapeJob() {
  const [job, setJob] = useState<JobStatus | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!job || job.status === 'done' || job.status === 'failed') return;
    const deadline = window.setTimeout(() => setError('The retailer did not respond within 60 seconds. Try one platform at a time.'), 60000);
    const timer = window.setInterval(() => {
      getJobStatus(job.job_id).then(setJob).catch((reason: unknown) => setError(reason instanceof Error ? reason.message : 'Status request failed'));
    }, 1500);
    return () => { window.clearInterval(timer); window.clearTimeout(deadline); };
  }, [job]);

  useEffect(() => {
    if (job?.status !== 'done') return;
    getResults(job.job_id).then((result) => setProducts(result.items)).catch((reason: unknown) => setError(reason instanceof Error ? reason.message : 'Results request failed'));
  }, [job]);

  async function start(platform: Platform, city: string, query: string): Promise<void> {
    setError(null); setProducts([]); setJob(null);
    try { const created = await createScrape(platform, city, query); setJob({ job_id: created.job_id, status: 'pending', progress: 0, error: null }); }
    catch (reason: unknown) { setError(reason instanceof Error ? reason.message : 'Could not start scrape'); }
  }
  return { job, products, error, start };
}

import type { JobStatus, Platform, Results } from '../types/product';

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { headers: { 'Content-Type': 'application/json' }, ...options });
  if (!response.ok) {
    const body = await response.json().catch(() => null) as { detail?: string } | null;
    throw new Error(body?.detail ?? `Request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}

export function createScrape(platform: Platform, city: string, query: string): Promise<{ job_id: string }> {
  return request('/api/scrape', { method: 'POST', body: JSON.stringify({ platform, city, query }) });
}
export function getJobStatus(jobId: string): Promise<JobStatus> { return request(`/api/scrape/${jobId}/status`); }
export function getResults(jobId: string): Promise<Results> { return request(`/api/results/${jobId}`); }
export async function downloadResults(jobId: string, format: 'csv' | 'json' | 'xlsx'): Promise<void> {
  const response = await fetch(`${API_BASE}/api/results/${jobId}/download?format=${format}`);
  if (!response.ok) throw new Error('Download failed');
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a'); link.href = url; link.download = `products-${jobId}.${format}`; link.click();
  URL.revokeObjectURL(url);
}

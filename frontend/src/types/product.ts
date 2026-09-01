export type Platform = 'blinkit' | 'bigbasket' | 'both';
export type JobState = 'pending' | 'running' | 'done' | 'failed';

export interface Product {
  product_name: string;
  brand: string | null;
  selling_price: number | null;
  mrp: number | null;
  discount: number | null;
  availability: string | null;
  product_url: string | null;
  category: string | null;
  subcategory: string | null;
  pack_size: string | null;
  platform: string;
  city: string;
  scraped_at: string;
}

export interface JobStatus { job_id: string; status: JobState; progress: number; error: string | null; }
export interface Results { items: Product[]; page: number; page_size: number; total: number; }

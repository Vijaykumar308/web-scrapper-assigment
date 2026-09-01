import { Search } from 'lucide-react';
import type { Platform } from '../types/product';

interface Props { loading: boolean; onSubmit: (platform: Platform, city: string, query: string) => void; }

export function ScrapeForm({ loading, onSubmit }: Props) {
  function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); const data = new FormData(event.currentTarget);
    onSubmit(data.get('platform') as Platform, String(data.get('city')), String(data.get('query')));
  }
  return <form className="scrape-form" onSubmit={submit}>
    <label>Search products<input name="query" placeholder="e.g. basmati rice" required /></label>
    <label>Delivery city<select name="city" defaultValue="Gurgaon"><option>Gurgaon</option><option>Mumbai</option><option>Delhi</option><option>Bengaluru</option><option>Hyderabad</option><option>Pune</option><option>Chennai</option><option>Kolkata</option></select></label>
    <label>Sources<select name="platform" defaultValue="both"><option value="both">Both platforms</option><option value="blinkit">Blinkit</option><option value="bigbasket">BigBasket</option></select></label>
    <button className="primary-button" disabled={loading} type="submit"><Search size={17} />{loading ? 'Running...' : 'Run scrape'}</button>
  </form>;
}

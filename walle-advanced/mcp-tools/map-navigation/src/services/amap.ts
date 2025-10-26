import axios from 'axios';
import { logger } from '../utils/logger.js';
import type { Location } from './baidu_map.js';

export function generateNavigationUrl(origin: string, destination: string): string {
  const baseUrl = 'https://www.amap.com/dir';
  const params = new URLSearchParams({
    from: origin,
    to: destination,
  });

  return `${baseUrl}?${params.toString()}`;
}

export function generateSearchUrl(query: string, city?: string): string {
  const baseUrl = 'https://www.amap.com/search';
  const params = new URLSearchParams({
    query: query,
  });

  if (city) {
    params.append('city', city);
  }

  return `${baseUrl}?${params.toString()}`;
}

export async function searchLocation(query: string, apiKey?: string, city?: string): Promise<Location[]> {
  if (!apiKey) {
    logger.warn('Amap API key not configured, returning mock data');
    return [
      {
        name: query,
        address: `${city || ''}`,
        location: { lat: 0, lng: 0 },
      },
    ];
  }

  try {
    const params: any = {
      keywords: query,
      output: 'json',
      key: apiKey,
    };

    if (city) {
      params.city = city;
    }

    const response = await axios.get('https://restapi.amap.com/v3/place/text', {
      params,
    });

    if (response.data.status === '1' && response.data.pois) {
      return response.data.pois.map((poi: any) => ({
        name: poi.name,
        address: poi.address,
        location: {
          lat: parseFloat(poi.location.split(',')[1]),
          lng: parseFloat(poi.location.split(',')[0]),
        },
      }));
    }

    logger.warn('Amap API returned no results', { query, city });
    return [];
  } catch (error) {
    logger.error('Failed to search location via Amap API', { error, query, city });
    return [];
  }
}

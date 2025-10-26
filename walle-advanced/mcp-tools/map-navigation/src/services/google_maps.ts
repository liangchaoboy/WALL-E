import axios from 'axios';
import { logger } from '../utils/logger.js';
import type { Location } from './baidu_map.js';

export function generateNavigationUrl(origin: string, destination: string, mode: string = 'transit'): string {
  const baseUrl = 'https://www.google.com/maps/dir/';
  const params = new URLSearchParams({
    api: '1',
    origin: origin,
    destination: destination,
    travelmode: mode,
  });

  return `${baseUrl}?${params.toString()}`;
}

export function generateSearchUrl(query: string): string {
  const baseUrl = 'https://www.google.com/maps/search/';
  return `${baseUrl}${encodeURIComponent(query)}`;
}

export async function searchLocation(query: string, apiKey?: string): Promise<Location[]> {
  if (!apiKey) {
    logger.warn('Google Maps API key not configured, returning mock data');
    return [
      {
        name: query,
        address: '',
        location: { lat: 0, lng: 0 },
      },
    ];
  }

  try {
    const params = {
      query: query,
      key: apiKey,
    };

    const response = await axios.get('https://maps.googleapis.com/maps/api/place/textsearch/json', {
      params,
    });

    if (response.data.status === 'OK' && response.data.results) {
      return response.data.results.map((result: any) => ({
        name: result.name,
        address: result.formatted_address,
        location: {
          lat: result.geometry.location.lat,
          lng: result.geometry.location.lng,
        },
      }));
    }

    logger.warn('Google Maps API returned no results', { query });
    return [];
  } catch (error) {
    logger.error('Failed to search location via Google Maps API', { error, query });
    return [];
  }
}

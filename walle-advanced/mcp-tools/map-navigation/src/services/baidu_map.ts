import axios from 'axios';
import { logger } from '../utils/logger.js';

export interface Location {
  name: string;
  address: string;
  location: {
    lat: number;
    lng: number;
  };
}

function extractCityName(address: string): string {
  const cities = [
    '北京', '上海', '天津', '重庆',
    '广州', '深圳', '杭州', '成都', '西安', '南京',
    '武汉', '苏州', '郑州', '长沙', '济南', '青岛',
    '沈阳', '大连', '哈尔滨', '长春', '福州', '厦门',
    '昆明', '兰州', '乌鲁木齐', '石家庄', '太原',
  ];

  for (const city of cities) {
    if (address.startsWith(city)) {
      return city;
    }
  }

  if (address.length <= 4) {
    return address;
  }

  return '全国';
}

export function generateNavigationUrl(origin: string, destination: string, mode: string = 'transit'): string {
  const baseUrl = 'https://map.baidu.com/direction';
  const params = new URLSearchParams({
    origin: origin,
    destination: destination,
    mode: mode,
    region: extractCityName(destination),
    output: 'html',
    src: 'webapp.walle.navigation',
  });

  return `${baseUrl}?${params.toString()}`;
}

export function generateSearchUrl(query: string, city?: string): string {
  const baseUrl = 'https://map.baidu.com/';
  const params = new URLSearchParams({
    query: query,
  });

  if (city) {
    params.append('c', city);
  }

  return `${baseUrl}?${params.toString()}`;
}

export async function searchLocation(query: string, apiKey?: string, city?: string): Promise<Location[]> {
  if (!apiKey) {
    logger.warn('Baidu Maps API key not configured, returning mock data');
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
      query: query,
      output: 'json',
      ak: apiKey,
    };

    if (city) {
      params.region = city;
    }

    const response = await axios.get('https://api.map.baidu.com/place/v2/search', {
      params,
    });

    if (response.data.status === 0 && response.data.results) {
      return response.data.results.map((result: any) => ({
        name: result.name,
        address: result.address,
        location: {
          lat: result.location.lat,
          lng: result.location.lng,
        },
      }));
    }

    logger.warn('Baidu Maps API returned no results', { query, city });
    return [];
  } catch (error) {
    logger.error('Failed to search location via Baidu Maps API', { error, query, city });
    return [];
  }
}

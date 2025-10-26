import { openInBrowser } from '../utils/browser.js';
import { logger } from '../utils/logger.js';
import config from '../config.js';
import * as baiduMap from '../services/baidu_map.js';
import * as amap from '../services/amap.js';
import * as googleMaps from '../services/google_maps.js';
import type { Location } from '../services/baidu_map.js';

export interface SearchLocationParams {
  query: string;
  city?: string;
  mapService?: 'baidu' | 'amap' | 'google';
}

export interface SearchLocationResult {
  success: boolean;
  message?: string;
  results?: Location[];
  url?: string;
}

export async function searchLocation(params: SearchLocationParams): Promise<SearchLocationResult> {
  const { query, city, mapService = 'baidu' } = params;

  if (!query || !query.trim()) {
    return {
      success: false,
      message: '错误: 搜索关键词不能为空',
    };
  }

  const trimmedQuery = query.trim();

  logger.info('Searching location', { query: trimmedQuery, city, mapService });

  let url: string;
  let mapName: string;
  let results: Location[] = [];

  const apiKey = config.apiKeys?.[mapService];

  switch (mapService) {
    case 'amap':
      url = amap.generateSearchUrl(trimmedQuery, city);
      mapName = '高德地图';
      if (apiKey) {
        results = await amap.searchLocation(trimmedQuery, apiKey, city);
      }
      break;
    case 'google':
      url = googleMaps.generateSearchUrl(trimmedQuery);
      mapName = 'Google Maps';
      if (apiKey) {
        results = await googleMaps.searchLocation(trimmedQuery, apiKey);
      }
      break;
    case 'baidu':
    default:
      url = baiduMap.generateSearchUrl(trimmedQuery, city);
      mapName = '百度地图';
      if (apiKey) {
        results = await baiduMap.searchLocation(trimmedQuery, apiKey, city);
      }
      break;
  }

  const opened = await openInBrowser(url);

  if (!opened) {
    return {
      success: false,
      message: '打开浏览器失败',
      url,
      results,
    };
  }

  let message = `✅ 已在${mapName}搜索: ${trimmedQuery}\n🔗 ${url}`;

  if (results.length > 0) {
    message += '\n\n📍 搜索结果:';
    results.slice(0, 3).forEach((result, index) => {
      message += `\n${index + 1}. ${result.name}`;
      if (result.address) {
        message += ` - ${result.address}`;
      }
    });

    if (results.length > 3) {
      message += `\n... 还有 ${results.length - 3} 个结果`;
    }
  }

  return {
    success: true,
    message,
    results,
    url,
  };
}

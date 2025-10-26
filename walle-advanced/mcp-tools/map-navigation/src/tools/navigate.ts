import { openInBrowser } from '../utils/browser.js';
import { logger } from '../utils/logger.js';
import * as baiduMap from '../services/baidu_map.js';
import * as amap from '../services/amap.js';
import * as googleMaps from '../services/google_maps.js';

export interface NavigateParams {
  origin: string;
  destination: string;
  mode?: 'driving' | 'transit' | 'walking';
  mapService?: 'baidu' | 'amap' | 'google';
}

export interface NavigateResult {
  success: boolean;
  message: string;
  url?: string;
}

export async function navigate(params: NavigateParams): Promise<NavigateResult> {
  const { origin, destination, mode = 'transit', mapService = 'baidu' } = params;

  if (!origin || !origin.trim()) {
    return {
      success: false,
      message: '错误: 起点不能为空',
    };
  }

  if (!destination || !destination.trim()) {
    return {
      success: false,
      message: '错误: 终点不能为空',
    };
  }

  const trimmedOrigin = origin.trim();
  const trimmedDestination = destination.trim();

  logger.info('Generating navigation URL', {
    origin: trimmedOrigin,
    destination: trimmedDestination,
    mode,
    mapService,
  });

  let url: string;
  let mapName: string;

  switch (mapService) {
    case 'amap':
      url = amap.generateNavigationUrl(trimmedOrigin, trimmedDestination);
      mapName = '高德地图';
      break;
    case 'google':
      url = googleMaps.generateNavigationUrl(trimmedOrigin, trimmedDestination, mode);
      mapName = 'Google Maps';
      break;
    case 'baidu':
    default:
      url = baiduMap.generateNavigationUrl(trimmedOrigin, trimmedDestination, mode);
      mapName = '百度地图';
      break;
  }

  const opened = await openInBrowser(url);

  if (!opened) {
    return {
      success: false,
      message: '打开浏览器失败',
      url,
    };
  }

  const modeText = mode === 'driving' ? '驾车' : mode === 'walking' ? '步行' : '公交';

  return {
    success: true,
    message: `✅ 成功打开 ${mapName}\n\n📍 起点：${trimmedOrigin}\n📍 终点：${trimmedDestination}\n🚗 方式：${modeText}\n🔗 导航链接：${url}\n\n地图应用已在浏览器中打开，正在准备导航...`,
    url,
  };
}

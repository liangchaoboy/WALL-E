import axios from 'axios';
import { logger } from '../utils/logger.js';

export interface CurrentLocation {
  city: string;
  province: string;
  country: string;
  location?: {
    lat: number;
    lng: number;
  };
  ip?: string;
}

export interface GetCurrentLocationResult {
  success: boolean;
  message?: string;
  location?: CurrentLocation;
}

export async function getCurrentLocation(): Promise<GetCurrentLocationResult> {
  try {
    logger.info('Getting current location via IP');

    const response = await axios.get('http://ip-api.com/json/', {
      params: {
        fields: 'status,country,regionName,city,lat,lon,query',
      },
      timeout: 5000,
    });

    if (response.data.status === 'success') {
      const location: CurrentLocation = {
        city: response.data.city || '未知',
        province: response.data.regionName || '未知',
        country: response.data.country || '未知',
        location: {
          lat: response.data.lat,
          lng: response.data.lon,
        },
        ip: response.data.query,
      };

      logger.info('Current location retrieved', location);

      return {
        success: true,
        message: `📍 当前位置: ${location.country} ${location.province} ${location.city}\n🌐 坐标: ${location.location?.lat}, ${location.location?.lng}\n🔍 IP: ${location.ip}`,
        location,
      };
    }

    return {
      success: false,
      message: '无法获取位置信息',
    };
  } catch (error) {
    logger.error('Failed to get current location', { error });

    return {
      success: false,
      message: `获取位置失败: ${error instanceof Error ? error.message : String(error)}`,
    };
  }
}

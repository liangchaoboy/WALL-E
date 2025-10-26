export interface MapConfig {
  defaultService: 'baidu' | 'amap' | 'google';
  apiKeys?: {
    baidu?: string;
    amap?: string;
    google?: string;
  };
}

const config: MapConfig = {
  defaultService: process.env.DEFAULT_MAP_SERVICE as any || 'baidu',
  apiKeys: {
    baidu: process.env.BAIDU_MAP_API_KEY,
    amap: process.env.AMAP_API_KEY,
    google: process.env.GOOGLE_MAPS_API_KEY,
  },
};

export default config;

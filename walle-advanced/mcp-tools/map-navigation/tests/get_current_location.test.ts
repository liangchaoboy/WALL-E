import { getCurrentLocation } from '../src/tools/get_current_location.js';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('get_current_location tool', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should return current location from IP API', async () => {
    mockedAxios.get.mockResolvedValue({
      data: {
        status: 'success',
        country: 'China',
        regionName: 'Shanghai',
        city: 'Shanghai',
        lat: 31.2304,
        lon: 121.4737,
        query: '123.45.67.89',
      },
    });

    const result = await getCurrentLocation();

    expect(result.success).toBe(true);
    expect(result.location).toBeDefined();
    expect(result.location?.city).toBe('Shanghai');
    expect(result.location?.province).toBe('Shanghai');
    expect(result.location?.country).toBe('China');
    expect(result.location?.location).toEqual({
      lat: 31.2304,
      lng: 121.4737,
    });
  });

  it('should return error when IP API fails', async () => {
    mockedAxios.get.mockResolvedValue({
      data: {
        status: 'fail',
      },
    });

    const result = await getCurrentLocation();

    expect(result.success).toBe(false);
    expect(result.message).toContain('无法获取位置信息');
  });

  it('should handle network errors gracefully', async () => {
    mockedAxios.get.mockRejectedValue(new Error('Network error'));

    const result = await getCurrentLocation();

    expect(result.success).toBe(false);
    expect(result.message).toContain('获取位置失败');
  });
});

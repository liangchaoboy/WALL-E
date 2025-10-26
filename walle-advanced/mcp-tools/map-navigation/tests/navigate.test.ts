import { navigate } from '../src/tools/navigate.js';
import * as browser from '../src/utils/browser.js';

jest.mock('../src/utils/browser.js');

describe('navigate tool', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should generate baidu maps URL and open browser', async () => {
    const mockOpen = jest.spyOn(browser, 'openInBrowser').mockResolvedValue(true);

    const result = await navigate({
      origin: '上海',
      destination: '北京',
      mode: 'transit',
      mapService: 'baidu',
    });

    expect(result.success).toBe(true);
    expect(result.url).toContain('map.baidu.com');
    expect(result.url).toContain('origin');
    expect(result.url).toContain('destination');
    expect(mockOpen).toHaveBeenCalledWith(expect.stringContaining('map.baidu.com'));
  });

  it('should generate amap URL when mapService is amap', async () => {
    const mockOpen = jest.spyOn(browser, 'openInBrowser').mockResolvedValue(true);

    const result = await navigate({
      origin: '上海',
      destination: '北京',
      mapService: 'amap',
    });

    expect(result.success).toBe(true);
    expect(result.url).toContain('amap.com');
    expect(mockOpen).toHaveBeenCalled();
  });

  it('should generate google maps URL when mapService is google', async () => {
    const mockOpen = jest.spyOn(browser, 'openInBrowser').mockResolvedValue(true);

    const result = await navigate({
      origin: 'Shanghai',
      destination: 'Beijing',
      mapService: 'google',
    });

    expect(result.success).toBe(true);
    expect(result.url).toContain('google.com/maps');
    expect(mockOpen).toHaveBeenCalled();
  });

  it('should return error when origin is empty', async () => {
    const result = await navigate({
      origin: '',
      destination: '北京',
    });

    expect(result.success).toBe(false);
    expect(result.message).toContain('起点不能为空');
  });

  it('should return error when destination is empty', async () => {
    const result = await navigate({
      origin: '上海',
      destination: '',
    });

    expect(result.success).toBe(false);
    expect(result.message).toContain('终点不能为空');
  });

  it('should return error when browser fails to open', async () => {
    const mockOpen = jest.spyOn(browser, 'openInBrowser').mockResolvedValue(false);

    const result = await navigate({
      origin: '上海',
      destination: '北京',
    });

    expect(result.success).toBe(false);
    expect(result.message).toContain('打开浏览器失败');
    expect(mockOpen).toHaveBeenCalled();
  });

  it('should trim whitespace from origin and destination', async () => {
    const mockOpen = jest.spyOn(browser, 'openInBrowser').mockResolvedValue(true);

    const result = await navigate({
      origin: '  上海  ',
      destination: '  北京  ',
    });

    expect(result.success).toBe(true);
    expect(result.message).toContain('上海');
    expect(result.message).toContain('北京');
    expect(mockOpen).toHaveBeenCalled();
  });
});

import { searchLocation } from '../src/tools/search_location.js';
import * as browser from '../src/utils/browser.js';

jest.mock('../src/utils/browser.js');

describe('search_location tool', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should generate baidu maps search URL and open browser', async () => {
    const mockOpen = jest.spyOn(browser, 'openInBrowser').mockResolvedValue(true);

    const result = await searchLocation({
      query: '东方明珠',
      mapService: 'baidu',
    });

    expect(result.success).toBe(true);
    expect(result.url).toContain('map.baidu.com');
    expect(result.url).toContain('query');
    expect(mockOpen).toHaveBeenCalledWith(expect.stringContaining('map.baidu.com'));
  });

  it('should generate amap search URL when mapService is amap', async () => {
    const mockOpen = jest.spyOn(browser, 'openInBrowser').mockResolvedValue(true);

    const result = await searchLocation({
      query: '东方明珠',
      city: '上海',
      mapService: 'amap',
    });

    expect(result.success).toBe(true);
    expect(result.url).toContain('amap.com');
    expect(mockOpen).toHaveBeenCalled();
  });

  it('should generate google maps search URL when mapService is google', async () => {
    const mockOpen = jest.spyOn(browser, 'openInBrowser').mockResolvedValue(true);

    const result = await searchLocation({
      query: 'Eiffel Tower',
      mapService: 'google',
    });

    expect(result.success).toBe(true);
    expect(result.url).toContain('google.com/maps');
    expect(mockOpen).toHaveBeenCalled();
  });

  it('should return error when query is empty', async () => {
    const result = await searchLocation({
      query: '',
    });

    expect(result.success).toBe(false);
    expect(result.message).toContain('搜索关键词不能为空');
  });

  it('should return error when browser fails to open', async () => {
    const mockOpen = jest.spyOn(browser, 'openInBrowser').mockResolvedValue(false);

    const result = await searchLocation({
      query: '东方明珠',
    });

    expect(result.success).toBe(false);
    expect(result.message).toContain('打开浏览器失败');
    expect(mockOpen).toHaveBeenCalled();
  });

  it('should trim whitespace from query', async () => {
    const mockOpen = jest.spyOn(browser, 'openInBrowser').mockResolvedValue(true);

    const result = await searchLocation({
      query: '  东方明珠  ',
    });

    expect(result.success).toBe(true);
    expect(result.message).toContain('东方明珠');
    expect(mockOpen).toHaveBeenCalled();
  });
});

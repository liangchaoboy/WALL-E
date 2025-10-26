import open from 'open';
import { logger } from './logger.js';

export async function openInBrowser(url: string): Promise<boolean> {
  try {
    logger.info('Opening URL in browser', { url });
    await open(url);
    return true;
  } catch (error) {
    logger.error('Failed to open browser', { error, url });
    return false;
  }
}

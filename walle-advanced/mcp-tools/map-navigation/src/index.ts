#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import { navigate, NavigateParams } from './tools/navigate.js';
import { searchLocation, SearchLocationParams } from './tools/search_location.js';
import { getCurrentLocation } from './tools/get_current_location.js';
import { logger } from './utils/logger.js';

const server = new Server(
  {
    name: 'map-navigation',
    version: '0.1.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

const tools: Tool[] = [
  {
    name: 'navigate',
    description: 'Open map navigation from origin to destination. Supports multiple map services (Baidu Maps, Amap, Google Maps) and travel modes (driving, transit, walking).',
    inputSchema: {
      type: 'object',
      properties: {
        origin: {
          type: 'string',
          description: 'Starting location (e.g., "上海七牛云", "Shanghai")',
        },
        destination: {
          type: 'string',
          description: 'Target location (e.g., "虹桥机场", "Beijing")',
        },
        mode: {
          type: 'string',
          enum: ['driving', 'transit', 'walking'],
          description: 'Travel mode (optional, defaults to "transit")',
        },
        mapService: {
          type: 'string',
          enum: ['baidu', 'amap', 'google'],
          description: 'Map service to use (optional, defaults to "baidu")',
        },
      },
      required: ['origin', 'destination'],
    },
  },
  {
    name: 'search_location',
    description: 'Search for a location on the map. Returns search results with location details and opens the map in browser.',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'Location search query (e.g., "东方明珠", "Eiffel Tower")',
        },
        city: {
          type: 'string',
          description: 'City to limit search to (optional, e.g., "上海", "Paris")',
        },
        mapService: {
          type: 'string',
          enum: ['baidu', 'amap', 'google'],
          description: 'Map service to use (optional, defaults to "baidu")',
        },
      },
      required: ['query'],
    },
  },
  {
    name: 'get_current_location',
    description: 'Get the current location based on IP address. Returns city, province, country, and coordinates.',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
];

server.setRequestHandler(ListToolsRequestSchema, async () => {
  logger.info('List tools requested');
  return { tools };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  logger.info('Tool called', { name, args });

  try {
    switch (name) {
      case 'navigate': {
        const result = await navigate(args as NavigateParams);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'search_location': {
        const result = await searchLocation(args as SearchLocationParams);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'get_current_location': {
        const result = await getCurrentLocation();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    logger.error('Tool execution failed', { name, error });
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: false,
            message: `执行失败: ${error instanceof Error ? error.message : String(error)}`,
          }),
        },
      ],
      isError: true,
    };
  }
});

async function main() {
  logger.info('Starting Map Navigation MCP Server');

  const transport = new StdioServerTransport();
  await server.connect(transport);

  logger.info('Map Navigation MCP Server started successfully');
}

main().catch((error) => {
  logger.error('Server failed to start', { error });
  process.exit(1);
});

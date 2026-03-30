import { Client, ActivityType } from 'discord.js';
import { Event } from '../types';

const readyEvent: Event = {
  name: 'ready',
  once: true,
  execute: async (client: Client) => {
    if (!client.user) return;

    console.log(`✅ ${client.user.tag} is online and ready!`);

    // Set bot activity
    await client.user.setPresence({
      activities: [
        {
          name: '/help for commands',
          type: ActivityType.Listening,
        },
      ],
      status: 'online',
    });

    console.log(`📊 Serving ${client.guilds.cache.size} servers`);
  },
};

export default readyEvent;

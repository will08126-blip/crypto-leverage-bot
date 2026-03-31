import { Client, ActivityType, REST, Routes } from 'discord.js';
import { Event } from '../types';

const readyEvent: Event = {
  name: 'ready',
  once: true,
  execute: async (client: Client) => {
    if (!client.user) return;

    console.log(`✅ ${client.user.tag} is online and ready!`);

    // Register slash commands with Discord
    const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_BOT_TOKEN!);
    
    try {
      console.log('🔄 Registering slash commands...');
      
      // Convert commands to API format using their data property
      const commands = client.commands
        .filter(cmd => cmd.data)
        .map(cmd => cmd.data!.toJSON());

      if (commands.length === 0) {
        console.warn('⚠️  No commands with data property found to register');
      } else {
        // Check if guild ID is available for faster registration
        const guildId = process.env.DISCORD_GUILD_ID;
        
        if (guildId) {
          // Register guild-specific commands (instant)
          await rest.put(
            Routes.applicationGuildCommands(client.user.id, guildId),
            { body: commands }
          );
          console.log(`✅ Registered ${commands.length} slash commands for guild ${guildId}`);
        } else {
          // Register globally (takes up to 1 hour to propagate)
          await rest.put(Routes.applicationCommands(client.user.id), { body: commands });
          console.log(`✅ Registered ${commands.length} slash commands globally`);
          console.log('⚠️  Note: Global commands may take up to 1 hour to appear');
          console.log('    Add DISCORD_GUILD_ID for instant registration');
        }
      }
    } catch (error) {
      console.error('❌ Failed to register commands:', error);
    }

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

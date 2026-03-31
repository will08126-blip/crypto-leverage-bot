import { Interaction, Client, CommandInteraction } from 'discord.js';
import { Event } from '../types';

const interactionCreateEvent: Event = {
  name: 'interactionCreate',
  once: false,
  execute: async (interaction: Interaction, client: Client) => {
    if (!interaction.isChatInputCommand()) return;

    const command = client.commands.get(interaction.commandName);
    if (!command) {
      console.error(`Command not found: ${interaction.commandName}`);
      return;
    }

    try {
      await command.execute(interaction as CommandInteraction, client);
    } catch (error) {
      console.error(`Error executing command ${interaction.commandName}:`, error);
      await interaction.reply({ content: 'An error occurred while executing this command.', ephemeral: true });
    }
  },
};

export default interactionCreateEvent;
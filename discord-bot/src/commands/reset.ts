import { SlashCommandBuilder, ChatInputCommandInteraction, CacheType, EmbedBuilder, Client } from 'discord.js';
import { Command } from '../types/index';
import axios from 'axios';

const resetCommand: Command = {
  name: 'reset',
  description: 'Reset all positions and balance (default $1000)',
  data: new SlashCommandBuilder()
    .setName('reset')
    .setDescription('Reset all positions and balance (default $1000)')
    .addNumberOption(option =>
      option.setName('balance')
        .setDescription('New balance (optional, default 1000)')
        .setRequired(false)) as SlashCommandBuilder,
  execute: async (interaction: ChatInputCommandInteraction<CacheType>, client: Client) => {
    const newBalance = interaction.options.getNumber('balance') || 1000;
    
    try {
      await axios.post('http://localhost:5000/reset', {
        balance: newBalance
      });
      
      const embed = new EmbedBuilder()
        .setColor('#00ff00')
        .setTitle('✅ Simulation Reset')
        .setDescription(`All positions closed and balance reset to **${newBalance} USDT**`)
        .setTimestamp();

      await interaction.reply({ embeds: [embed], ephemeral: true });
    } catch (error) {
      console.error('Error resetting simulation:', error);
      await interaction.reply({ content: 'Failed to reset simulation. Is the trading engine running?', ephemeral: true });
    }
  },
};

export default resetCommand;
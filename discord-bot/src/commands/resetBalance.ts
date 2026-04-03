import { SlashCommandBuilder, ChatInputCommandInteraction, CacheType, EmbedBuilder, Client } from 'discord.js';
import { Command } from '../types/index';
import axios from 'axios';

const resetBalanceCommand: Command = {
  name: 'resetbalance',
  description: 'Reset account balance to default ($1000)',
  data: new SlashCommandBuilder()
    .setName('resetbalance')
    .setDescription('Reset account balance to default ($1000)')
    .addNumberOption(option =>
      option.setName('balance')
        .setDescription('New balance (optional, default 1000)')
        .setRequired(false)) as SlashCommandBuilder,
  execute: async (interaction: ChatInputCommandInteraction<CacheType>, client: Client) => {
    const newBalance = interaction.options.getNumber('balance') || 1000;
    
    try {
      await axios.post('http://localhost:5000/command', {
        action: 'reset_balance',
        balance: newBalance
      });
      
      const embed = new EmbedBuilder()
        .setColor('#00ff00')
        .setTitle('✅ Balance Reset')
        .setDescription(`Account balance reset to **${newBalance} USDT**`)
        .setTimestamp();

      await interaction.reply({ embeds: [embed], ephemeral: true });
    } catch (error) {
      console.error('Error resetting balance:', error);
      await interaction.reply({ content: 'Failed to reset balance. Is the trading engine running?', ephemeral: true });
    }
  },
};

export default resetBalanceCommand;
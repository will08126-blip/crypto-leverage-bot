import { SlashCommandBuilder, ChatInputCommandInteraction, CacheType, EmbedBuilder, Client } from 'discord.js';
import { Command } from '../types/index';
import axios from 'axios';

const setBalanceCommand: Command = {
  name: 'setbalance',
  description: 'Set account balance to a specific amount',
  data: new SlashCommandBuilder()
    .setName('setbalance')
    .setDescription('Set account balance to a specific amount')
    .addNumberOption(option =>
      option.setName('amount')
        .setDescription('New balance amount')
        .setRequired(true)) as SlashCommandBuilder,
  execute: async (interaction: ChatInputCommandInteraction<CacheType>, client: Client) => {
    const amount = interaction.options.getNumber('amount');
    if (!amount || amount <= 0) {
      await interaction.reply({ content: 'Please provide a positive amount.', ephemeral: true });
      return;
    }
    
    try {
      await axios.post('http://localhost:5000/command', {
        action: 'set_balance',
        balance: amount
      });
      
      const embed = new EmbedBuilder()
        .setColor('#00ff00')
        .setTitle('✅ Balance Updated')
        .setDescription(`Account balance set to **${amount} USDT**`)
        .setTimestamp();

      await interaction.reply({ embeds: [embed], ephemeral: true });
    } catch (error) {
      console.error('Error setting balance:', error);
      await interaction.reply({ content: 'Failed to set balance. Is the trading engine running?', ephemeral: true });
    }
  },
};

export default setBalanceCommand;
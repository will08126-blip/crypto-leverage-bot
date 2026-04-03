import { SlashCommandBuilder, ChatInputCommandInteraction, CacheType, EmbedBuilder, Client } from 'discord.js';
import { Command } from '../types/index';
import axios from 'axios';

const balanceCommand: Command = {
  name: 'balance',
  description: 'View your account balance',
  data: new SlashCommandBuilder()
    .setName('balance')
    .setDescription('View your account balance'),
  execute: async (interaction: ChatInputCommandInteraction<CacheType>, client: Client) => {
    try {
      const response = await axios.get('http://localhost:5000/balance');
      const balance = response.data.balance;
      
      const embed = new EmbedBuilder()
        .setColor('#00ff00')
        .setTitle('💰 Account Balance')
        .addFields(
          {
            name: 'Total Balance',
            value: `${balance.toFixed(2)} USDT`,
            inline: true,
          },
        )
        .setTimestamp();

      await interaction.reply({ embeds: [embed], ephemeral: true });
    } catch (error) {
      console.error('Error fetching balance:', error);
      await interaction.reply({ content: 'Failed to fetch balance. Is the trading engine running?', ephemeral: true });
    }
  },
};

export default balanceCommand;

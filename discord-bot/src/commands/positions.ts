import { SlashCommandBuilder, ChatInputCommandInteraction, CacheType, EmbedBuilder, Client } from 'discord.js';
import { Command } from '../types/index';
import axios from 'axios';

const positionsCommand: Command = {
  name: 'positions',
  description: 'View open positions',
  data: new SlashCommandBuilder()
    .setName('positions')
    .setDescription('View open positions'),
  execute: async (interaction: ChatInputCommandInteraction<CacheType>, client: Client) => {
    try {
      const response = await axios.get('http://localhost:5000/positions');
      const positions = response.data.positions;
      
      if (!positions || positions.length === 0) {
        await interaction.reply({ content: 'No open positions.', ephemeral: true });
        return;
      }

      const embed = new EmbedBuilder()
        .setColor('#00ff00')
        .setTitle('📊 Open Positions')
        .setTimestamp();

      positions.forEach((pos: any, index: number) => {
        embed.addFields({
          name: `${index + 1}. ${pos.symbol} (${pos.side.toUpperCase()})`,
          value: `Entry: ${pos.entry_price}\nSize: ${pos.size}\nLeverage: ${pos.leverage}x\nPnL: ${pos.pnl?.toFixed(2) ?? 'N/A'}`,
          inline: false,
        });
      });

      await interaction.reply({ embeds: [embed], ephemeral: true });
    } catch (error) {
      console.error('Error fetching positions:', error);
      await interaction.reply({ content: 'Failed to fetch positions. Is the trading engine running?', ephemeral: true });
    }
  },
};

export default positionsCommand;
import { SlashCommandBuilder, CommandInteraction, EmbedBuilder, Client } from 'discord.js';
import { Command } from '../types/index';

const balanceCommand: Command = {
  name: 'balance',
  description: 'View your account balance',
  execute: async (interaction: CommandInteraction, client: Client) => {
    // In production, this would fetch from your trading engine
    // For now, return mock data
    const mockBalance = {
      total: 10000.50,
      available: 8500.25,
      inPositions: 1500.25,
      currency: 'USDT',
    };

    const embed = new EmbedBuilder()
      .setColor('#00ff00')
      .setTitle('💰 Account Balance')
      .addFields(
        {
          name: 'Total Balance',
          value: `${mockBalance.total.toFixed(2)} ${mockBalance.currency}`,
          inline: true,
        },
        {
          name: 'Available',
          value: `${mockBalance.available.toFixed(2)} ${mockBalance.currency}`,
          inline: true,
        },
        {
          name: 'In Positions',
          value: `${mockBalance.inPositions.toFixed(2)} ${mockBalance.currency}`,
          inline: true,
        },
      )
      .setTimestamp();

    await interaction.reply({ embeds: [embed], ephemeral: true });
  },
};

export default balanceCommand;

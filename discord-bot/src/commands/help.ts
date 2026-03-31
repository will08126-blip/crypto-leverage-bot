import { SlashCommandBuilder, CommandInteraction, EmbedBuilder, Client } from 'discord.js';
import { Command } from '../types/index';

const helpCommand: Command = {
  name: 'help',
  description: 'Show all available commands',
  execute: async (interaction: CommandInteraction, client: Client) => {
    const embed = new EmbedBuilder()
      .setColor('#0099ff')
      .setTitle('🤖 Crypto Leverage Bot - Help')
      .setDescription('Here are the available commands:')
      .addFields(
        {
          name: '/trade <symbol> <direction> <leverage>',
          value: 'Open a new position. Example: `/trade BTC/USDT long 10`',
          inline: false,
        },
        {
          name: '/close <symbol>',
          value: 'Close an open position. Example: `/close BTC/USDT`',
          inline: false,
        },
        {
          name: '/positions',
          value: 'View all current open positions',
          inline: false,
        },
        {
          name: '/balance',
          value: 'View your account balance',
          inline: false,
        },
        {
          name: '/backtest <strategy> <symbol> <timeframe>',
          value: 'Run backtest on historical data. Example: `/backtest rsi_strategy BTC/USDT 1h`',
          inline: false,
        },
        {
          name: '/help',
          value: 'Show this help message',
          inline: false,
        },
      )
      .setFooter({ text: 'Use responsibly - leverage trading is risky!' });

    await interaction.reply({ embeds: [embed], ephemeral: true });
  },
};

export default helpCommand;

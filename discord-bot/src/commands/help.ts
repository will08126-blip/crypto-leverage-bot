import { SlashCommandBuilder, ChatInputCommandInteraction, CacheType, EmbedBuilder, Client } from 'discord.js';
import { Command } from '../types/index';

const helpCommand: Command = {
  name: 'help',
  description: 'Show all available commands',
  data: new SlashCommandBuilder()
    .setName('help')
    .setDescription('Show all available commands'),
  execute: async (interaction: ChatInputCommandInteraction<CacheType>, client: Client) => {
    const embed = new EmbedBuilder()
      .setColor('#0099ff')
      .setTitle('🤖 Crypto Leverage Bot - Help')
      .setDescription('Here are the available commands:')
      .addFields(
        {
          name: '/balance',
          value: 'View your account balance',
          inline: false,
        },
        {
          name: '/positions',
          value: 'View all current open positions',
          inline: false,
        },
        {
          name: '/resetbalance [amount]',
          value: 'Reset account balance to default ($1000) or specified amount',
          inline: false,
        },
        {
          name: '/setbalance <amount>',
          value: 'Set account balance to a specific amount',
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

import { SlashCommandBuilder, ChatInputCommandInteraction, CacheType, EmbedBuilder, Client } from 'discord.js';
import { Command } from '../types/index';
import axios from 'axios';

const aggressionCommand: Command = {
  name: 'setaggression',
  description: 'Set trading aggression level (1-10)',
  data: new SlashCommandBuilder()
    .setName('setaggression')
    .setDescription('Set trading aggression level (1-10)')
    .addIntegerOption(option =>
      option.setName('level')
        .setDescription('Aggression level (1=conservative, 10=aggressive)')
        .setRequired(true)
        .setMinValue(1)
        .setMaxValue(10)) as SlashCommandBuilder,
  execute: async (interaction: ChatInputCommandInteraction<CacheType>, client: Client) => {
    const level = interaction.options.getInteger('level', true);
    
    // Define aggression mapping
    const aggressionMap: { [key: number]: { min_confidence: number, risk_per_trade: number, leverage: number } } = {
      1: { min_confidence: 0.8, risk_per_trade: 0.005, leverage: 1 },
      2: { min_confidence: 0.75, risk_per_trade: 0.007, leverage: 2 },
      3: { min_confidence: 0.7, risk_per_trade: 0.01, leverage: 3 },
      4: { min_confidence: 0.65, risk_per_trade: 0.012, leverage: 5 },
      5: { min_confidence: 0.6, risk_per_trade: 0.015, leverage: 7 },
      6: { min_confidence: 0.55, risk_per_trade: 0.02, leverage: 10 },
      7: { min_confidence: 0.5, risk_per_trade: 0.025, leverage: 15 },
      8: { min_confidence: 0.45, risk_per_trade: 0.03, leverage: 20 },
      9: { min_confidence: 0.4, risk_per_trade: 0.04, leverage: 30 },
      10: { min_confidence: 0.35, risk_per_trade: 0.05, leverage: 50 }
    };
    
    const settings = aggressionMap[level] || aggressionMap[5];
    
    try {
      await axios.post('http://localhost:5000/config', {
        min_confidence: settings.min_confidence,
        risk_per_trade: settings.risk_per_trade,
        leverage: settings.leverage
      });
      
      const embed = new EmbedBuilder()
        .setColor('#00ff00')
        .setTitle('✅ Aggression Updated')
        .setDescription(`Level ${level} settings applied:`)
        .addFields(
          { name: 'Min Confidence', value: settings.min_confidence.toString(), inline: true },
          { name: 'Risk per Trade', value: `${(settings.risk_per_trade * 100).toFixed(1)}%`, inline: true },
          { name: 'Leverage', value: `${settings.leverage}x`, inline: true }
        )
        .setTimestamp();

      await interaction.reply({ embeds: [embed], ephemeral: true });
    } catch (error) {
      console.error('Error updating aggression:', error);
      await interaction.reply({ content: 'Failed to update aggression. Is the trading engine running?', ephemeral: true });
    }
  },
};

export default aggressionCommand;
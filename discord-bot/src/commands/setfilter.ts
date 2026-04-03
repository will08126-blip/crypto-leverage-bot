import { SlashCommandBuilder, ChatInputCommandInteraction, CacheType, EmbedBuilder, Client } from 'discord.js';
import { Command } from '../types/index';
import axios from 'axios';

const setFilterCommand: Command = {
  name: 'setfilter',
  description: 'Adjust signal filtering parameters',
  data: new SlashCommandBuilder()
    .setName('setfilter')
    .setDescription('Adjust signal filtering parameters')
    .addNumberOption(option =>
      option.setName('min_confidence')
        .setDescription('Minimum confidence threshold (0.0-1.0)')
        .setRequired(false)
        .setMinValue(0)
        .setMaxValue(1))
    .addIntegerOption(option =>
      option.setName('max_positions')
        .setDescription('Maximum concurrent positions')
        .setRequired(false)
        .setMinValue(1)
        .setMaxValue(10))
    .addBooleanOption(option =>
      option.setName('require_consensus')
        .setDescription('Require at least two strategies to agree')
        .setRequired(false)) as SlashCommandBuilder,
  execute: async (interaction: ChatInputCommandInteraction<CacheType>, client: Client) => {
    const minConfidence = interaction.options.getNumber('min_confidence');
    const maxPositions = interaction.options.getInteger('max_positions');
    const requireConsensus = interaction.options.getBoolean('require_consensus');
    
    const updates: { [key: string]: any } = {};
    if (minConfidence !== null) updates['min_confidence'] = minConfidence;
    if (maxPositions !== null) updates['max_positions'] = maxPositions;
    if (requireConsensus !== null) updates['require_consensus'] = requireConsensus;
    
    if (Object.keys(updates).length === 0) {
      await interaction.reply({ content: 'No parameters provided. Use at least one option.', ephemeral: true });
      return;
    }
    
    try {
      await axios.post('http://localhost:5000/config', updates);
      
      const embed = new EmbedBuilder()
        .setColor('#00ff00')
        .setTitle('✅ Filter Parameters Updated')
        .setDescription('The following parameters were updated:')
        .addFields(
          ...Object.entries(updates).map(([key, value]) => ({
            name: key,
            value: String(value),
            inline: true,
          }))
        )
        .setTimestamp();

      await interaction.reply({ embeds: [embed], ephemeral: true });
    } catch (error) {
      console.error('Error updating filter parameters:', error);
      await interaction.reply({ content: 'Failed to update filter parameters. Is the trading engine running?', ephemeral: true });
    }
  },
};

export default setFilterCommand;
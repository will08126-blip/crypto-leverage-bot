import { Client, EmbedBuilder, TextChannel } from 'discord.js';

/**
 * Send a trading signal to a Discord channel
 */
export async function sendSignalToDiscord(
  client: Client,
  channelId: string,
  signal: {
    symbol: string;
    direction: 'long' | 'short';
    entryPrice: number;
    stopLoss: number;
    takeProfit: number;
    leverage: number;
    indicator: string;
    confidence: number;
  }
): Promise<void> {
  if (!channelId) {
    console.error('❌ No Discord channel ID configured');
    return;
  }

  try {
    const channel = client.channels.cache.get(channelId) as TextChannel;
    if (!channel) {
      console.error(`❌ Channel ${channelId} not found`);
      return;
    }

    const color = signal.direction === 'long' ? 0x00ff00 : 0xff0000;
    const emoji = signal.direction === 'long' ? '📈' : '📉';

    const embed = new EmbedBuilder()
      .setColor(color)
      .setTitle(`${emoji} ${signal.symbol} ${signal.direction.toUpperCase()} Signal`)
      .addFields(
        {
          name: 'Entry Price',
          value: `$${signal.entryPrice.toLocaleString()}`,
          inline: true,
        },
        {
          name: 'Stop Loss',
          value: `$${signal.stopLoss.toLocaleString()}`,
          inline: true,
        },
        {
          name: 'Take Profit',
          value: `$${signal.takeProfit.toLocaleString()}`,
          inline: true,
        },
        {
          name: 'Leverage',
          value: `${signal.leverage}x`,
          inline: true,
        },
        {
          name: 'Indicator',
          value: signal.indicator,
          inline: true,
        },
        {
          name: 'Confidence',
          value: `${(signal.confidence * 100).toFixed(0)}%`,
          inline: true,
        }
      )
      .setTimestamp()
      .setFooter({ text: 'Trading Signal' });

    await channel.send({ embeds: [embed] });
    console.log(`✅ Signal sent to channel ${channelId}: ${signal.symbol} ${signal.direction}`);
  } catch (error) {
    console.error('❌ Failed to send signal to Discord:', error);
  }
}

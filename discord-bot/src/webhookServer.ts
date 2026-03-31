import express, { Request, Response } from 'express';
import { Client } from 'discord.js';
import { sendSignalToDiscord } from './utils/signalSender';

const app = express();
app.use(express.json());

/**
 * Initialize webhook server
 */
export function initWebhookServer(client: Client) {
  const PORT = process.env.WEBHOOK_PORT || 3000;
  const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET || 'your-webhook-secret';

  // Health check endpoint
  app.get('/health', (req: Request, res: Response) => {
    res.json({ status: 'ok', bot: client.user?.tag });
  });

  // Trading signal endpoint
  app.post('/webhook/signal', (req: Request, res: Response) => {
    // Verify secret if configured
    const secret = req.headers['x-webhook-secret'];
    if (WEBHOOK_SECRET && secret !== WEBHOOK_SECRET) {
      console.log('❌ Unauthorized webhook request');
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const signal = req.body;
    const channelId = process.env.DISCORD_CHANNEL_ID;

    if (!channelId) {
      console.error('❌ DISCORD_CHANNEL_ID not configured');
      return res.status(500).json({ error: 'Channel ID not configured' });
    }

    console.log('📥 Received signal:', signal);

    // Send signal to Discord
    sendSignalToDiscord(client, channelId, signal)
      .then(() => {
        res.json({ success: true, message: 'Signal sent to Discord' });
      })
      .catch((error) => {
        console.error('❌ Failed to process signal:', error);
        res.status(500).json({ error: 'Failed to send signal' });
      });
  });

  // Start server
  app.listen(PORT, () => {
    console.log(`🌐 Webhook server running on port ${PORT}`);
    console.log(`   POST http://localhost:${PORT}/webhook/signal`);
  });

  return app;
}

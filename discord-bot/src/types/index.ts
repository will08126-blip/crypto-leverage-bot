import { Client, ChatInputCommandInteraction, CacheType, Message, Collection, SlashCommandBuilder } from 'discord.js';

export interface Command {
  name: string;
  description: string;
  data?: SlashCommandBuilder;
  options?: any[];
  execute: (interaction: ChatInputCommandInteraction<CacheType>, client: Client) => Promise<void> | void;
}

export interface Event {
  name: string;
  once?: boolean;
  execute: (...args: any[]) => Promise<void> | void;
}

export interface TradingSignal {
  symbol: string;
  direction: 'long' | 'short';
  price?: number;
  entryPrice?: number;
  stopLoss?: number;
  takeProfit?: number;
  leverage?: number;
  timestamp: Date;
  indicator?: string;
  confidence?: number;
}

export interface Position {
  symbol: string;
  side: 'long' | 'short';
  entryPrice: number;
  size: number;
  leverage: number;
  timestamp: Date;
  pnl?: number;
}

export interface AccountBalance {
  total: number;
  available: number;
  inPositions: number;
  currency: string;
}

export interface BacktestResult {
  strategy: string;
  symbol: string;
  timeframe: string;
  startDate: Date;
  endDate: Date;
  totalTrades: number;
  winningTrades: number;
  losingTrades: number;
  totalPnL: number;
  winRate: number;
  sharpeRatio?: number;
  maxDrawdown?: number;
}

export interface BotConfig {
  exchange: string;
  leverage: number;
  riskPerTrade: number;
  stopLoss: number;
  takeProfit: number;
  maxPositions: number;
}


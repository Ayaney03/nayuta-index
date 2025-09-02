// あやねえボットの設定ファイル

module.exports = {
  // ボットの基本設定
  bot: {
    name: 'あやねえボット',
    description: '秘書力マスター講座生向けのサポートボット',
    version: '1.0.0',
    color: '#1E90FF', // あやねえの青色
    prefix: '!',
    emoji: '💎'
  },

  // 回答の設定
  responses: {
    maxLessons: 3, // 一度に表示する最大レッスン数
    defaultTimeout: 5000, // 回答のタイムアウト（ミリ秒）
    errorMessage: '💎 すみません、少し調子が悪いみたい...もう一度試してもらえますか？',
    emptyMessage: '💎 こんにちは！何かお困りのことはありますか？\n\n例：「スプレッドシートでデータをまとめるときのコツを教えて」'
  },

  // あやねえの特徴的な表現
  expressions: {
    greeting: ['💎 こんにちは！', '💎 お疲れさまです！', '💎 何かお手伝いできることはありますか？'],
    encouragement: ['頑張って！', '応援してます✨', 'きっとできますよ！', '一緒に頑張りましょう！'],
    selfTalk: ['やばくない？', '怖すぎ', 'これ、本当に大事', 'マジで重要'],
    actionPrompt: ['まずは行動してみて！', '実践あるのみ！', '今日からできること', '明日から試してみて']
  },

  // レッスンカテゴリの設定
  categories: {
    spreadsheet: {
      name: 'スプレッドシート活用',
      icon: '📊',
      color: '#4CAF50'
    },
    efficiency: {
      name: '時短・効率化',
      icon: '⚡',
      color: '#FF9800'
    },
    communication: {
      name: 'コミュニケーション',
      icon: '💬',
      color: '#2196F3'
    },
    mindset: {
      name: 'マインドセット',
      icon: '🧠',
      color: '#9C27B0'
    },
    worklife: {
      name: '家事育児両立',
      icon: '👨‍👩‍👧‍👦',
      color: '#E91E63'
    },
    income: {
      name: '収入アップ',
      icon: '💰',
      color: '#FFC107'
    }
  },

  // Discord設定
  discord: {
    intents: [
      'Guilds',
      'GuildMessages', 
      'MessageContent',
      'DirectMessages'
    ],
    permissions: [
      'SendMessages',
      'ReadMessageHistory',
      'UseSlashCommands',
      'EmbedLinks',
      'ReadMessages'
    ]
  },

  // ログ設定
  logging: {
    level: 'info', // debug, info, warn, error
    logToFile: false,
    logFile: 'bot.log'
  }
};

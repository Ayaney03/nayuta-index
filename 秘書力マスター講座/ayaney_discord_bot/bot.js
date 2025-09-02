const { Client, GatewayIntentBits, EmbedBuilder } = require('discord.js');
const { findRelevantLessons, getResponsePattern } = require('./knowledge_base');
require('dotenv').config();

// Discordクライアントの初期化
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.DirectMessages
  ]
});

// ボットが起動したときの処理
client.once('ready', () => {
  console.log(`🤖 あやねえボットが起動しました！ ${client.user.tag} としてログイン中`);
  
  // ボットのステータスを設定
  client.user.setActivity('秘書力マスター講座をサポート中 💎', { type: 'WATCHING' });
});

// メッセージを受信したときの処理
client.on('messageCreate', async (message) => {
  // ボット自身のメッセージは無視
  if (message.author.bot) return;
  
  // DMまたは@メンションされた場合のみ反応
  const isMentioned = message.mentions.has(client.user);
  const isDM = message.channel.type === 1; // DM_CHANNEL
  
  if (!isMentioned && !isDM) return;
  
  try {
    // メッセージ内容を取得（メンションを除去）
    let userMessage = message.content;
    if (isMentioned) {
      userMessage = userMessage.replace(`<@${client.user.id}>`, '').trim();
    }
    
    // 空のメッセージの場合
    if (!userMessage) {
      await message.reply('💎 こんにちは！何かお困りのことはありますか？\n\n例：「スプレッドシートでデータをまとめるときのコツを教えて」');
      return;
    }
    
    // 関連レッスンを検索
    const relevantLessons = findRelevantLessons(userMessage);
    
    // 回答パターンを取得
    const responsePattern = getResponsePattern(userMessage);
    
    // 回答を構築
    let response = responsePattern.response;
    
    // 関連レッスンがある場合は追加
    if (relevantLessons.length > 0) {
      response += '\n\n🔹 **おすすめレッスン**\n';
      relevantLessons.slice(0, 3).forEach((lesson, index) => {
        response += `${index + 1}. **${lesson.title}**\n   ${lesson.description}\n\n`;
      });
    }
    
    // Embedを作成してより見やすく
    const embed = new EmbedBuilder()
      .setColor('#1E90FF') // あやねえの青色
      .setTitle('💎 あやねえからのアドバイス')
      .setDescription(response)
      .setFooter({ 
        text: '秘書力マスター講座 | 詳しいレッスンはDiscordのレッスンチャンネルをチェック！',
        iconURL: client.user.displayAvatarURL()
      })
      .setTimestamp();
    
    await message.reply({ embeds: [embed] });
    
  } catch (error) {
    console.error('エラーが発生しました:', error);
    await message.reply('💎 すみません、少し調子が悪いみたい...もう一度試してもらえますか？');
  }
});

// よくある質問コマンド
client.on('messageCreate', async (message) => {
  if (message.author.bot) return;
  
  // !faq コマンド
  if (message.content.toLowerCase().startsWith('!faq') || message.content.toLowerCase().startsWith('！faq')) {
    const embed = new EmbedBuilder()
      .setColor('#1E90FF')
      .setTitle('💎 よくある質問')
      .setDescription(`
🔹 **スプレッドシートの見栄えを良くしたい**
→ @あやねえボット スプレッドシート 整理

🔹 **時短術を知りたい**
→ @あやねえボット 時短 効率化

🔹 **クライアントとのコミュニケーション**
→ @あやねえボット クライアント コミュニケーション

🔹 **家事と仕事の両立**
→ @あやねえボット 家事 両立

🔹 **単価アップの方法**
→ @あやねえボット 単価 アップ

**使い方：** @あやねえボット [質問内容] で質問してね！
      `)
      .setFooter({ text: '秘書力マスター講座 | あやねえボット' });
    
    await message.reply({ embeds: [embed] });
  }
});

// ヘルプコマンド
client.on('messageCreate', async (message) => {
  if (message.author.bot) return;
  
  if (message.content.toLowerCase().startsWith('!help') || message.content.toLowerCase().startsWith('！help')) {
    const embed = new EmbedBuilder()
      .setColor('#1E90FF')
      .setTitle('💎 あやねえボットの使い方')
      .setDescription(`
**基本的な使い方：**
- @あやねえボット [質問内容] でメンション
- DMで直接質問も可能

**コマンド一覧：**
- \`!faq\` または \`！faq\` - よくある質問を表示
- \`!help\` または \`！help\` - このヘルプを表示

**質問例：**
- 「スプレッドシートでデータをまとめるときのコツは？」
- 「時短で仕事を効率化したい」
- 「クライアントとの連絡で気をつけることは？」

あやねえらしい実践的なアドバイスと、関連レッスンをお届けします✨
      `)
      .setFooter({ text: '秘書力マスター講座 | 替えの効かない最強の右腕を目指そう！' });
    
    await message.reply({ embeds: [embed] });
  }
});

// エラーハンドリング
client.on('error', error => {
  console.error('Discord.jsエラー:', error);
});

process.on('unhandledRejection', error => {
  console.error('未処理のPromise拒否:', error);
});

// ボットを起動
client.login(process.env.DISCORD_TOKEN);

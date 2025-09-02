// 🤖 Notion × Cursor 自動化スクリプト
// 秘書力マスター講座 9月ローンチ プロジェクト管理

const { Client } = require('@notionhq/client');
const fs = require('fs');
const path = require('path');

// Notion API設定
const notion = new Client({
  auth: process.env.NOTION_API_KEY, // 環境変数で設定
});

// データベースID（実際のIDに置き換える）
const DATABASES = {
  DAILY_TASKS: 'your-daily-tasks-database-id',
  TEAM_MEMBERS: 'your-team-members-database-id',
  KPI_TRACKING: 'your-kpi-tracking-database-id',
  CONTENT_BANK: 'your-content-bank-database-id'
};

// 📅 日次タスク自動生成
async function createDailyTasks(date) {
  const dailyTaskTemplates = [
    {
      name: 'X投稿（朝）',
      category: 'SNS',
      priority: '高',
      estimatedTime: 30,
      assignee: 'コンテンツチーム'
    },
    {
      name: 'X投稿（夜）',
      category: 'SNS', 
      priority: '高',
      estimatedTime: 30,
      assignee: 'コンテンツチーム'
    },
    {
      name: 'LINE配信確認',
      category: 'LINE',
      priority: '中',
      estimatedTime: 15,
      assignee: '運営チーム'
    },
    {
      name: '数値チェック・分析',
      category: '分析',
      priority: '中',
      estimatedTime: 20,
      assignee: '運営チーム'
    }
  ];

  for (const task of dailyTaskTemplates) {
    try {
      await notion.pages.create({
        parent: { database_id: DATABASES.DAILY_TASKS },
        properties: {
          '📝 タスク名': {
            title: [{ text: { content: task.name } }]
          },
          '📅 日付': {
            date: { start: date }
          },
          '🏷️ カテゴリ': {
            select: { name: task.category }
          },
          '⭐ 優先度': {
            select: { name: task.priority }
          },
          '📊 ステータス': {
            select: { name: '未着手' }
          },
          '⏰ 予定時間': {
            number: task.estimatedTime
          },
          '👤 担当者': {
            rich_text: [{ text: { content: task.assignee } }]
          }
        }
      });
      console.log(`✅ タスク作成完了: ${task.name} (${date})`);
    } catch (error) {
      console.error(`❌ タスク作成エラー: ${task.name}`, error);
    }
  }
}

// 📊 KPI データ自動更新
async function updateKPIData(data) {
  try {
    await notion.pages.create({
      parent: { database_id: DATABASES.KPI_TRACKING },
      properties: {
        '📅 日付': {
          date: { start: new Date().toISOString().split('T')[0] }
        },
        '📱 X フォロワー': {
          number: data.xFollowers || 0
        },
        '📧 LINE 登録者': {
          number: data.lineSubscribers || 0
        },
        '👀 エンゲージメント': {
          number: data.engagement || 0
        },
        '📞 問い合わせ数': {
          number: data.inquiries || 0
        },
        '💰 申込み数': {
          number: data.applications || 0
        },
        '📝 メモ': {
          rich_text: [{ text: { content: data.memo || '' } }]
        }
      }
    });
    console.log('✅ KPIデータ更新完了');
  } catch (error) {
    console.error('❌ KPIデータ更新エラー:', error);
  }
}

// 📝 コンテンツファイル同期
async function syncContentToNotion(filePath, category) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const fileName = path.basename(filePath);
    
    await notion.pages.create({
      parent: { database_id: DATABASES.CONTENT_BANK },
      properties: {
        '📝 タイトル': {
          title: [{ text: { content: fileName } }]
        },
        '🏷️ カテゴリ': {
          select: { name: category }
        },
        '📅 作成日': {
          date: { start: new Date().toISOString().split('T')[0] }
        },
        '📊 ステータス': {
          select: { name: '作成完了' }
        }
      },
      children: [
        {
          object: 'block',
          type: 'code',
          code: {
            caption: [],
            rich_text: [{ type: 'text', text: { content: content } }],
            language: 'markdown'
          }
        }
      ]
    });
    console.log(`✅ コンテンツ同期完了: ${fileName}`);
  } catch (error) {
    console.error(`❌ コンテンツ同期エラー: ${filePath}`, error);
  }
}

// 🔔 Slack通知機能
async function sendSlackNotification(message, channel = '#general') {
  // Slack Webhook URL（環境変数で設定）
  const webhookUrl = process.env.SLACK_WEBHOOK_URL;
  
  if (!webhookUrl) {
    console.log('Slack通知: ', message);
    return;
  }

  try {
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        channel: channel,
        text: message,
        username: '秘書力ローンチBot',
        icon_emoji: ':rocket:'
      })
    });
    
    if (response.ok) {
      console.log('✅ Slack通知送信完了');
    }
  } catch (error) {
    console.error('❌ Slack通知エラー:', error);
  }
}

// 📈 進捗レポート生成
async function generateProgressReport() {
  try {
    // 今日のタスクを取得
    const today = new Date().toISOString().split('T')[0];
    const response = await notion.databases.query({
      database_id: DATABASES.DAILY_TASKS,
      filter: {
        property: '📅 日付',
        date: { equals: today }
      }
    });

    const tasks = response.results;
    const completed = tasks.filter(task => 
      task.properties['📊 ステータス'].select?.name === '完了'
    ).length;
    
    const total = tasks.length;
    const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

    const report = `
📊 **本日の進捗レポート** (${today})
━━━━━━━━━━━━━━━━━━━━
✅ 完了タスク: ${completed}/${total}
📈 完了率: ${completionRate}%
━━━━━━━━━━━━━━━━━━━━

${completionRate >= 80 ? '🎉 素晴らしい進捗です！' : 
  completionRate >= 60 ? '👍 順調に進んでいます' : 
  '⚠️ 進捗が遅れています。サポートが必要かもしれません'}
    `;

    await sendSlackNotification(report, '#progress-reports');
    return report;
  } catch (error) {
    console.error('❌ 進捗レポート生成エラー:', error);
  }
}

// 🤖 メイン実行関数
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'create-daily-tasks':
      const date = args[1] || new Date().toISOString().split('T')[0];
      await createDailyTasks(date);
      break;
      
    case 'update-kpi':
      const kpiData = JSON.parse(args[1] || '{}');
      await updateKPIData(kpiData);
      break;
      
    case 'sync-content':
      const filePath = args[1];
      const category = args[2] || 'その他';
      if (filePath) {
        await syncContentToNotion(filePath, category);
      }
      break;
      
    case 'progress-report':
      await generateProgressReport();
      break;
      
    case 'setup-weekly-tasks':
      // 1週間分のタスクを一括作成
      for (let i = 0; i < 7; i++) {
        const date = new Date();
        date.setDate(date.getDate() + i);
        await createDailyTasks(date.toISOString().split('T')[0]);
      }
      break;
      
    default:
      console.log(`
🤖 Notion自動化スクリプト - 使用方法

コマンド:
  create-daily-tasks [日付]     - 日次タスクを作成
  update-kpi [JSONデータ]       - KPIデータを更新  
  sync-content [ファイルパス] [カテゴリ] - コンテンツを同期
  progress-report              - 進捗レポートを生成
  setup-weekly-tasks           - 1週間分のタスクを作成

例:
  node notion-automation.js create-daily-tasks 2025-09-02
  node notion-automation.js update-kpi '{"xFollowers":1500,"lineSubscribers":800}'
  node notion-automation.js sync-content "./content/post.md" "X投稿"
      `);
  }
}

// Git hooks用の関数
function setupGitHooks() {
  const hookContent = `#!/bin/sh
# Post-commit hook: Notionに変更を通知

# 変更されたファイルを取得
changed_files=$(git diff-tree --no-commit-id --name-only -r HEAD)

# マークダウンファイルの変更をNotionに同期
for file in $changed_files; do
  if [[ $file == *.md ]]; then
    node ./チーム運営/Notion自動化スクリプト.js sync-content "$file" "コンテンツ"
  fi
done

# 進捗レポートを生成
node ./チーム運営/Notion自動化スクリプト.js progress-report
`;

  fs.writeFileSync('.git/hooks/post-commit', hookContent);
  fs.chmodSync('.git/hooks/post-commit', '755');
  console.log('✅ Git hooks設定完了');
}

// スクリプトが直接実行された場合
if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  createDailyTasks,
  updateKPIData,
  syncContentToNotion,
  sendSlackNotification,
  generateProgressReport,
  setupGitHooks
};

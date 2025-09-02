const fs = require('fs');
const path = require('path');

console.log('🤖 あやねえDiscordボットのセットアップを開始します...\n');

// .envファイルの作成
const envPath = path.join(__dirname, '.env');
const envExamplePath = path.join(__dirname, 'env-example.txt');

if (!fs.existsSync(envPath)) {
  if (fs.existsSync(envExamplePath)) {
    fs.copyFileSync(envExamplePath, envPath);
    console.log('✅ .envファイルを作成しました');
    console.log('📝 .envファイルを編集して、以下の情報を設定してください：');
    console.log('   - DISCORD_TOKEN: Discordボットのトークン');
    console.log('   - GUILD_ID: DiscordサーバーのID');
  } else {
    console.log('❌ env-example.txtが見つかりません');
  }
} else {
  console.log('✅ .envファイルは既に存在します');
}

// .gitignoreファイルの作成
const gitignorePath = path.join(__dirname, '.gitignore');
const gitignoreContent = `# Environment variables
.env

# Node modules
node_modules/

# Logs
*.log
logs/

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# nyc test coverage
.nyc_output

# Dependency directories
node_modules/
jspm_packages/

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env
.env.test

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# next.js build output
.next

# nuxt.js build output
.nuxt

# vuepress build output
.vuepress/dist

# Serverless directories
.serverless

# FuseBox cache
.fusebox/

# DynamoDB Local files
.dynamodb/
`;

if (!fs.existsSync(gitignorePath)) {
  fs.writeFileSync(gitignorePath, gitignoreContent);
  console.log('✅ .gitignoreファイルを作成しました');
} else {
  console.log('✅ .gitignoreファイルは既に存在します');
}

console.log('\n🔹 次のステップ：');
console.log('1. .envファイルを編集してDiscordボットの設定を入力');
console.log('2. npm install でパッケージをインストール');
console.log('3. npm start でボットを起動');
console.log('\n詳しい手順はREADME.mdを確認してください！');

console.log('\n💎 セットアップ完了！あやねえボットの準備ができました✨');

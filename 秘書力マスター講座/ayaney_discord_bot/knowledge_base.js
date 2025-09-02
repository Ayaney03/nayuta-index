// あやねえの知識ベース - レッスン情報とQ&Aパターン

const lessonDatabase = {
  // スプレッドシート関連
  spreadsheet: {
    keywords: ['スプレッドシート', 'スプシ', 'Excel', 'エクセル', '表', 'データ', '整理', '見栄え', '色', 'フォーマット'],
    lessons: [
      {
        title: 'クライアントに信頼されるスプレッドシート資料作成術',
        url: '第8章_事例で学ぶサポート力＆提案力強化/スプレッドシート活用術/クライアントに信頼されるスプレッドシート資料作成術.md',
        description: '色の統一術、数字の体裁整理、見栄えを整えるコツ'
      },
      {
        title: 'AI活用で効率化！あやねえおすすめスプレッドシート関数10選',
        url: '第8章_事例で学ぶサポート力＆提案力強化/スプレッドシート活用術/AI活用で効率化！あやねえおすすめスプレッドシート関数10選.md',
        description: 'AIを使った関数作成、実務で使える関数10選'
      }
    ]
  },

  // 時短・効率化関連
  efficiency: {
    keywords: ['時短', '効率化', '自動化', 'AI', 'ツール', '管理', 'スケジュール', 'タスク'],
    lessons: [
      {
        title: 'ズボラ式正義。時短仕事術を生み出す3つの知恵法',
        url: '第5章_稼ぐ秘書の時短仕事術/ズボラ式正義。時短仕事術を生み出す3つの知恵法.md',
        description: '時短仕事術の基本的な考え方と実践方法'
      },
      {
        title: 'やることリストがスッと片付く、ママのための超甘やかしやることリスト作成7つの秘訣',
        url: '第5章_稼ぐ秘書の時短仕事術/やることリストがスッと片付く、ママのための超甘やかしやることリスト作成7つの秘訣.md',
        description: 'タスク管理の効率化テクニック'
      }
    ]
  },

  // コミュニケーション関連
  communication: {
    keywords: ['コミュニケーション', '連絡', 'メール', 'チャット', '返信', '催促', '指摘', 'クライアント'],
    lessons: [
      {
        title: 'インフルエンサーから学ぶ業務を前に進めるテキストコミュニケーション術',
        url: '第4章_神サポート秘書コミュニケーション術/インフルエンサーから学ぶ業務を前に進めるテキストコミュニケーション術.md',
        description: '効率的なテキストコミュニケーションの方法'
      },
      {
        title: '相手を不快にさせない指摘・催促の仕方',
        url: '第4章_神サポート秘書コミュニケーション術/相手を不快にさせない指摘・催促の仕方.md',
        description: '角の立たない指摘・催促のテクニック'
      }
    ]
  },

  // マインドセット関連
  mindset: {
    keywords: ['マインド', '考え方', '心構え', '成長', '目標', 'モチベーション', '失敗', '成功'],
    lessons: [
      {
        title: '最短最速で結果を出す人の心構え',
        url: '第2章_稼げるオンライン秘書のマインド/最短最速で結果を出す人の心構え.md',
        description: '成果を出すためのマインドセット'
      },
      {
        title: '手を挙げる勇気',
        url: '第2章_稼げるオンライン秘書のマインド/手を挙げる勇気.md',
        description: '積極的に行動するためのマインド'
      }
    ]
  },

  // 家事育児関連
  worklife: {
    keywords: ['家事', '育児', '両立', '時間', 'ママ', '子育て', '家族', '仕組み化'],
    lessons: [
      {
        title: '洗濯物畳みを卒業して年間90時間の余白を生む',
        url: '第6章_家事育児の仕組み化/洗濯物畳みを卒業して年間90時間の余白を生む.md',
        description: '家事の効率化で時間を作る方法'
      }
    ]
  },

  // 単価アップ・収入関連
  income: {
    keywords: ['単価', '収入', '稼ぐ', '値上げ', '交渉', '契約', '高単価', 'マネタイズ'],
    lessons: [
      {
        title: '高単価を目指すなら相場ではなく市場を見極めよう',
        url: '第3章_脱サラを目指す人向け/高単価を目指すなら相場ではなく市場を見極めよう.md',
        description: '高単価案件を獲得するための考え方'
      },
      {
        title: 'マネタイズ方法10選_概要',
        url: '第9章_稼ぎ方の多様性・マネタイズ戦略/マネタイズ方法10選_概要.md',
        description: '収入の柱を増やす方法'
      }
    ]
  }
};

// あやねえの回答パターン
const responsePatterns = {
  // スプレッドシート関連の質問
  spreadsheet_formatting: {
    response: `💎 スプレッドシートの見栄え整理、めっちゃ大事ですよね！

🔹 **色を揃えるコツ**
同じ階層の色を選ぶだけで統一感がグッと出ます。
青=ポジティブ、赤=注意で使い分けると、クライアントも直感的に理解しやすい！

🔹 **数字の体裁**
3桁区切りと右揃えは絶対やって。これだけで「この人、仕事丁寧だな」って思ってもらえます。

詳しいテクニックはこちらのレッスンで解説してるので、ぜひチェックしてみて✨`,
    lessons: ['spreadsheet']
  },

  // 時短・効率化の質問
  time_management: {
    response: `💎 時短術、これは秘書の生命線ですよね！

私も3児ママで1日10時間睡眠取りながら月収100万達成してるので、時短は本当に大切。

🔹 **基本の考え方**
「ズボラ式正義」って私は呼んでるんですが、完璧を目指さずに「これで十分」のラインを見極めるのがコツ。

🔹 **具体的なテクニック**
やることリストも「甘やかし」方式で作ると、スッと片付くようになりますよ！

実践的な方法はレッスンで詳しく説明してるので、ぜひ見てみてくださいね。`,
    lessons: ['efficiency']
  },

  // コミュニケーション関連
  client_communication: {
    response: `💎 クライアントとのコミュニケーション、これは本当に重要！

私の基本スタンスは「即レスより、少ないやり取りで完結する」コミュニケーション。

🔹 **ポイント**
- 許可を取るより事後報告（責任取る前提で）
- 返信スピードより、コミュニケーションの精度
- 先回り思考で相手の手間を減らす

指摘や催促も、相手を不快にさせないテクニックがあるんです。
詳しいやり方はレッスンで解説してるので、チェックしてみて！`,
    lessons: ['communication']
  },

  // 一般的な励まし・アドバイス
  general_advice: {
    response: `💎 その気持ち、すごくわかります！

秘書って「替えの効かない最強の右腕」を目指すお仕事だから、悩むこともあって当然。

🔹 **大切なのは**
「お客さんマインド」から抜け出して、責任を取りに行く行動力を身につけること。

失敗しても大丈夫。私も散々失敗してきたけど、そこから学んで改善していけば必ず成長できます。

まずは行動→改善のサイクルを回していきましょう！
具体的な方法はレッスンにたくさんあるので、ぜひ活用してくださいね✨`
  }
};

// キーワードマッチング関数
function findRelevantLessons(userMessage) {
  const message = userMessage.toLowerCase();
  const relevantLessons = [];
  
  for (const [category, data] of Object.entries(lessonDatabase)) {
    const hasKeyword = data.keywords.some(keyword => 
      message.includes(keyword.toLowerCase())
    );
    
    if (hasKeyword) {
      relevantLessons.push(...data.lessons);
    }
  }
  
  return relevantLessons;
}

// 回答パターンマッチング関数
function getResponsePattern(userMessage) {
  const message = userMessage.toLowerCase();
  
  // スプレッドシート関連
  if (message.includes('スプレッドシート') || message.includes('スプシ') || 
      message.includes('データ') && (message.includes('整理') || message.includes('見栄え'))) {
    return responsePatterns.spreadsheet_formatting;
  }
  
  // 時短・効率化関連
  if (message.includes('時短') || message.includes('効率') || message.includes('時間')) {
    return responsePatterns.time_management;
  }
  
  // コミュニケーション関連
  if (message.includes('クライアント') && (message.includes('連絡') || message.includes('コミュニケーション'))) {
    return responsePatterns.client_communication;
  }
  
  // デフォルト
  return responsePatterns.general_advice;
}

module.exports = {
  lessonDatabase,
  responsePatterns,
  findRelevantLessons,
  getResponsePattern
};

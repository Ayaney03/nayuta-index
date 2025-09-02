// 年間決済日マッピングデータ
const annualPaymentDatesMapping = [
    '2024-03-01', // M001 藤澤秀彰
    '', // M002 鈴木裕介 - 空欄
    '2024-03-08', // M003 福井康大
    '', // M004 俵健太郎 - 空欄
    '2024-02-28', // M005 進藤勇輝
    '', '', '', '', // M006-M010 - 空欄x4
    '2024-02-12', // M011 根塚陽己
    '2024-03-01', // M012 藤原綜太郎
    '2024-02-09', // M013 石島秀峰
    '', '', // M014-M015 - 空欄x2
    '2024-02-21', // M016 湊翔太郎
    '2024-02-10', // M017 鈴木菜摘
    '', // M018 松島徹 - 空欄
    '2024-02-05', // M019 粟津律子
    '', '', // M020-M021 - 空欄x2
    '2025-02-04', // M022 ブル
    '', '', // M023-M024 - 空欄x2
    '2024-11-02', // M025 池本湊了汰
    '', '', // M026-M027 - 空欄x2
    '2024-02-26', // M028 山縣誠二
    '', '', '', '', '', '', '', '', '', '', '', '', // M029-M040 - 空欄x12
    '2024-07-01', // M041 増田凌一
    '', '', '', '', '', '', '', '', // M042-M049 - 空欄x8
    '2024-05-16', // M050 平岩遼志
    '2024-05-18', // M051 佐藤一気
    '', '', '', '', '', '', // M052-M057 - 空欄x6
    '2025-01-16', // M058 小島啓輔
    '2025-02-12', // M059 尾崎勇哉
    '', '', // M060-M061 - 空欄x2
    '2506', // M062 日高悠河 (年省略形式)
    '', '', '', // M063-M065 - 空欄x3
    '2024-12-04', // M066 長田一
    '', '', // M067-M068 - 空欄x2
    '2506', // M069 中西航平 (年省略形式)
    '2024-10-25', // M070 熊谷瑞奈美
    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', // M071-M086 - 空欄x16
    '2024-10-30', // M087 藤井徹
    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', // M088-M111 - 空欄x24
];

// 年間決済日の次回更新日を計算する関数
function calculateNextPaymentDate(paymentDate) {
    if (!paymentDate) return null;
    
    // 年省略形式（2506など）の処理
    if (paymentDate.length === 4 && paymentDate.startsWith('25')) {
        const month = paymentDate.substring(2);
        paymentDate = `2025-${month.padStart(2, '0')}-01`;
    }
    
    try {
        const lastPayment = new Date(paymentDate);
        const nextPayment = new Date(lastPayment);
        nextPayment.setFullYear(nextPayment.getFullYear() + 1);
        return nextPayment.toISOString().split('T')[0];
    } catch (error) {
        return null;
    }
}

// 年間決済の更新状況を判定する関数
function getPaymentStatus(paymentDate) {
    if (!paymentDate) return { status: '未設定', color: '#6c757d' };
    
    const nextPayment = calculateNextPaymentDate(paymentDate);
    if (!nextPayment) return { status: 'エラー', color: '#dc3545' };
    
    const today = new Date();
    const nextPaymentDate = new Date(nextPayment);
    const daysUntilPayment = Math.ceil((nextPaymentDate - today) / (1000 * 60 * 60 * 24));
    
    if (daysUntilPayment < 0) {
        return { status: '更新必要', color: '#dc3545', daysOverdue: Math.abs(daysUntilPayment) };
    } else if (daysUntilPayment <= 30) {
        return { status: '更新間近', color: '#ffc107', daysUntil: daysUntilPayment };
    } else if (daysUntilPayment <= 90) {
        return { status: '要注意', color: '#fd7e14', daysUntil: daysUntilPayment };
    } else {
        return { status: '正常', color: '#28a745', daysUntil: daysUntilPayment };
    }
}

// メンバーデータベースに年間決済情報を追加する関数
function updateMembersWithAnnualPayments(membersDatabase) {
    return membersDatabase.map((member, index) => {
        const paymentDate = annualPaymentDatesMapping[index] || '';
        const nextPaymentDate = calculateNextPaymentDate(paymentDate);
        const paymentStatus = getPaymentStatus(paymentDate);
        
        return {
            ...member,
            annualPaymentDate: paymentDate, // 最新の年間決済日
            nextPaymentDate: nextPaymentDate, // 次回更新予定日
            paymentStatus: paymentStatus.status, // 更新ステータス
            paymentStatusColor: paymentStatus.color, // ステータス色
            daysUntilPayment: paymentStatus.daysUntil, // 更新まで日数
            daysOverdue: paymentStatus.daysOverdue, // 期限切れ日数
            // 年間会員かどうかの判定
            isAnnualMember: member.currentStatus === '年間' && paymentDate !== ''
        };
    });
}

// 年間決済統計を計算する関数
function calculateAnnualPaymentStats(membersDatabase) {
    const stats = {
        total: 0,
        normal: 0,      // 正常
        attention: 0,   // 要注意
        upcoming: 0,    // 更新間近
        overdue: 0      // 更新必要
    };

    membersDatabase.forEach(member => {
        if (member.isAnnualMember) {
            stats.total++;
            switch(member.paymentStatus) {
                case '正常':
                    stats.normal++;
                    break;
                case '要注意':
                    stats.attention++;
                    break;
                case '更新間近':
                    stats.upcoming++;
                    break;
                case '更新必要':
                    stats.overdue++;
                    break;
            }
        }
    });

    return stats;
}

console.log('Annual payment dates mapping loaded. Use updateMembersWithAnnualPayments() to apply.');

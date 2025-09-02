import csv
import json
from collections import defaultdict

# CSVデータを読み込み
product_data = defaultdict(list)

with open('決済-20250824-114821.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    for row in reader:
        if len(row) > 12:
            metadata_sources = [row[11], row[12]] if len(row) > 11 else [row[12]]
            
            for metadata_str in metadata_sources:
                if metadata_str:
                    try:
                        metadata = json.loads(metadata_str)
                        if 'product_detail_name' in metadata:
                            product = metadata['product_detail_name']
                            customer = metadata.get('customer_name') or metadata.get('univapay-name', '不明')
                            amount = row[7] if len(row) > 7 else row[5] if len(row) > 5 else ''
                            status = row[9] if len(row) > 9 else ''
                            event = row[16] if len(row) > 16 else ''
                            date = row[4] if len(row) > 4 else ''
                            
                            product_data[product].append({
                                'customer': customer,
                                'amount': amount,
                                'status': status,
                                'event': event,
                                'date': date
                            })
                            break
                    except:
                        pass

# 統計情報を計算
total_customers = sum(len(customers) for customers in product_data.values())
success_count = 0
failed_count = 0
refund_count = 0

for customers in product_data.values():
    for customer in customers:
        if customer['status'] == '成功' and customer['event'] == '売上':
            success_count += 1
        elif customer['status'] == '失敗' or '失敗' in customer['event']:
            failed_count += 1
        elif customer['event'] == '返金':
            refund_count += 1

# HTMLチェックシートを生成
html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>決済データ チェックシート</title>
    <style>
        body {{
            font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .product-section {{
            margin: 30px 0;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}
        .product-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            font-size: 18px;
            font-weight: bold;
        }}
        .product-content {{
            padding: 20px;
        }}
        .customer-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }}
        .customer-item {{
            display: flex;
            align-items: center;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            background: #fafafa;
            transition: all 0.3s ease;
        }}
        .customer-item:hover {{
            background: #f0f0f0;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .status-success {{
            border-left: 4px solid #4CAF50;
            background: #f1f8e9;
        }}
        .status-failed {{
            border-left: 4px solid #f44336;
            background: #ffebee;
        }}
        .status-refund {{
            border-left: 4px solid #ff9800;
            background: #fff3e0;
        }}
        .checkbox {{
            margin-right: 12px;
            width: 18px;
            height: 18px;
            cursor: pointer;
        }}
        .customer-info {{
            flex: 1;
        }}
        .customer-name {{
            font-weight: bold;
            font-size: 14px;
            color: #333;
        }}
        .customer-details {{
            font-size: 12px;
            color: #666;
            margin-top: 4px;
        }}
        .status-badge {{
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
            margin-left: 8px;
        }}
        .badge-success {{
            background: #4CAF50;
            color: white;
        }}
        .badge-failed {{
            background: #f44336;
            color: white;
        }}
        .badge-refund {{
            background: #ff9800;
            color: white;
        }}
        .summary {{
            background: #e8f5e8;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
            text-align: center;
        }}
        .summary-stats {{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        }}
        .stat-label {{
            font-size: 12px;
            color: #666;
        }}
        @media (max-width: 768px) {{
            .customer-grid {{
                grid-template-columns: 1fr;
            }}
            .summary-stats {{
                flex-direction: column;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏪 決済データ チェックシート</h1>
        
        <div class="summary">
            <div class="summary-stats">
                <div class="stat-item">
                    <div class="stat-number">{len(product_data)}</div>
                    <div class="stat-label">商品種類</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{total_customers}</div>
                    <div class="stat-label">総決済件数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{success_count}</div>
                    <div class="stat-label">成功</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{failed_count}</div>
                    <div class="stat-label">失敗</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{refund_count}</div>
                    <div class="stat-label">返金</div>
                </div>
            </div>
        </div>
'''

# 商品ごとのセクションを生成
for product in sorted(product_data.keys()):
    customers = sorted(product_data[product], key=lambda x: x['customer'])
    
    # 商品の価格を取得（最初の顧客から）
    price = customers[0]['amount'] if customers else ''
    
    html_content += f'''
        <div class="product-section">
            <div class="product-header">
                {product} ({price}円) - {len(customers)}件
            </div>
            <div class="product-content">
                <div class="customer-grid">
    '''
    
    for customer in customers:
        # ステータスに応じてクラスを設定
        if customer['status'] == '成功' and customer['event'] == '売上':
            status_class = 'status-success'
            badge_class = 'badge-success'
            status_text = '✅ 成功'
        elif customer['status'] == '失敗' or '失敗' in customer['event']:
            status_class = 'status-failed'
            badge_class = 'badge-failed'
            status_text = '❌ 失敗'
        elif customer['event'] == '返金':
            status_class = 'status-refund'
            badge_class = 'badge-refund'
            status_text = '↩️ 返金'
        else:
            status_class = ''
            badge_class = 'badge-success'
            status_text = '⚪ その他'
        
        date_short = customer['date'][:10] if len(customer['date']) >= 10 else customer['date']
        
        html_content += f'''
                    <div class="customer-item {status_class}">
                        <input type="checkbox" class="checkbox">
                        <div class="customer-info">
                            <div class="customer-name">{customer['customer']}</div>
                            <div class="customer-details">{date_short} | {customer['event']}</div>
                        </div>
                        <span class="status-badge {badge_class}">{status_text}</span>
                    </div>
        '''
    
    html_content += '''
                </div>
            </div>
        </div>
    '''

html_content += '''
    </div>
    
    <script>
        // チェックボックスの状態を保存
        document.addEventListener('DOMContentLoaded', function() {
            const checkboxes = document.querySelectorAll('.checkbox');
            checkboxes.forEach((checkbox, index) => {
                const savedState = localStorage.getItem('checkbox_' + index);
                if (savedState === 'true') {
                    checkbox.checked = true;
                }
                
                checkbox.addEventListener('change', function() {
                    localStorage.setItem('checkbox_' + index, this.checked);
                });
            });
        });
    </script>
</body>
</html>
'''

# HTMLファイルを保存
with open('決済データチェックシート.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('✅ チェックシートを作成しました！')
print('📄 ファイル名: 決済データチェックシート.html')
print(f'📊 統計: {len(product_data)}商品, {total_customers}件, 成功{success_count}件, 失敗{failed_count}件, 返金{refund_count}件')

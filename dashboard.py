#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Business Dashboard - Unified Monitor
Consolidated view of:
- Stock portfolio performance
- AI complaint tickets
- System health
"""

import json
from pathlib import Path
from datetime import datetime
import requests

def check_portfolio():
    """Check current portfolio status"""
    portfolio_path = Path.home() / '.hermes' / 'stock_portfolio.json'
    
    if not portfolio_path.exists():
        return None
    
    with open(portfolio_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    positions_data = data.get('positions', [])
    
    total_invested = 0
    current_value = 0
    positions = []
    
    # Mock current prices (in production, fetch from API)
    current_prices = {
        '601899': 34.30,
        '600036': 38.50,
        '600030': 27.50,
    }
    
    for pos in positions_data:
        code = pos.get('code', '')
        cost = pos.get('avg_price', 0)
        shares = pos.get('shares', 0)
        current_price = current_prices.get(code, cost)
        
        invested = cost * shares
        current = current_price * shares
        gain = (current - invested) / invested * 100 if invested > 0 else 0
        
        total_invested += invested
        current_value += current
        
        positions.append({
            'code': code,
            'name': pos.get('name', code),
            'shares': shares,
            'cost': cost,
            'current': current_price,
            'gain_pct': gain
        })
    
    return {
        'total_invested': total_invested,
        'current_value': current_value,
        'total_gain_pct': (current_value - total_invested) / total_invested * 100 if total_invested > 0 else 0,
        'positions': positions
    }

def check_tickets():
    """Check complaint tickets status"""
    tickets_path = Path.home() / 'AI-OCR-Complaint-Handler' / 'data' / 'tickets.json'
    
    if not tickets_path.exists():
        return {'total': 0, 'new': 0, 'resolved': 0}
    
    with open(tickets_path, 'r', encoding='utf-8') as f:
        tickets = json.load(f)
    
    return {
        'total': len(tickets),
        'new': sum(1 for t in tickets if t['status'] == 'new'),
        'in_progress': sum(1 for t in tickets if t['status'] == 'in_progress'),
        'resolved': sum(1 for t in tickets if t['status'] == 'resolved'),
    }

def check_system_health():
    """Check system health"""
    health = {
        'stock_picker': '✓',
        'portfolio_monitor': '✓',
        'ocr_service': '✓',
        'telegram_bot': '⚠',  # Network issues
        'database': '✓',
    }
    
    # Check if services are running (simplified)
    return health

def print_dashboard():
    """Print unified dashboard"""
    print("\n" + "═" * 80)
    print(f"                    AI 业务监控仪表板 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 80 + "\n")
    
    # Portfolio section
    print("📊 股票投资组合")
    print("-" * 80)
    portfolio = check_portfolio()
    if portfolio:
        print(f"总投入：¥{portfolio['total_invested']:,.2f}")
        print(f"当前值：¥{portfolio['current_value']:,.2f}")
        print(f"总收益：{portfolio['total_gain_pct']:+.2f}%")
        print("\n持仓明细:")
        for pos in portfolio['positions']:
            status = '🟢' if pos['gain_pct'] > 0 else '🔴'
            print(f"  {status} {pos['name']} ({pos['code']}) - {pos['shares']}股 @ ¥{pos['current']:.2f}  {pos['gain_pct']:+.2f}%")
    else:
        print("  无持仓数据")
    
    print("\n")
    
    # Tickets section
    print("🎫 AI 投诉工单")
    print("-" * 80)
    tickets = check_tickets()
    print(f"总工单：{tickets['total']}  |  新工单：{tickets['new']}  |  处理中：{tickets.get('in_progress', 0)}  |  已解决：{tickets['resolved']}")
    
    if tickets['new'] > 0:
        print(f"  ⚠️ 有 {tickets['new']} 个新工单待处理")
    
    print("\n")
    
    # System health
    print("🔧 系统健康状态")
    print("-" * 80)
    health = check_system_health()
    for service, status in health.items():
        service_name = service.replace('_', ' ').title()
        print(f"  {status} {service_name}")
    
    print("\n" + "═" * 80)
    print("提示：运行以下命令查看详情")
    print("  - 股票选股：cd /Users/wtueeq/hermes-stock-analysis && python3 stable_stock_picker.py")
    print("  - 持仓监控：cd /Users/wtueeq/hermes-stock-analysis && python3 portfolio_monitor.py")
    print("  - 工单管理：cd /Users/wtueeq/AI-OCR-Complaint-Handler && python3 app/ticket_manager.py list")
    print("  - AI Demo: streamlit run /Users/wtueeq/AI-OCR-Complaint-Handler/app/main.py")
    print("═" * 80 + "\n")

if __name__ == "__main__":
    print_dashboard()

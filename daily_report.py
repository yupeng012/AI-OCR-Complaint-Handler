#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Daily Report Generator
Generates comprehensive daily reports for:
- Portfolio performance
- Trading activities
- AI complaint tickets
- System health
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
import requests

class DailyReportGenerator:
    def __init__(self):
        self.report_dir = Path.home() / 'Desktop' / 'Yupeng AI 每日晨报'
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        self.portfolio_path = Path.home() / '.hermes' / 'stock_portfolio.json'
        self.trade_log_path = Path.home() / '.hermes' / 'trade_log.json'
        self.tickets_path = Path.home() / 'AI-OCR-Complaint-Handler' / 'data' / 'tickets.json'
    
    def get_portfolio_summary(self):
        """Get portfolio summary"""
        if not self.portfolio_path.exists():
            return None
        
        with open(self.portfolio_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        positions = data.get('positions', [])
        total_invested = sum(pos.get('avg_price', 0) * pos.get('shares', 0) for pos in positions)
        
        # Mock current prices (in production, fetch from API)
        current_prices = {
            '601899': 34.30,
            '600036': 38.50,
            '600030': 27.50,
        }
        
        current_value = sum(
            current_prices.get(pos.get('code', ''), pos.get('avg_price', 0)) * pos.get('shares', 0)
            for pos in positions
        )
        
        gain_pct = (current_value - total_invested) / total_invested * 100 if total_invested > 0 else 0
        
        return {
            'total_invested': total_invested,
            'current_value': current_value,
            'gain_pct': gain_pct,
            'positions': positions,
            'cash': data.get('cash', 0),
        }
    
    def get_today_trades(self):
        """Get today's trades"""
        if not self.trade_log_path.exists():
            return []
        
        with open(self.trade_log_path, 'r', encoding='utf-8') as f:
            trades = json.load(f)
        
        today = datetime.now().strftime('%Y-%m-%d')
        today_trades = [t for t in trades if t.get('timestamp', '')[:10] == today]
        
        return today_trades
    
    def get_ticket_summary(self):
        """Get ticket summary"""
        if not self.tickets_path.exists():
            return {'total': 0, 'new': 0, 'resolved': 0}
        
        with open(self.tickets_path, 'r', encoding='utf-8') as f:
            tickets = json.load(f)
        
        today = datetime.now().strftime('%Y-%m-%d')
        today_tickets = [t for t in tickets if t.get('timestamp', '')[:10] == today]
        
        return {
            'total': len(tickets),
            'new_today': len(today_tickets),
            'new': sum(1 for t in tickets if t['status'] == 'new'),
            'in_progress': sum(1 for t in tickets if t['status'] == 'in_progress'),
            'resolved': sum(1 for t in tickets if t['status'] == 'resolved'),
        }
    
    def generate_report(self):
        """Generate daily report"""
        today = datetime.now().strftime('%Y-%m-%d')
        weekday = datetime.now().strftime('%A')
        
        # Get data
        portfolio = self.get_portfolio_summary()
        trades = self.get_today_trades()
        tickets = self.get_ticket_summary()
        
        # Build report
        report = []
        report.append("=" * 80)
        report.append(f"AI 业务日报 - {today} ({weekday})")
        report.append("=" * 80)
        report.append("")
        
        # Portfolio section
        report.append("📊 投资组合表现")
        report.append("-" * 80)
        if portfolio:
            report.append(f"总投入：¥{portfolio['total_invested']:,.2f}")
            report.append(f"当前值：¥{portfolio['current_value']:,.2f}")
            report.append(f"收益率：{portfolio['gain_pct']:+.2f}%")
            report.append(f"可用现金：¥{portfolio['cash']:,.2f}")
            report.append("")
            report.append("持仓明细:")
            
            current_prices = {
                '601899': 34.30,
                '600036': 38.50,
                '600030': 27.50,
            }
            
            for pos in portfolio['positions']:
                code = pos.get('code', '')
                name = pos.get('name', code)
                shares = pos.get('shares', 0)
                cost = pos.get('avg_price', 0)
                current = current_prices.get(code, cost)
                gain = (current - cost) / cost * 100
                status = '🟢' if gain > 0 else '🔴'
                report.append(f"  {status} {name}: {shares}股 @ ¥{current:.2f} ({gain:+.2f}%)")
        else:
            report.append("无持仓数据")
        
        report.append("")
        
        # Trades section
        report.append("💼 今日交易")
        report.append("-" * 80)
        if trades:
            for trade in trades:
                action = '买入' if trade.get('action') == 'buy' else '卖出'
                report.append(f"  {action} {trade.get('name', '')} {trade.get('quantity', 0)}股 @ ¥{trade.get('price', 0):.2f}")
        else:
            report.append("  今日无交易")
        
        report.append("")
        
        # Tickets section
        report.append("🎫 AI 工单统计")
        report.append("-" * 80)
        report.append(f"总工单数：{tickets.get('total', 0)}")
        report.append(f"今日新增：{tickets.get('new_today', 0)}")
        report.append(f"待处理：{tickets.get('new', 0)}")
        report.append(f"已解决：{tickets.get('resolved', 0)}")
        
        report.append("")
        
        # Market outlook (simplified)
        report.append("📈 市场展望")
        report.append("-" * 80)
        report.append("当前市场整体震荡，建议保持观望，等待更好机会。")
        report.append("关注评分达到 6.0+ 的优质标的。")
        
        report.append("")
        report.append("=" * 80)
        report.append(f"报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        
        report_text = '\n'.join(report)
        
        # Save report
        filename = f"Daily_Report_{today}.md"
        filepath = self.report_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"✓ 日报已生成：{filepath}")
        print("\n" + report_text)
        
        return filepath

if __name__ == "__main__":
    generator = DailyReportGenerator()
    generator.generate_report()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ticket Management System CLI
Manage complaint tickets: list, update, resolve, notify
"""

import json
from pathlib import Path
from datetime import datetime
import requests
import sys

class TicketManager:
    def __init__(self):
        self.data_dir = Path.home() / 'AI-OCR-Complaint-Handler' / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.tickets_file = self.data_dir / 'tickets.json'
        self.tickets = self.load_tickets()
        
        # Telegram config
        self.telegram_enabled = True
        self.telegram_token = "7399788056:MAF_6kL6g4jFkZqKqKqKqKqKqKqK"  # Mock
        self.chat_id = "-1001234567890"  # Mock
    
    def load_tickets(self):
        if self.tickets_file.exists():
            with open(self.tickets_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_tickets(self):
        with open(self.tickets_file, 'w', encoding='utf-8') as f:
            json.dump(self.tickets, f, indent=2, ensure_ascii=False)
    
    def list_tickets(self, status=None):
        """List all tickets"""
        print(f"\n{'='*80}")
        print("工单管理系统")
        print(f"{'='*80}\n")
        
        filtered = self.tickets
        if status:
            filtered = [t for t in self.tickets if t['status'] == status]
        
        if not filtered:
            print("暂无工单")
            return
        
        print(f"{'工单号':<20} {'时间':<20} {'类型':<12} {'优先级':<8} {'状态':<12}")
        print("-" * 80)
        
        for ticket in filtered:
            print(f"{ticket['ticket_id']:<20} {ticket['timestamp'][:19]:<20} {ticket['category']:<12} {ticket['priority']:<8} {ticket['status']:<12}")
        
        print(f"\n总计：{len(filtered)} 个工单")
    
    def update_ticket(self, ticket_id, status=None, notes=None):
        """Update a ticket"""
        found = False
        for ticket in self.tickets:
            if ticket['ticket_id'] == ticket_id:
                found = True
                if status:
                    ticket['status'] = status
                if notes:
                    ticket['notes'].append({
                        'timestamp': datetime.now().isoformat(),
                        'note': notes
                    })
                break
        
        if found:
            self.save_tickets()
            print(f"✓ 工单 {ticket_id} 已更新")
        else:
            print(f"✗ 工单 {ticket_id} 不存在")
    
    def send_telegram_notification(self, ticket):
        """Send new ticket notification to Telegram"""
        if not self.telegram_enabled:
            return
        
        message = f"""
🔔 <b>新投诉工单</b>

工单号：{ticket['ticket_id']}
时间：{ticket['timestamp'][:19]}
类型：{ticket['category']}
优先级：{ticket['priority']}
情感：{ticket['sentiment']} ({ticket['sentiment_score']:.2f})

请尽快处理！
"""
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            resp = requests.post(url, json=data, timeout=5)
            if resp.status_code == 200:
                print(f"✓ Telegram 通知已发送")
            else:
                print(f"✗ Telegram 发送失败：{resp.status_code}")
        except Exception as e:
            print(f"✗ Telegram 通知失败：{e}")
    
    def generate_report(self):
        """Generate daily report"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        total = len(self.tickets)
        new_count = sum(1 for t in self.tickets if t['status'] == 'new')
        resolved_count = sum(1 for t in self.tickets if t['status'] == 'resolved')
        
        # By category
        by_category = {}
        for ticket in self.tickets:
            cat = ticket['category']
            by_category[cat] = by_category.get(cat, 0) + 1
        
        print(f"\n{'='*80}")
        print(f"每日工单报告 - {today}")
        print(f"{'='*80}")
        print(f"总工单数：{total}")
        print(f"新工单：{new_count}")
        print(f"已解决：{resolved_count}")
        print(f"\n按类型分布:")
        for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}")
        
        return {
            'date': today,
            'total': total,
            'new': new_count,
            'resolved': resolved_count,
            'by_category': by_category
        }

if __name__ == "__main__":
    manager = TicketManager()
    
    if len(sys.argv) < 2:
        print("用法：python ticket_manager.py [list|update|report] [args]")
        print("  list [status]  - 列出工单")
        print("  update <id> <status> - 更新工单状态")
        print("  report - 生成日报")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        manager.list_tickets(status)
    
    elif command == 'update':
        if len(sys.argv) < 4:
            print("用法：python ticket_manager.py update <ticket_id> <status>")
            sys.exit(1)
        ticket_id = sys.argv[2]
        status = sys.argv[3]
        manager.update_ticket(ticket_id, status=status)
    
    elif command == 'report':
        manager.generate_report()

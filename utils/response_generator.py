"""
Response Generator - Auto Response Generation
Generates professional responses to complaints
"""

def generate_response(ticket):
    """
    Generate professional response based on ticket
    
    Args:
        ticket: Ticket dictionary with category, sentiment, etc.
    
    Returns:
        str: Generated response text
    """
    category = ticket.get('category', 'Other')
    sentiment = ticket.get('sentiment', 'neutral')
    ticket_id = ticket.get('ticket_id', 'UNKNOWN')
    
    # Response templates by category
    templates = {
        'Product Quality': """## Response Plan

**Category**: Product Quality Issue  
**Ticket ID**: {ticket_id}  
**Priority**: {priority}

### Action Items:
1. Apologize sincerely for the quality issue
2. Offer immediate replacement or refund
3. Arrange free return shipping
4. Provide compensation coupon
5. Escalate to quality control team

### Suggested Response:
> Dear Valued Customer,
>
> We sincerely apologize for the quality issue you experienced with your recent purchase. 
> This is not the standard we uphold, and we take full responsibility.
>
> We would like to:
> 1. Immediately send you a replacement at no cost
> 2. Provide a prepaid return label for the defective item
> 3. Offer a 20% discount coupon for your next purchase
>
> Your satisfaction is our priority. We will investigate this matter thoroughly.
>
> Best regards,  
> Customer Care Team
> Ticket Reference: {ticket_id}
> """,
        
        'Customer Service': """## Response Plan

**Category**: Customer Service Issue  
**Ticket ID**: {ticket_id}  
**Priority**: {priority}

### Action Items:
1. Sincere apology for poor service experience
2. Investigate the incident with specific staff
3. Provide additional training to team
4. Offer service recovery gesture
5. Follow-up call from manager

### Suggested Response:
> Dear Valued Customer,
>
> We deeply apologize for the unacceptable service you received. This does not 
> reflect our values, and we are taking immediate action.
>
> We are:
> 1. Investigating this incident with our team
> 2. Providing additional training to prevent recurrence
> 3. Offering you a $50 credit as a gesture of goodwill
>
> We value your business and want to earn back your trust.
>
> Sincerely,  
> Customer Experience Manager  
> Ticket Reference: {ticket_id}
> """,
        
        'Shipping & Logistics': """## Response Plan

**Category**: Shipping & Logistics  
**Ticket ID**: {ticket_id}  
**Priority**: {priority}

### Action Items:
1. Apologize for shipping delay/damage
2. Track and investigate with carrier
3. Expedite replacement if needed
4. File claim with logistics provider
5. Offer shipping credit

### Suggested Response:
> Dear Customer,
>
> We apologize for the shipping issue with your order. We understand your frustration.
>
> We are:
> 1. Investigating with our logistics partner
> 2. Sending a replacement via express shipping (free)
> 3. Providing a shipping credit for the inconvenience
>
> Your order is important to us.
>
> Best regards,  
> Logistics Team  
> Ticket Reference: {ticket_id}
> """,
        
        'Refund & Return': """## Response Plan

**Category**: Refund & Return Request  
**Ticket ID**: {ticket_id}  
**Priority**: {priority}

### Action Items:
1. Process refund immediately
2. Provide return shipping label
3. Confirm refund timeline
4. Offer exchange alternative
5. Follow up to ensure satisfaction

### Suggested Response:
> Dear Customer,
>
> We have processed your refund request. The amount will be credited within 3-5 business days.
>
> Next Steps:
> 1. Attached is your prepaid return label
> 2. Refund will be processed upon receipt
> 3. Alternative: We can offer an exchange with free upgrade
>
> We appreciate your patience.
>
> Best regards,  
> Returns Department  
> Ticket Reference: {ticket_id}
> """,
        
        'False Advertising': """## Response Plan

**Category**: False Advertising Concern  
**Ticket ID**: {ticket_id}  
**Priority**: {priority}

### Action Items:
1. Acknowledge concern seriously
2. Review advertising materials
3. Clarify product specifications
4. Offer remedy (refund/exchange)
5. Update marketing if needed

### Suggested Response:
> Dear Customer,
>
> Thank you for bringing this to our attention. We take advertising accuracy seriously.
>
> We are:
> 1. Reviewing the product description in question
> 2. Clarifying specifications on our website
> 3. Offering you a full refund or exchange
>
> We appreciate your feedback helping us improve.
>
> Sincerely,  
> Marketing Team  
> Ticket Reference: {ticket_id}
> """,
        
        'Other': """## Response Plan

**Category**: Other  
**Ticket ID**: {ticket_id}  
**Priority**: {priority}

### Action Items:
1. Acknowledge customer concern
2. Investigate specific issue
3. Provide appropriate solution
4. Follow up for satisfaction

### Suggested Response:
> Dear Customer,
>
> Thank you for contacting us. We have received your concern and are reviewing it carefully.
>
> A member of our team will respond within 24 hours with a resolution.
>
> Ticket Reference: {ticket_id}
>
> Best regards,  
> Customer Care Team
> """
    }
    
    # Determine priority
    if sentiment == 'negative':
        priority = '🔴 High'
    elif sentiment == 'neutral':
        priority = '🟡 Medium'
    else:
        priority = '🟢 Low'
    
    # Get template
    template = templates.get(category, templates['Other'])
    
    # Format with ticket_id and priority
    response = template.format(
        ticket_id=ticket_id,
        priority=priority
    )
    
    return response

def generate_response_simple(category):
    """
    Simple response generator
    
    Args:
        category: Complaint category
    
    Returns:
        str: Simple response
    """
    responses = {
        'Product Quality': 'We apologize for the quality issue. We will send a replacement immediately.',
        'Customer Service': 'We apologize for the poor service. We are addressing this with our team.',
        'Shipping & Logistics': 'We apologize for the shipping issue. We are expediting your replacement.',
        'Refund & Return': 'Your refund has been processed. Thank you for your patience.',
        'False Advertising': 'Thank you for the feedback. We are reviewing our product descriptions.'
    }
    
    return responses.get(category, 'Thank you for your feedback. We will address this issue.')

if __name__ == "__main__":
    # Test response generation
    test_ticket = {
        'ticket_id': 'TS20260511001',
        'category': 'Product Quality',
        'sentiment': 'negative'
    }
    
    response = generate_response(test_ticket)
    print(response)

"""
FAST VECTORSTORE POPULATION - OPTIMIZED FOR SPEED
Quickly populate vector database with batched processing
Works across all systems (Windows, Linux, Mac)
"""
import asyncio
import sys
from pathlib import Path
from typing import List, Dict
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.embedding_service import embedding_service
from app.services.rag_service import rag_service
from app.core.logging import logger


# Comprehensive SOP Documents
SOP_DOCUMENTS = [
    {
        "id": "upi_fraud",
        "title": "UPI/Digital Payment Fraud Complete Procedure",
        "category": "financial_fraud",
        "content": """UPI/DIGITAL PAYMENT FRAUD - IMMEDIATE ACTIONS:
1. CALL 1930 IMMEDIATELY (24x7 Financial Cyber Fraud Helpline)
2. Report on https://cybercrime.gov.in within 24 hours
3. Contact your bank customer care to freeze transaction
4. Take screenshots of all transaction details and messages
5. DO NOT delete any evidence (SMS, call logs, screenshots)

STEP-BY-STEP REPORTING:
→ Visit cybercrime.gov.in
→ Click "Report Other Cybercrimes"
→ Select "Online Financial Fraud" → "UPI Related Fraud"
→ Provide: Transaction ID, Amount, Fraudster UPI/Phone, Screenshots
→ Submit complaint and note reference number (CCN2025XXXXX)

EVIDENCE TO COLLECT:
✓ UPI transaction screenshot with UTR number
✓ Bank SMS alerts
✓ Chat/message screenshots from fraudster
✓ Fraudster's UPI ID/phone number
✓ Timeline of events

BANK ACTIONS:
- Immediately call bank customer care
- Request transaction reversal/chargeback
- File written complaint at branch within 3 days
- Request blocking of fraudulent account
- Get complaint reference number

FOLLOW-UP:
- Track on cybercrime portal using reference number
- Escalate to State Nodal Officer if no response in 15 days
- Contact Banking Ombudsman if bank doesn't resolve in 30 days
- File FIR at cyber cell if amount > ₹1 lakh"""
    },
    {
        "id": "social_media_hack",
        "title": "Social Media Account Hacking - Complete SOP",
        "category": "hacking",
        "content": """SOCIAL MEDIA HACKING - IMMEDIATE RECOVERY STEPS:

IMMEDIATE ACTIONS:
1. Try to recover account using "Forgot Password" 
2. Check if recovery email/phone is still accessible
3. Use platform's account recovery process immediately
4. Alert friends/followers about the hack (from alternate account)
5. Document all unauthorized activity with screenshots

PLATFORM-SPECIFIC RECOVERY:
FACEBOOK: facebook.com/hacked → Follow recovery wizard
INSTAGRAM: Help Center → "Hacked Accounts" → Request support link
TWITTER/X: help.twitter.com → "Account" → "Hacked account"
WHATSAPP: Reinstall app with your number to kick out hacker

REPORT TO CYBERCRIME PORTAL:
1. Visit https://cybercrime.gov.in
2. Click "Report Other Cybercrimes"
3. Select "Cyber Attack/Hacking" → "Hacking/Defacement"
4. Provide: Platform name, account details, date of hack, screenshots
5. Upload evidence of unauthorized access

EVIDENCE TO COLLECT:
✓ Screenshots of unauthorized posts/messages
✓ Unusual login activity/locations
✓ Changed account details
✓ Messages sent by hacker
✓ Login notification emails
✓ Recovery attempt confirmations

PREVENTION AFTER RECOVERY:
→ Enable Two-Factor Authentication (2FA) immediately
→ Change password to strong unique password (12+ characters)
→ Review authorized apps and remove suspicious ones
→ Check connected devices and logout all sessions
→ Update recovery email and phone number
→ Review recent activity and posts

REPORT TO PLATFORM:
- Use in-app reporting for all unauthorized content
- Request account activity log
- Report impersonation if hacker created fake profile
- Request IP logs of unauthorized access

LEGAL ACTIONS:
- File FIR if financial loss or defamation occurred
- Cyber harassment: Report under IT Act Section 66A/67
- Identity theft: Mention IPC Section 419/420
- Get cybercrime portal complaint number for all proceedings"""
    },
    {
        "id": "online_job_fraud",
        "title": "Online Job/Task Fraud - Complete Reporting SOP",
        "category": "financial_fraud", 
        "content": """ONLINE JOB/TASK FRAUD (Telegram/WhatsApp Jobs) - IMMEDIATE ACTIONS:

RECOGNIZE THE FRAUD:
⚠ Simple tasks for high money (like product reviews, clicking)
⚠ Asked to pay "registration fee" or "advance"
⚠ Promises of ₹1000-5000 daily for 1-2 hours work
⚠ Telegram/WhatsApp groups for "part-time work"
⚠ Asked to transfer money to "unlock" your earnings

IF YOU PAID MONEY:
1. STOP all further payments immediately
2. CALL 1930 (Financial Cyber Fraud Helpline) NOW
3. Block fraudster on all platforms
4. Screenshot ALL conversations and payment proofs
5. Report within 24 hours for fund recovery

REPORT TO CYBERCRIME PORTAL:
→ Visit https://cybercrime.gov.in
→ Select "Report Other Cybercrimes"
→ Category: "Online Financial Fraud" → "Online Job Fraud"
→ Provide: Fraudster contact, payment details, chat screenshots
→ Upload all evidence files

EVIDENCE CHECKLIST:
✓ Complete chat history with fraudster
✓ Job/task descriptions and promises made
✓ Payment screenshots (UPI/bank transfer)
✓ Group invite links/screenshots
✓ Website URLs if any
✓ Fraudster's phone/Telegram/WhatsApp number
✓ Bank account details where money sent

BANKING ACTIONS:
- Immediately report to your bank
- Request transaction reversal
- File complaint at bank branch
- Get bank complaint reference
- Request blocking of fraudster's account

REPORT TO PLATFORMS:
Telegram: Report user and group for fraud
WhatsApp: Report contact as spam/fraud
Block and delete fraudster contact

LEGAL RECOURSE:
- File FIR at nearest cyber police station
- Mention IPC Section 420 (Cheating) and IT Act Section 66D
- Provide cybercrime portal complaint number
- Get FIR copy for insurance/future reference

WARNING SIGNS TO AVOID:
❌ Pay to get paid schemes
❌ Unrealistic earnings for simple work  
❌ Pressure to pay immediately
❌ No company registration details
❌ Only Telegram/WhatsApp communication
❌ Tasks that seem illegal or unethical"""
    },
    {
        "id": "investment_fraud",
        "title": "Investment/Trading Fraud - Complete SOP",
        "category": "financial_fraud",
        "content": """INVESTMENT/TRADING FRAUD - IMMEDIATE PROTECTIVE ACTIONS:

RECOGNIZE INVESTMENT SCAMS:
⚠ Guaranteed high returns (20-50% monthly)
⚠ Pressure to invest immediately 
⚠ Celebrity endorsements (usually fake)
⚠ WhatsApp/Telegram trading groups
⚠ Unregistered platforms/apps
⚠ Cannot withdraw your money

IMMEDIATE ACTIONS IF SCAMMED:
1. STOP sending more money immediately
2. Try to withdraw remaining balance
3. Screenshot entire platform/app interface
4. Document all conversations with "advisor"
5. CALL 1930 for financial fraud reporting
6. Report within 24 hours to freeze funds

REPORT TO AUTHORITIES:
→ Cybercrime Portal: https://cybercrime.gov.in
→ Category: "Online Financial Fraud" → "Investment/Trading Fraud"
→ SEBI Complaints: scores.gov.in (for stock market fraud)
→ RBI: rbidocs.rbi.org.in (for unauthorized NBFCs)

EVIDENCE TO COLLECT:
✓ Platform/app screenshots showing investment
✓ Payment receipts and bank statements
✓ Promotional material and promises made
✓ Chat history with advisors/support
✓ Website URL and app download link
✓ Company registration claims
✓ Social media ads/posts about platform
✓ Referral links and group invites

BANKING ACTIONS:
- Report to your bank immediately
- Request chargeback if used card
- File formal complaint at branch
- Request investigation into recipient accounts
- Block any recurring payments

VERIFY LEGITIMACY (Before Investing):
→ Check SEBI registration: sebi.gov.in
→ Verify mutual fund: amfiindia.com
→ Check company MCA: mca.gov.in
→ RBI authorized NBFC list: rbi.org.in
→ NSE/BSE listing verification

RED FLAGS TO WATCH:
❌ Not registered with SEBI/RBI
❌ Pressure to invest NOW
❌ Guaranteed returns claims
❌ Celebrity fake endorsements
❌ Only accepts crypto/UPI (no bank)
❌ Withdrawal problems or conditions
❌ Upfront fees or commissions

LEGAL ACTION:
- File FIR mentioning IPC 420, 406, IT Act 66D
- Submit complaint to Economic Offences Wing
- Contact SEBI Investor Protection Cell
- Get lawyer consultation for recovery
- Join other victims for class action

RECOVERY OPTIONS:
- Cybercrime complaint → Fund freeze
- Bank chargeback within 30-60 days
- SEBI arbitration for registered entities
- Consumer forum for unfair trade
- Civil suit for fraud recovery"""
    },
    {
        "id": "cybercrime_portal_guide",
        "title": "National Cybercrime Portal Complete Guide",
        "category": "reporting",
        "content": """CYBERCRIME.GOV.IN - COMPLETE USAGE GUIDE

PORTAL URL: https://cybercrime.gov.in
HELPLINE: 1930 (24x7 for financial frauds)

WHO CAN REPORT:
✓ Any Indian citizen
✓ Age 18+ required (parent/guardian for minors)
✓ Valid Indian mobile number needed
✓ Email ID required

TYPES OF COMPLAINTS:
1. Women/Child Related Crime (Anonymous reporting available)
2. Other Cybercrimes (Login required):
   - Financial Fraud
   - Social Media Crime
   - Cyber Attack/Hacking
   - Online Gambling
   - Cyberbullying
   - Ransomware
   - Cyber Terrorism

STEP-BY-STEP COMPLAINT FILING:

STEP 1: REGISTRATION
→ Visit cybercrime.gov.in
→ Click "Report Other Cybercrimes"
→ Enter mobile number → Verify OTP
→ Create account with email and password

STEP 2: SELECT CATEGORY
Choose from:
- Online Financial Fraud (UPI, Banking, Investment)
- Cyber Attack (Hacking, Phishing, Malware)
- Social Media Related Crime
- Cyber Bullying/Stalking
- Ransomware Attack
- Cryptocurrency Fraud
- Others

STEP 3: SUB-CATEGORY
Select specific fraud type (e.g., UPI Fraud, Job Fraud)

STEP 4: INCIDENT DETAILS
Provide:
- Date and time of incident
- Where it occurred (platform/website)
- Detailed description
- Financial loss amount (if any)
- Suspect information (if known)
- How you were contacted

STEP 5: SUSPECT INFORMATION
Enter if known:
- Phone number
- Email ID
- Social media profile
- Website URL
- Bank account number
- UPI ID
- Cryptocurrency wallet

STEP 6: UPLOAD EVIDENCE
Attach files (max 50MB each):
- Screenshots (PNG, JPG)
- Chat logs/conversation
- Bank statements (PDF)
- Transaction receipts
- Video evidence (if any)
- Audio recordings

STEP 7: REVIEW & SUBMIT
- Check all details carefully
- Submit complaint
- Note down complaint number (Format: CCN2025XXXXX)
- Save acknowledgment receipt

AFTER SUBMISSION:

TRACKING COMPLAINT:
→ Login to cybercrime.gov.in
→ Go to "Track Your Complaint"
→ Enter complaint number
→ Check status updates

COMPLAINT STATUS:
- Pending: Under review
- Assigned: Sent to jurisdictional police
- Under Investigation: Active inquiry
- Action Taken: Police took action
- Closed: Investigation completed

FOLLOW-UP ACTIONS:
- Check status every 7 days
- Respond to police requests promptly
- Provide additional evidence if asked
- Contact jurisdictional police station

ESCALATION:
If no action in 30 days:
1. Email: complaints@cybercrime.gov.in
2. Contact State Nodal Officer (details on portal)
3. File RTI application
4. Approach SP Cyber Cell of your state

IMPORTANT NOTES:
✓ File complaint ASAP (within 24 hours for financial fraud)
✓ Keep complaint number safe
✓ Don't file duplicate complaints
✓ Update if you have new evidence
✓ Cooperate with investigating officer
✓ Response time: 7-30 days usually

HELPLINE SUPPORT:
1930: Financial cyber fraud (24x7)
155260: General cyber helpline
181: Women helpline"""
    },
    {
        "id": "phishing_scam",
        "title": "Phishing/Fake Link/OTP Fraud - Complete SOP",
        "category": "fraud",
        "content": """PHISHING/OTP FRAUD - IMMEDIATE ACTIONS:

IDENTIFY PHISHING:
⚠ SMS/Email claiming account blocked/KYC update needed
⚠ Fake courier/delivery links
⚠ Lottery/prize winning messages
⚠ Links mimicking bank/government websites
⚠ Requests for OTP, CVV, PIN, or password

IF YOU ALREADY CLICKED LINK OR SHARED OTP:

IMMEDIATE (Within 5 minutes):
1. Call your bank's customer care NOW
2. Block all debit/credit cards immediately
3. Change all banking passwords
4. Enable transaction alerts
5. Check bank balance for unauthorized transactions

NEXT STEPS (Within 1 hour):
1. Call 1930 to report financial fraud
2. File complaint on cybercrime.gov.in
3. Take screenshots of phishing message/website
4. Note down sender number/email/website URL
5. Forward phishing SMS to 1909 (TRAI spam reporting)

REPORT TO CYBERCRIME PORTAL:
→ Visit https://cybercrime.gov.in
→ Category: "Cyber Attack" → "Phishing"
→ Or "Financial Fraud" if money lost
→ Provide: Phishing link, sender details, screenshots
→ Upload evidence

EVIDENCE TO COLLECT:
✓ Screenshot of phishing SMS/Email
✓ Sender phone number/email
✓ Fake website URL and screenshots
✓ Any data entered on fake site
✓ Bank transaction alerts if money debited
✓ Call recording if scammer called
✓ WhatsApp chat if contacted there

BANKING ACTIONS:
- Immediately inform bank of compromise
- Block ALL cards (even unused ones)
- File written complaint at bank
- Request reversal of unauthorized transactions
- Update mobile number for alerts
- Enable 2FA for net banking

REPORT PHISHING TO:
→ Bank: Forward SMS to bank's official email
→ TRAI: Forward to 1909 for spam blocking
→ Google Safe Browsing: safebrowsing.google.com/safebrowsing/report_phish
→ Report phishing email to: reportphishing@apwg.org

PREVENTION CHECKLIST:
✓ Never click links in unexpected SMS/emails
✓ Always type website URL manually
✓ Check website URL carefully (look for https://)
✓ Never share OTP, CVV, PIN with anyone
✓ Banks never ask for OTP/PIN on call
✓ Enable SMS/Email alerts for all transactions
✓ Use strong unique passwords
✓ Enable 2FA wherever available

RED FLAGS:
❌ Urgent action required messages
❌ Account will be blocked threats
❌ Too good to be true offers
❌ Spelling mistakes in messages
❌ Suspicious sender email/number
❌ Requests for sensitive information
❌ Links with random characters

COMMON PHISHING TYPES:
1. Bank KYC Update Scam
2. Fake Courier/Delivery links
3. Electricity Bill Payment scams
4. Government Scheme fraud SMS
5. Credit Card Upgrade scams
6. OTP Verification scams
7. Lottery/Prize winning frauds

WHAT NOT TO DO:
❌ Don't panic and act hastily
❌ Don't call number in phishing message
❌ Don't reply to phishing SMS
❌ Don't download suspicious apps
❌ Don't share screenshots with sensitive info publicly

LEGAL ACTION:
- File FIR if money lost
- Mention IT Act Section 66C, 66D
- IPC Section 420 for cheating
- Keep cybercrime complaint number
- Follow up with local cyber cell"""
    },
    {
        "id": "cyberbullying_harassment",
        "title": "Cyberbullying & Online Harassment - Complete SOP",
        "category": "harassment",
        "content": """CYBERBULLYING/HARASSMENT - IMMEDIATE PROTECTIVE ACTIONS:

TYPES OF CYBER HARASSMENT:
- Abusive messages/comments
- Threats and blackmail
- Morphed photos/videos
- Fake profiles/impersonation
- Doxxing (sharing personal info)
- Online stalking
- Revenge porn
- Trolling and hate speech

IMMEDIATE ACTIONS:
1. DO NOT engage with harasser
2. DO NOT delete any evidence
3. Screenshot everything immediately
4. Block harasser on all platforms
5. Report to platform immediately
6. Secure your accounts (privacy settings)

DOCUMENT EVIDENCE:
✓ Screenshots with date/time stamps
✓ URLs of harassing posts/profiles
✓ Sender's profile information
✓ Messages and comments (full thread)
✓ Emails with full headers
✓ IP address if available
✓ Witness statements if any

REPORT TO PLATFORMS:
Facebook: Report → Bullying/Harassment
Instagram: Report → It's inappropriate → Harassment
Twitter: Report Tweet → Abusive/Harmful
WhatsApp: Report contact → Block and Delete
YouTube: Report → Harassment/Cyberbullying

REPORT TO CYBERCRIME PORTAL:
→ Visit https://cybercrime.gov.in
→ For women/children: "Report Women/Child Related Crime" (ANONYMOUS)
→ For others: "Report Other Cybercrimes" → "Cyber Bullying/Stalking"
→ Provide: Platform, harasser details, screenshots
→ Upload ALL evidence

WOMEN/CHILD COMPLAINTS (ANONYMOUS):
- No login required
- Privacy protected
- Direct to dedicated police teams
- Faster action on sensitive cases
- Contact: 1091 (Women Helpline)

LEGAL PROVISIONS:
→ IT Act Section 67: Publishing obscene content
→ IT Act Section 67A: Sexually explicit content
→ IT Act Section 66E: Privacy violation
→ IT Act Section 66D: Cheating by impersonation
→ IPC Section 354A: Sexual harassment
→ IPC Section 354C: Voyeurism
→ IPC Section 354D: Stalking
→ IPC Section 503: Criminal intimidation
→ IPC Section 506: Death/injury threats
→ IPC Section 509: Insulting modesty of woman

ENHANCED PRIVACY SETTINGS:
Instagram/Facebook:
- Make account private
- Limit who can comment
- Turn off "Allow others to find by email/phone"
- Remove tagged posts approval required
- Block anonymous/fake accounts

Twitter/X:
- Protect tweets (private account)
- Mute specific words/phrases
- Block accounts
- Disable photo tagging
- Limit who can reply

SUPPORT RESOURCES:
→ Women Helpline: 1091
→ Child Helpline: 1098
→ Mental Health Support: 
   NIMHANS: 080-46110007
   Vandrevala Foundation: 1860-2662-345
→ Legal Aid: doj.gov.in/legal-aid

REPORTING TO POLICE:
- File FIR at local police station or cyber cell
- Mention specific IPC/IT Act sections
- Provide cybercrime portal complaint number
- Request anticipatory measures if threats
- Get FIR copy for records

IMMEDIATE SAFETY MEASURES:
✓ Change all passwords
✓ Enable 2FA on all accounts
✓ Review app permissions
✓ Check location sharing settings
✓ Remove metadata from shared photos
✓ Limit personal information publicly visible
✓ Inform trusted friends/family
✓ Consider temporary account deactivation

TROLLING & HATE SPEECH:
- Report to platform for community guidelines violation
- Mass reporting by supporters helps
- Document pattern if organized trolling
- Report to cybercrime if threats involved
- Consider legal action for defamation

REVENGE PORN:
- Report immediately to platform
- File complaint on cybercrime portal (anonymous for women)
- IT Act Section 66E + IPC 354A applicable
- Request immediate takedown
- Contact platform's legal team
- File FIR with cyber cell

FOR MINORS (Under 18):
- Parent/Guardian must file complaint
- Report to school/college authorities
- Child Welfare Committee involvement
- POCSO Act provisions if applicable
- Special protection measures
- Counseling support available

FOLLOW-UP:
- Track complaint regularly
- Respond to police inquiries promptly
- Keep evidence backup in multiple places
- Document any new harassment
- Seek counseling if needed
- Update security settings regularly"""
    },
    {
        "id": "ransomware_attack",
        "title": "Ransomware Attack - Complete Recovery SOP",
        "category": "cyber_attack",
        "content": """RANSOMWARE ATTACK - IMMEDIATE RESPONSE:

IDENTIFY RANSOMWARE:
⚠ Files suddenly encrypted (can't open)
⚠ File extensions changed (.locked, .encrypted, etc.)
⚠ Ransom note demanding payment
⚠ Desktop wallpaper changed to threat message
⚠ Timer counting down for payment

CRITICAL - DO NOT:
❌ DO NOT pay the ransom (no guarantee of decryption)
❌ DO NOT delete anything
❌ DO NOT restart computer immediately
❌ DO NOT contact attackers yet

IMMEDIATE ACTIONS (First 10 minutes):

1. ISOLATE INFECTED SYSTEM:
   - Disconnect from internet (unplug Ethernet/disable WiFi)
   - Disconnect from network
   - Turn off shared drives/cloud sync
   - Disconnect external drives

2. TAKE PHOTOS:
   - Photo of ransom message with phone
   - Screen showing encrypted files
   - Any contact information provided
   - Timer if displayed

3. DO NOT SHUTDOWN:
   - Keep system running for investigation
   - Shutdown may trigger additional encryption
   - Investigators can analyze running processes

REPORT TO AUTHORITIES:

→ CERT-In: incident@cert-in.org.in | cert-in.org.in
→ Cybercrime Portal: cybercrime.gov.in → "Cyber Attack" → "Ransomware"
→ Call 1930 if business/financial loss
→ Local Cyber Cell for FIR

EVIDENCE COLLECTION:
✓ Photos of ransom note
✓ Ransom payment address (Bitcoin/crypto wallet)
✓ Contact email/URL provided by attackers
✓ List of encrypted files
✓ System logs (if accessible)
✓ Recent downloads/email attachments
✓ Network activity logs

TECHNICAL ANALYSIS:

Identify Ransomware Variant:
→ Upload ransom note to: nomoreransom.org
→ Check ID Ransomware: id-ransomware.malwarehunterteam.com
→ Knowing variant helps find decryption tool

RECOVERY OPTIONS:

Option 1: FREE DECRYPTION TOOLS
- Check No More Ransom Project: nomoreransom.org
- 150+ free decryption tools available
- Upload sample encrypted file
- Download matching decryption tool
- Follow instructions carefully

Option 2: RESTORE FROM BACKUP
- Check if backups exist (external drive/cloud)
- Ensure backup not infected
- Restore to clean system
- Update all security before reconnecting

Option 3: PROFESSIONAL HELP
- Contact cybersecurity firms
- Forensic analysis may recover files
- Corporate/government: Engage IR team
- Cost vs. data value assessment

FOR BUSINESSES:

Immediate:
→ Activate Incident Response Plan
→ Isolate affected systems from network
→ Notify IT/Security team
→ Alert management
→ Preserve evidence for forensics
→ Contact cyber insurance provider

Investigation:
→ Identify patient zero (first infected system)
→ Check how ransomware entered
→ Assess data breach/exfiltration
→ Review backup integrity
→ Analyze attack timeline

Recovery:
→ Clean systems with anti-malware
→ Patch vulnerabilities
→ Restore from clean backups
→ Strengthen security controls
→ Employee security training

PREVENTION (After Recovery):

CRITICAL SECURITY MEASURES:
✓ Regular backups (3-2-1 rule: 3 copies, 2 different media, 1 offsite)
✓ Keep backups offline/air-gapped
✓ Update all software and OS regularly
✓ Install genuine antivirus
✓ Enable Windows Defender Ransomware Protection
✓ Disable macros in Office files
✓ Use ad-blockers
✓ Don't open unknown email attachments
✓ Don't click suspicious links

TECHNICAL PROTECTIONS:
→ Application whitelisting
→ Disable RDP if not needed
→ Network segmentation
→ Email filtering and scanning
→ Web content filtering
→ Regular security audits
→ Intrusion Detection Systems

LEGAL RECOURSE:
- File FIR under IT Act Section 66
- Cybercrime portal complaint mandatory
- Report to CERT-In for coordination
- Corporate: Notify data protection authorities
- Business interruption insurance claim
- Civil action against negligent vendors

COMMON INFECTION METHODS:
1. Phishing emails with malicious attachments
2. Malicious advertisements (malvertising)
3. Software vulnerabilities
4. Remote Desktop Protocol (RDP) attacks
5. Infected USB drives
6. Compromised websites
7. Fake software updates

FAMOUS RANSOMWARE VARIANTS:
- WannaCry
- Petya/NotPetya  
- CryptoLocker
- Locky
- Bad Rabbit
- Ryuk
- Sodinokibi/REvil

RESOURCES:
→ No More Ransom: nomoreransom.org
→ CERT-In: cert-in.org.in
→ Microsoft Malware Protection: microsoft.com/security
→ Kaspersky Decrypt Tools: support.kaspersky.com

REMEMBER:
- Prevention is better than cure
- Regular backups are your best defense
- Never pay ransom (encourages attacks)
- Report to authorities to help others
- Seek professional help for business-critical data"""
    },
    {
        "id": "police_station_finder",
        "title": "How to Find Nearest Cyber Police Station",
        "category": "reporting",
        "content": """FINDING NEAREST CYBER POLICE STATION/CELL:

OFFICIAL METHODS:

1. CYBERCRIME PORTAL METHOD:
→ Visit https://cybercrime.gov.in
→ Click "Report Other Cybercrimes"
→ During complaint filing, portal shows jurisdictional police
→ Complete address and contact shown
→ Can directly file complaint or visit station

2. CITIZEN SERVICES:
→ Search "cyber crime police station near me" on Google Maps
→ Most cyber cells now listed with timings
→ Call before visiting to confirm

3. STATE POLICE WEBSITES:
Every state has dedicated cyber cell:
→ Delhi: cybercrime.delhi.gov.in
→ Maharashtra: cybercell.mahapol.gov.in  
→ Karnataka: ksp.gov.in
→ Tamil Nadu: ccctns.tnpolice.gov.in
→ Uttar Pradesh: uppolice.gov.in

MAJOR CITIES CYBER CELLS:

DELHI:
- CyPAD (Cyber Cell): Dwarka Sector 13
- Contact: 011-26781837
- Email: igcybercrime@delhipolice.gov.in

MUMBAI:
- Cyber Crime Cell, BKC
- Contact: 022-26594074
- Email: ccbmum-cid@mahapolice.gov.in

BENGALURU:
- CEN Police Station (Cyber Crime)
- Contact: 080-22943480
- Email: igcid@ksp.gov.in

HYDERABAD:
- Cyber Crime Police Station
- Contact: 040-27853508
- Email: ccs.cyberabad@tspolice.gov.in

CHENNAI:
- Crime Against Women & Children Wing
- Contact: 044-28447701
- Email: cbcid-hq@tnpolice.gov.in

KOLKATA:
- Cyber Crime PS, Bhawani Bhawan
- Contact: 033-22143028
- Email: wb.police@gov.in

PUNE:
- Pune City Cyber Cell
- Contact: 020-26126989

WHEN TO VISIT CYBER CELL:

Visit in Person For:
✓ High-value financial fraud (>₹1 lakh)
✓ Serious threats to life/safety
✓ Corporate/business cybercrimes
✓ Data breach incidents
✓ Child abuse material cases
✓ Ransomware attacks
✓ When online complaint not sufficient

WHAT TO CARRY:
✓ Identity proof (Aadhaar/PAN/Driving License)
✓ Address proof
✓ Mobile phone with evidence
✓ Printed screenshots
✓ Bank statements (if financial fraud)
✓ Any physical evidence
✓ List of dates/times/events
✓ Suspect information (if known)

AT THE CYBER CELL:

1. Reception/Front Desk:
   - Explain your complaint briefly
   - They'll guide to relevant section

2. Filing Complaint:
   - Provide detailed written complaint
   - Attach all evidence
   - Get acknowledgment receipt
   - Note FIR/complaint number
   - Get investigating officer details

3. After Filing:
   - Ask about timeline
   - Get contact number for follow-up
   - Understand next steps
   - Cooperate with investigation

DISTRICT-LEVEL REPORTING:

If no cyber cell in your district:
1. Go to nearest police station
2. Ask for Cyber Crime Nodal Officer
3. They'll register complaint or guide to cyber cell
4. Rural areas: File at district headquarters

ONLINE VS OFFLINE:

File Online For:
- All types of cybercrimes
- Quick registration
- Track status online
- Evidence upload facility
- 24x7 availability

Visit Offline For:
- Complex cases needing explanation
- Urgent matters
- Large volume of evidence
- Follow-up on pending cases
- Getting investigation updates

STATE HELPLINES:
→ Delhi: 155315
→ Uttar Pradesh: 155260
→ Maharashtra: 022-26594074
→ Karnataka: 080-22942627
→ Tamil Nadu: 9498233474

ESCALATION PATH:
1. First: File on cybercrime.gov.in
2. If no response in 15 days: Visit cyber cell
3. If still no action: Contact SP Cyber Cell
4. Further escalation: State Nodal Officer
5. Last resort: DGP Cyber Crime

WORKING HOURS:
- Most cyber cells: 10 AM - 6 PM (Mon-Fri)
- Some 24x7 cells in metro cities
- Emergency: Call 1930 (24x7)
- Weekend: Online portal available

IMPORTANT NOTES:
✓ No fee for filing complaint
✓ Complaint in Hindi/English/Regional language accepted
✓ Woman officer available for women complainants
✓ Can take a support person with you
✓ Language barrier: Request translator
✓ Get written acknowledgment always
✓ Keep FIR copy safe

SPECIALIZED UNITS:

Cybercrimes Against Women & Children:
- Dedicated cells in all states
- Woman officers available
- Sensitive handling
- Counseling support
- Fast-track investigation

Banking Fraud Unit:
- Quick coordination with banks
- Fund freeze mechanism
- Works with 1930 helpline
- NPCI coordination

Corporate Cyber Cell:
- Business email compromise
- Data breach investigations
- Intellectual property theft
- Corporate espionage

RIGHTS AS COMPLAINANT:
✓ Right to file complaint
✓ Right to get FIR copy
✓ Right to investigation updates
✓ Right to victim compensation
✓ Right to privacy protection
✓ Right to legal representation
✓ Right to appeal if FIR not registered

FOLLOW-UP:
- Follow up every 15 days
- Provide additional evidence promptly
- Respond to investigator calls
- Attend proceedings when called
- Check online status regularly"""
    },
    {
        "id": "online_gaming_fraud",
        "title": "Online Gaming & Betting Fraud - Complete SOP",
        "category": "financial_fraud",
        "content": """ONLINE GAMING/BETTING FRAUD - IMMEDIATE ACTIONS:

RECOGNIZE GAMING SCAMS:
⚠ Color prediction games (Red/Green betting)
⚠ Teen Patti/Rummy real money apps
⚠ Online cricket betting
⚠ Casino games promising big wins
⚠ Initial small wins, then big losses
⚠ Cannot withdraw winnings
⚠ Account blocked after deposit

COMMON SCAM PATTERNS:
1. Initial wins to build trust
2. Increase bet amounts
3. Sudden losses after big deposit
4. Withdrawal problems
5. Account suspension
6. Customer support disappears
7. App/website vanishes

IMMEDIATE ACTIONS IF SCAMMED:
1. STOP playing/depositing immediately
2. Take screenshots of:
   - App interface and your account
   - Bet history and transactions
   - Winning amount shown
   - Deposit and withdrawal attempts
   - Chat with customer support
   - Promotional messages received
3. Try to withdraw remaining balance
4. Don't delete app yet (evidence needed)

LEGAL STATUS:
⚠ Online gambling is ILLEGAL in India (except Sikkim/Goa)
⚠ Betting apps are illegal under Public Gambling Act 1867
⚠ You can still report fraud, but may face questions
⚠ Financial fraud aspect is definitely reportable

REPORT TO AUTHORITIES:
→ Call 1930 immediately
→ Cybercrime Portal: https://cybercrime.gov.in
→ Category: "Online Financial Fraud" → "Online Gambling/Betting Fraud"
→ Provide: App name, deposits made, withdrawal issues
→ Upload: Screenshots, payment proofs, chat history

EVIDENCE CHECKLIST:
✓ Gaming app screenshots (full interface)
✓ Your account showing balance
✓ Deposit transaction receipts
✓ Withdrawal request screenshots
✓ Bank statement showing debits
✓ Promotional SMS/WhatsApp messages
✓ Referral links/codes
✓ Terms & conditions screenshots
✓ Customer support chat
✓ App download link/website URL

BANKING ACTIONS:
- Report unauthorized if account compromised
- Request chargeback if possible
- File complaint at bank branch
- Block cards if details shared
- Monitor for suspicious activity

PLATFORM REPORTING:
Google Play: Report app → "Inappropriate content" → "Gambling"
Apple App Store: Report a problem
WhatsApp: Report promotional messages as spam
Telegram: Report groups/channels promoting gambling

COMMON GAMING SCAMS:

1. COLOR PREDICTION SCAM:
   - Predict red/green/violet colors
   - Starts with wins, then losses
   - Cannot withdraw after winning big
   - Apps: Daman, 82 Lottery, 91 Club, etc.

2. TEEN PATTI/RUMMY FRAUD:
   - Real money card games
   - Rigged algorithms
   - Bots playing against you
   - Withdrawal delays/excuses

3. BETTING APPS:
   - Cricket/Sports betting
   - Match-fixing claims
   - Inside information scam
   - Losses blamed on wrong predictions

4. SPIN & WIN FRAUDS:
   - Lucky wheel spins
   - Daily rewards turn to real money deposit
   - Can't withdraw without referrals
   - Pyramid scheme model

RED FLAGS:
❌ Guaranteed wins/returns
❌ Referral bonuses focus
❌ Withdrawal minimum very high
❌ Complex withdrawal conditions
❌ No company registration details
❌ Customer support unavailable
❌ App not on official stores
❌ Payment only via UPI/crypto

PREVENTION:
✓ Avoid all betting/gambling apps
✓ Remember: House always wins
✓ Don't trust initial wins
✓ Check app legitimacy before download
✓ Don't share financial details
✓ Verify company registration
✓ Don't fall for referral schemes

LEGAL PROVISIONS:
→ Public Gambling Act, 1867
→ IT Act Section 66D (Cheating by impersonation)
→ IPC Section 420 (Cheating)
→ IPC Section 406 (Criminal breach of trust)

WHAT POLICE CAN DO:
- Investigate fraud/cheating aspect
- Freeze fraudsters' accounts
- Block illegal gambling apps
- Track organized crime syndicates
- Help recover money in some cases

VICTIM SUPPORT:
- Don't feel embarrassed to report
- Focus on financial fraud aspect
- Many others also scammed
- Reporting helps shut down scams
- Possible compensation from seized assets

ADDICTION HELP:
If addicted to online gambling:
→ Gambling Anonymous India: gamblersanonymous.org.in
→ Mental Health Helpline: 08046110007
→ Seek counseling: NIMHANS, local psychiatrists
→ Block gambling sites/apps on your phone
→ Share phone with trusted person for monitoring

BANK ACCOUNT PROTECTION:
- Enable transaction alerts
- Set daily transaction limits
- Freeze unused accounts
- Don't save card details on apps
- Use separate account for online transactions
- Enable 2FA for banking apps

RECOVERY CHANCES:
- Higher if reported within 24 hours
- Fund freeze possible via 1930 helpline
- Banks can chargeback sometimes
- Police can seize operator accounts
- Civil suit for recovery possible

ALTERNATIVE ACTIONS:
- Consumer court for unfair trade
- RBI complaint for payment gateway misuse
- Report to hosting provider
- Report domain to registrar
- Social media reporting to warn others

REMEMBER:
- If it sounds too good to be true, it is
- No easy money exists
- Gambling is rigged against you
- Report to save others from scam
- Learn from mistake and move on"""
    }
]


async def populate_vectorstore_fast():
    """Fast vectorstore population with optimized batching"""
    
    print("=" * 80)
    print("  FAST VECTORSTORE POPULATION - OPTIMIZED FOR ALL SYSTEMS")
    print("=" * 80)
    print()
    
    start_time = time.time()
    
    # Step 1: Initialize services
    print("Step 1: Initializing services...")
    print("-" * 80)
    
    try:
        # Initialize embedding service
        if not embedding_service.is_initialized():
            print("→ Loading embedding model...")
            await embedding_service.initialize()
            print("✓ Embedding model ready")
        else:
            print("✓ Embedding model already loaded")
        
        # Initialize RAG service
        if not rag_service._initialized:
            print("→ Initializing vector database...")
            await rag_service.initialize()
            print("✓ Vector database ready")
        else:
            print("✓ Vector database already initialized")
        
        print()
        
        # Step 2: Check existing data
        print("Step 2: Checking existing data...")
        print("-" * 80)
        existing_count = rag_service.get_document_count()
        print(f"Current documents in vectorstore: {existing_count}")
        
        if existing_count > 0:
            response = input("\n⚠ Vectorstore already has data. Clear and rebuild? (y/n): ")
            if response.lower() == 'y':
                print("→ Clearing existing vectorstore...")
                rag_service.collection.delete(where={})
                print("✓ Vectorstore cleared")
            else:
                print("✓ Keeping existing data, will add new documents")
        print()
        
        # Step 3: Process documents
        print(f"Step 3: Processing {len(SOP_DOCUMENTS)} documents...")
        print("-" * 80)
        
        texts = []
        metadatas = []
        ids = []
        
        for doc in SOP_DOCUMENTS:
            # Prepare document data
            texts.append(doc["content"])
            metadatas.append({
                "title": doc["title"],
                "category": doc["category"],
                "source": "Government Guidelines",
                "date": "2025",
                "doc_id": doc["id"]
            })
            ids.append(doc["id"])
        
        print(f"✓ Prepared {len(texts)} documents for vectorization")
        print()
        
        # Step 4: Batch embed and add to vectorstore
        print("Step 4: Vectorizing and storing (batched for speed)...")
        print("-" * 80)
        
        # Embed in batch (much faster)
        print("→ Generating embeddings in batch...")
        embeddings = await embedding_service.embed_batch(texts)
        print(f"✓ Generated {len(embeddings)} embeddings")
        
        # Add to ChromaDB in single batch
        print("→ Adding to vectorstore...")
        rag_service.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print("✓ Documents stored successfully")
        print()
        
        # Step 5: Verify
        print("Step 5: Verification...")
        print("-" * 80)
        final_count = rag_service.get_document_count()
        print(f"✓ Total documents in vectorstore: {final_count}")
        
        # Test retrieval
        print("\n→ Testing retrieval speed...")
        test_query = "How to report UPI fraud?"
        test_start = time.time()
        results = await rag_service.retrieve(test_query, top_k=3)
        test_time = time.time() - test_start
        print(f"✓ Retrieved {len(results)} relevant documents in {test_time:.3f}s")
        
        if results:
            print(f"\n  Top result: {results[0]['source']} (score: {results[0]['score']:.3f})")
        
        print()
        
        # Summary
        elapsed = time.time() - start_time
        print("=" * 80)
        print("  SUCCESS - VECTORSTORE READY!")
        print("=" * 80)
        print(f"✓ Total documents: {final_count}")
        print(f"✓ Vector database: {rag_service.db_path}")
        print(f"✓ Total time: {elapsed:.2f} seconds")
        print(f"✓ Retrieval speed: {test_time*1000:.0f}ms")
        print()
        print("Your LLM is now ready for FAST queries!")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        logger.error(f"Vectorstore population failed: {e}", exc_info=True)
        return False


async def main():
    """Main execution"""
    success = await populate_vectorstore_fast()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

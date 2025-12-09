"""
Data Population Script
Populates the vector database with comprehensive cybercrime SOP documents
Based on official government guidelines and procedures
"""
import asyncio
import json
import sys
from pathlib import Path
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.embedding_service import embedding_service
from app.services.rag_service import rag_service
from app.core.logging import logger


# Comprehensive SOP Documents based on government guidelines
SOP_DOCUMENTS = [
    {
        "id": "upi_fraud_sop",
        "title": "UPI/Digital Payment Fraud - Complete Reporting Procedure",
        "category": "financial_fraud",
        "content": """
UPI/DIGITAL PAYMENT FRAUD - STANDARD OPERATING PROCEDURE

IMMEDIATE ACTIONS (First 5 Minutes):
1. STOP all communication with the fraudster immediately
2. DO NOT delete any messages, call logs, or transaction records
3. Block the fraudster's UPI ID/phone number in your payment app
4. Take screenshots of ALL transaction details
5. Contact your bank's customer care immediately to report fraud
6. Request transaction freeze/reversal if within 24 hours

EMERGENCY HELPLINE - 1930 (MUST CALL):
- Available 24x7 for financial cyber fraud
- Call immediately after discovering fraud
- Provide: Your details, transaction ID, amount, fraudster UPI ID/phone
- Police will create ticket in Citizen Financial Cyber Fraud Reporting System
- System automatically alerts destination bank to freeze funds
- Get helpline reference number for tracking

NATIONAL CYBERCRIME PORTAL REPORTING:
1. Visit https://cybercrime.gov.in
2. Click "Report Other Cybercrimes" button
3. Register/Login using Indian mobile number (OTP verification)
4. Select Category: "Report Other Cybercrimes" → "Online Financial Fraud"
5. Sub-category: Select specific fraud type:
   - UPI Related Fraud
   - Internet Banking Related Fraud
   - Business Email Compromise/Email Takeover
   - Debit/Credit Card Fraud/Sim Swap Fraud
   - E-Wallet Related Fraud
   - Cryptocurrency Fraud

INCIDENT DETAILS TO PROVIDE:
- Date and time of fraud
- Platform/app used (PhonePe, Google Pay, Paytm, etc.)
- Transaction amount and UTR/UPI Transaction ID
- Your bank account details
- Fraudster's UPI ID/phone number/account number
- Method used (fake payment link, QR code, request money scam, etc.)

EVIDENCE CHECKLIST (Upload All):
✓ UPI transaction screenshot with timestamp and UTR number
✓ Bank SMS showing debit/credit alert
✓ Screenshot of fraudster's chat/messages
✓ Screenshot of payment app transaction history
✓ Fraudster's UPI ID/phone number/profile
✓ Any fake website/app screenshots
✓ Email or SMS from fraudster (if any)

BANKING ACTIONS:
1. Immediately call bank customer care (available on back of card)
2. Request immediate transaction reversal/chargeback
3. File written complaint at bank branch within 3 days
4. Request blocking of fraudulent beneficiary account
5. Get bank complaint reference number
6. Follow up with bank within 30 days for resolution

NPCI COMPLAINT (For UPI Issues):
1. Visit https://www.npci.org.in
2. Navigate to "Grievance Redressal" section
3. Select "UPI" under payment systems
4. Fill complaint form with:
   - UPI Transaction ID
   - Date/time of transaction
   - Bank statement proof
   - Cybercrime portal complaint number
5. NPCI will coordinate with banks for resolution

FOLLOW-UP ACTIONS:
- Track complaint on cybercrime portal using reference number (format: CCN2025XXXXX)
- If no response in 15 days, escalate to State Nodal Officer
- Contact Banking Ombudsman if bank doesn't resolve in 30 days
- File physical FIR at local cyber cell if amount > ₹1 lakh
- Monitor bank account for any unauthorized transactions
- Enable transaction alerts and 2FA on all banking apps

PREVENTION FOR FUTURE:
- Never share UPI PIN, CVV, OTP, or passwords
- Don't accept payment requests - only send money
- Verify UPI ID before sending money
- Use only official payment apps from Play Store/App Store
- Enable biometric authentication
- Set transaction limits in payment apps
- Regularly check transaction history
"""
    },
    {
        "id": "social_media_hack_sop",
        "title": "Social Media Account Hacking - Complete Recovery & Reporting",
        "category": "social_media",
        "content": """
SOCIAL MEDIA ACCOUNT HACKING - STANDARD OPERATING PROCEDURE

IMMEDIATE ACTIONS (First 10 Minutes):
1. STOP panicking - account can be recovered
2. DO NOT delete app or create new account yet
3. Try platform's account recovery immediately:
   - Instagram: "Forgot Password?" → "Need More Help?"
   - Facebook: "Forgot Password?" → "No longer have access to these?"
   - WhatsApp: Reinstall app → Enter phone → Request SMS code
   - Twitter/X: "Forgot Password?" → Email/phone recovery
4. Screenshot ALL unauthorized posts/messages before reporting
5. Alert your contacts via other platforms about the hack
6. Check email for password reset/login alerts

PLATFORM-SPECIFIC RECOVERY:

INSTAGRAM (12 Complaint Categories):
1. Try recovery: Settings → Help → Report a Problem → "My account was hacked"
2. Follow in-app selfie verification process
3. Report to cybercrime portal if recovery fails
4. Complaint categories: Hate Speech, Nudity, Violence, Bullying, Spam, Intellectual Property, Impersonation, Self-Injury, False Information, Sale of Illegal Goods, Child Safety, Other

FACEBOOK (13 Complaint Categories):
1. Visit facebook.com/hacked
2. Click "My Account is Compromised"
3. Follow recovery steps with trusted contacts/ID verification
4. Report via Meta Transparency Center: transparency.fb.com
5. Complaint categories: Violent & Criminal Behavior, Safety, Objectionable Content, Intellectual Property, Spam & Fake Accounts, User & Account Management, Others

WHATSAPP:
1. Reinstall WhatsApp on your phone
2. Enter your phone number
3. Request verification code via SMS
4. This automatically logs out hacker's device
5. Enable 2-step verification immediately
6. Report to cybercrime portal if SIM swap involved

TWITTER/X (13 Content Categories):
1. Try password reset via email/phone
2. Report to Twitter Support: help.twitter.com
3. Select "Hacked Account" category
4. Follow verification process
5. Enable 2FA after recovery

YOUTUBE (9 Complaint Categories):
1. Use Google Account Recovery: accounts.google.com/signin/recovery
2. Report via YouTube Help: support.google.com/youtube
3. Categories: Sexual Content, Violent Content, Hateful Content, Harassment, Spam, Child Safety, Privacy, Copyright, Other

NATIONAL CYBERCRIME PORTAL REPORTING:
1. Visit https://cybercrime.gov.in
2. Click "Report Other Cybercrimes"
3. Register/Login with mobile number (OTP)
4. Select Category: "Social Media Related Crime"
5. Sub-categories:
   - Hacking/Defacement
   - Fake Profile
   - Profile Hacking/Identity Theft
   - Provocative Speech for Unlawful Acts
   - Impersonating Email
   - Cyber Bullying/Stalking/Sexting
   - Cheating by Impersonation

EVIDENCE TO COLLECT:
✓ Screenshots of unauthorized posts/messages (before deletion)
✓ Screenshot of changed profile information
✓ Email alerts about password changes/new login
✓ Screenshots showing you're locked out
✓ Original registration email/phone number proof
✓ Previous profile pictures/posts for ownership proof
✓ Screenshots of hacker's activities from friends' accounts
✓ IP address of unauthorized login (if visible in activity log)

ADDITIONAL REPORTING:
1. Report to platform's official grievance officer:
   - Instagram/Facebook: Meta India Grievance Officer
   - Twitter: Twitter India Grievance Officer
   - Contact details available on cybercrime.gov.in

2. For serious cases (morphed images, blackmail, threats):
   - File FIR at local cyber cell
   - Report under IT Act Sections 66C (identity theft), 66D (cheating), 67 (obscene content)

ACCOUNT SECURITY POST-RECOVERY:
- Change password immediately (strong: 12+ characters, symbols, numbers)
- Enable Two-Factor Authentication (2FA)
- Review connected apps and revoke suspicious access
- Check email forwarding rules
- Review recent login activity
- Update recovery email/phone number
- Log out all other sessions
- Review and remove unauthorized followers/friends
- Check privacy settings (make private temporarily)

LINKED ACCOUNTS SECURITY:
- Change passwords on all accounts using same password
- Enable 2FA on email, bank apps, other social media
- Check for linked payment methods and remove unknown ones
- Review recent activity on all platforms

PREVENTION TIPS:
- Never click suspicious links even from friends
- Don't use same password across platforms
- Enable login alerts
- Don't accept login requests from unknown locations
- Use official apps only
- Regularly check connected apps
- Don't share OTPs or passwords
"""
    },
    {
        "id": "online_job_fraud_sop",
        "title": "Online Job/Work-from-Home Fraud - Reporting Procedure",
        "category": "financial_fraud",
        "content": """
ONLINE JOB/WORK-FROM-HOME FRAUD - STANDARD OPERATING PROCEDURE

COMMON FRAUD TYPES:
- Part-time job scams (like products, write reviews, earn money)
- Data entry work-from-home schemes
- Upfront fee for job placement
- Fake company recruitment
- Task-based earning apps with initial payment
- MLM/pyramid schemes disguised as jobs
- Crypto/forex trading job scams
- Fake government job offers

IMMEDIATE ACTIONS:
1. STOP all payments immediately
2. STOP sharing personal documents (Aadhaar, PAN, bank details)
3. DO NOT delete chat history or payment records
4. Block fraudster on all platforms
5. Screenshot ALL conversations, job postings, payment receipts
6. If you shared bank details, inform bank immediately
7. If you shared Aadhaar/PAN, monitor for misuse

RED FLAGS TO IDENTIFY:
- Job requires upfront registration/training fee
- Promises unrealistic earnings (₹1000/hour for simple tasks)
- Asks for money to "activate" account
- Initial small payments to gain trust, then asks for large deposit
- Poor grammar in official communications
- Uses WhatsApp/Telegram instead of official email
- Company website is newly created or looks unprofessional
- Can't verify company registration

NATIONAL CYBERCRIME PORTAL REPORTING:
1. Visit https://cybercrime.gov.in
2. Select "Report Other Cybercrimes"
3. Category: "Online Financial Fraud" → "Cyber Fraud Involving Job Related Impersonation"
4. Provide detailed description of fraud scheme
5. Upload all evidence

EVIDENCE TO COLLECT:
✓ Job posting screenshot (platform, URL, date)
✓ All chat conversations (WhatsApp/Telegram/Email)
✓ Company website screenshot
✓ Payment receipts/transaction screenshots
✓ Bank statement showing debits
✓ Fraudster's phone numbers, UPI IDs, account numbers
✓ Fake appointment letter/offer letter
✓ Any identity documents they shared (usually fake)

IF MONEY LOST - CALL 1930:
- Report to National Cyber Crime Helpline immediately
- Provide transaction details for fund freeze
- Get helpline reference number

FINANCIAL RECOVERY STEPS:
1. File complaint on cybercrime.gov.in (get acknowledgment number)
2. Call 1930 helpline for urgent freezing
3. Report to your bank with complaint number
4. File police complaint at local cyber cell
5. Request chargeback/reversal from bank
6. Track complaint status regularly

ADDITIONAL REPORTING:
1. Report fake job posting to the platform:
   - LinkedIn: Report job/company profile
   - Naukri.com: Use fraud reporting feature
   - Indeed: Report fraudulent job
   - Telegram/WhatsApp: Report and block number

2. Report to job portals if fraudsters used their name:
   - Contact customer support with evidence
   - Help them take down fake listings

IDENTITY THEFT PREVENTION:
If you shared Aadhaar/PAN/bank details:
- Lock Aadhaar biometrics via UIDAI website
- Check CIBIL score for unauthorized loans
- Enable transaction alerts on bank accounts
- File identity theft report on cybercrime.gov.in
- Monitor email for suspicious account creation

LEGAL PROVISIONS:
Applicable IT Act Sections:
- Section 66D: Cheating by personation using computer
- Section 420 IPC: Cheating and dishonestly inducing delivery of property
- Section 66C: Identity theft

FOLLOW-UP:
- Track complaint on cybercrime portal every 7 days
- If no action in 30 days, escalate to State Nodal Officer
- Keep all evidence safely (don't delete for at least 6 months)
- Coordinate with investigating officer if contacted

PREVENTION FOR FUTURE:
- Verify company registration (MCA website)
- Check company reviews on Google/Glassdoor
- Legitimate companies never ask for money
- Research company before applying
- Use only official company email (not Gmail)
- Don't share financial details before job confirmation
- If it sounds too good to be true, it probably is
"""
    },
    {
        "id": "sextortion_blackmail_sop",
        "title": "Sextortion/Online Blackmail - Sensitive Reporting Procedure",
        "category": "women_child_safety",
        "content": """
SEXTORTION/ONLINE BLACKMAIL - STANDARD OPERATING PROCEDURE

⚠️ IMPORTANT: This is a serious crime. You are NOT at fault. Help is available.

WHAT IS SEXTORTION:
- Threatening to share intimate images/videos unless you pay money
- Threatening to share morphed/fake intimate content
- Blackmail after video call recording
- Blackmail after consensual content sharing
- Threats to harm reputation or inform family

IMMEDIATE ACTIONS (CRITICAL):
1. DO NOT PANIC - This is a common crime, not your fault
2. DO NOT PAY - Payment never stops blackmail, only increases demands
3. DO NOT DELETE EVIDENCE - Save everything
4. STOP ALL COMMUNICATION with blackmailer immediately
5. Block blackmailer on all platforms (WhatsApp, Instagram, email, etc.)
6. Take screenshots of ALL threats, messages, emails
7. DO NOT share more images/videos under pressure
8. Tell a trusted person (friend, family, counselor)

EVIDENCE PRESERVATION (URGENT):
✓ Screenshot ALL threatening messages (include timestamps)
✓ Save chat export from WhatsApp (Chat → More → Export Chat)
✓ Screenshot blackmailer's profile/account details
✓ Save emails with full headers
✓ Record phone numbers/UPI IDs/account numbers
✓ Screenshot payment demands
✓ Note platform where initial contact happened
✓ Save any fake/morphed images they sent (for evidence)

NATIONAL CYBERCRIME PORTAL - SPECIAL REPORTING:
1. Visit https://cybercrime.gov.in
2. Click "Report Crime Related to Women/Child" (Special Category)
3. This ensures priority handling and confidentiality
4. Select Category: "Sexually Explicit Content" OR "Cyber Stalking/Bullying of Women/Children"
5. Complete details with maximum information
6. Upload ALL screenshots and evidence
7. Save complaint acknowledgment number (CCN2025XXXXX)

HELPLINES (IMMEDIATE SUPPORT):
- National Cyber Crime Helpline: 1930 (24x7)
- Women's Helpline: 181 (24x7)
- Cyber Crime Reporting: Call 1930 for immediate assistance
- These are trained professionals, conversation is confidential

POLICE REPORTING:
1. File FIR at nearest Cyber Cell or Police Station
2. Specifically mention you've filed online complaint (provide CCN number)
3. Request woman police officer if victim is female
4. Legal provisions to cite:
   - Section 354A IPC: Sexual harassment
   - Section 354C IPC: Voyeurism
   - Section 354D IPC: Stalking
   - Section 384/385 IPC: Extortion/Putting person in fear
   - Section 503/506 IPC: Criminal intimidation
   - IT Act Section 66E: Privacy violation
   - IT Act Section 67/67A: Publishing obscene content

PLATFORM REPORTING:
Report to platform immediately for content removal:

WhatsApp:
- Settings → Help → Contact Us → Report sextortion
- Forward threatening messages to WhatsApp: +91 96500 95095

Instagram/Facebook:
- Report account for "Blackmail or Extortion"
- Report specific messages/posts
- Meta will investigate and may remove content

Email (Gmail/Others):
- Report as phishing/abuse
- Block sender
- Set up filters to auto-delete

FINANCIAL FRAUD (If Paid):
- Call 1930 immediately for transaction freeze
- Report to bank with complaint number
- Request chargeback
- Provide UPI ID/account number of fraudster

LEGAL ACTIONS:
1. Cyber cell will trace blackmailer through:
   - Phone number (with telecom records)
   - UPI ID/bank account
   - IP address from platform
   - Device metadata from images/videos

2. Police can issue notices to platforms for:
   - User data disclosure
   - Content removal
   - Account blocking

3. Court can order:
   - Pre-publication injunction (prevent sharing)
   - Take down notices to platforms
   - Compensation for victim

CONTENT REMOVAL:
If intimate content is published online:
1. Report immediately to cybercrime.gov.in
2. Request urgent content removal
3. Report to platform's abuse team
4. Police will issue take-down notice
5. File complaint under IT Act Section 67A (sexually explicit content)

COUNSELING & SUPPORT:
- Most states have Cyber Crime Victim Support Centers
- Free counseling available
- Contact through cybercrime portal or 1930 helpline
- Mental health professionals trained for cyber crime victims

IMPORTANT FACTS:
✓ Sharing intimate images is NOT a crime by victim
✓ You will NOT be arrested or prosecuted
✓ Complaint filing is CONFIDENTIAL
✓ Police are trained to handle sensitively
✓ Blackmailers are professionals - likely targeting many people
✓ Paying does NOT stop demands - they always ask for more
✓ Most content is NEVER actually shared (it's a bluff)

PRIVACY PROTECTION:
- Complaint marked as sensitive on portal
- Limited access to case details
- Court hearings can be in-camera (private)
- Victim's name not published in media
- Evidence handled confidentially

AFTER REPORTING:
- Track complaint status on cybercrime portal
- Cooperate with investigating officer
- Provide any additional evidence if requested
- Don't communicate with blackmailer even if they contact again
- Report any new threats immediately

PREVENTION TIPS:
- Don't share intimate content online (even with trusted people)
- Don't accept video calls from strangers
- Be cautious on dating apps
- Use privacy settings on social media
- Don't click suspicious links
- Cover webcam when not in use
- Be skeptical of online relationships

Remember: Law enforcement takes these cases seriously. You have legal protection. The blackmailer is committing multiple crimes. Report immediately and don't negotiate with criminals.
"""
    },
    {
        "id": "phishing_email_sop",
        "title": "Phishing Email/SMS/Call - Identification & Reporting",
        "category": "phishing",
        "content": """
PHISHING ATTACK - STANDARD OPERATING PROCEDURE

WHAT IS PHISHING:
- Fake emails/SMS pretending to be from banks, government, or companies
- Fraudulent calls claiming to be from officials
- Messages with malicious links to steal passwords/OTP
- Fake websites mimicking legitimate services
- Social engineering to extract sensitive information

COMMON PHISHING SCENARIOS:
- "Your account will be blocked, click here to verify"
- "KYC update required, update now"
- "Suspicious activity detected, verify immediately"
- "You've won a prize, claim now"
- "Your package is pending, pay customs duty"
- "Income tax refund available, click to claim"
- "Aadhaar/PAN linked to account, update now"
- Calls claiming to be from bank/police/courier company

IMMEDIATE ACTIONS:
1. DO NOT click any links in suspicious messages
2. DO NOT call back unknown numbers claiming to be officials
3. DO NOT share OTP, password, CVV, PIN, Aadhaar, PAN
4. DO NOT download attachments from unknown senders
5. Take screenshot of phishing message/email
6. Check sender's email address/phone number carefully
7. Visit official website directly (type URL, don't click link)

IDENTIFY PHISHING:
Red Flags in Emails:
✗ Sender email doesn't match official domain
  (e.g., sbi@gmail.com instead of sbi.co.in)
✗ Generic greetings ("Dear Customer" not your name)
✗ Urgent language creating panic
✗ Spelling/grammar mistakes
✗ Suspicious links (hover to see real URL)
✗ Requests for sensitive information
✗ Threats of account closure/legal action
✗ Unexpected attachments

Red Flags in SMS/WhatsApp:
✗ Unknown sender ID or random number
✗ Messages about accounts you don't have
✗ Shortened URLs (bit.ly, tinyurl)
✗ Requests to call back immediately
✗ Prize/lottery you didn't enter

Red Flags in Phone Calls:
✗ Caller asks for OTP, PIN, CVV, password
✗ Threats of arrest/account freeze
✗ Pressure to act immediately
✗ Asks you to install remote access app (AnyDesk, TeamViewer)
✗ Claims to be from bank but doesn't know your details
✗ Asks you to transfer money to "safe account"

REPORTING PROCEDURE:

1. NATIONAL CYBERCRIME PORTAL:
   - Visit https://cybercrime.gov.in
   - Click "Report Other Cybercrimes"
   - Category: "Online and Social Media Related Crime" → "Cyber Attack/Phishing"
   - Provide: Phishing message/email screenshot, sender details, link URL
   - Upload evidence and submit

2. REPORT TO SPECIFIC AUTHORITIES:

   For Banking Phishing:
   - Forward to your bank's official phishing email
   - SBI: report.phishing@sbi.co.in
   - ICICI: phishing@icicibank.com
   - HDFC: phishing@hdfcbank.com
   - Call bank customer care to verify any suspicious communication

   For Government Impersonation:
   - Income Tax phishing: Report to incometax.gov.in
   - UIDAI (Aadhaar): report@uidai.gov.in
   - RBI: report.phishing@rbi.org.in

   For Email Phishing:
   - Gmail: Report as phishing (select message → Report phishing)
   - Outlook: Report message → Phishing
   - Yahoo: Report as spam/phishing

   For SMS Phishing:
   - Forward to 1909 (TRAI's SMS reporting number)
   - Report to your telecom provider
   - Block sender number

3. CERT-IN REPORTING:
   - For critical/widespread phishing attacks
   - Email: incident@cert-in.org.in
   - Website: https://www.cert-in.org.in
   - Provide: Phishing email with full headers, URLs, IP addresses

EVIDENCE TO COLLECT:
✓ Full screenshot of phishing email (include sender, subject, date)
✓ Email headers (show full headers option in email)
✓ Phishing website URL
✓ Screenshot of fake website
✓ SMS sender ID and full message
✓ Phone number of caller (if phishing call)
✓ Call recording (if available)
✓ Any documents/PDFs attached to phishing email

IF YOU CLICKED THE LINK:
1. Disconnect from internet immediately (WiFi/data off)
2. Run antivirus scan on device
3. Change passwords from a DIFFERENT device (not the compromised one)
4. Enable 2FA on all accounts
5. Monitor bank accounts for unauthorized transactions
6. Inform your bank if you entered banking details
7. File complaint on cybercrime portal immediately
8. Factory reset device if malware suspected

IF YOU SHARED INFORMATION:
Banking Details (OTP/CVV/PIN):
- Call bank immediately (1800 numbers on back of card)
- Block cards and request new ones
- Enable transaction alerts
- Monitor account for 30 days
- File complaint on cybercrime portal and call 1930

Aadhaar/PAN Details:
- Lock Aadhaar biometrics: resident.uidai.gov.in
- Check for unauthorized SIM cards on your Aadhaar
- Monitor CIBIL score for fake loans
- File identity theft complaint

Passwords:
- Change password immediately on all accounts using same password
- Enable 2FA everywhere
- Check recent login activity
- Log out all other sessions

PLATFORM-SPECIFIC REPORTING:

WhatsApp Phishing:
- Long press message → Report → Report and Block
- Don't forward suspicious messages
- Verify sender identity before clicking links

Social Media Phishing (Fake Pages):
- Report page/profile to platform
- Don't engage with suspicious DMs
- Verify official pages (blue tick)

PROTECTION MEASURES:
✓ Install antivirus software (Kaspersky, Norton, McAfee)
✓ Keep OS and apps updated
✓ Enable email spam filters
✓ Use password manager (don't reuse passwords)
✓ Enable 2FA on all critical accounts
✓ Verify before trusting (Google official contact details)
✓ Bookmark important websites (don't click links)
✓ Check URL carefully (https, correct spelling)
✓ Never share OTP with anyone (banks never ask)
✓ Be skeptical of unsolicited communications

VERIFICATION METHODS:
Before responding to any email/call/SMS:
1. Check sender email domain carefully
2. Google the phone number/email to check reports
3. Visit official website directly (don't click link)
4. Call official customer care to verify
5. Check for spelling mistakes in URL
6. Look for security indicators (https, padlock)

LEGAL PROVISIONS:
Phishing is punishable under:
- IT Act Section 66C: Identity theft
- IT Act Section 66D: Cheating by personation
- IPC Section 419: Cheating by personation
- IPC Section 420: Cheating

Remember: 
- NO legitimate organization asks for OTP/PIN/password
- Banks NEVER call asking to verify details
- Government websites end in .gov.in or .nic.in
- When in doubt, verify through official channels
- It's better to ignore than to become a victim
"""
    },
    {
        "id": "sim_swap_fraud_sop",
        "title": "SIM Swap/Cloning Fraud - Emergency Response",
        "category": "financial_fraud",
        "content": """
SIM SWAP FRAUD - STANDARD OPERATING PROCEDURE

WHAT IS SIM SWAP FRAUD:
- Fraudster gets duplicate SIM issued in your name
- Your SIM suddenly stops working ("No Service")
- OTPs for banking/apps go to fraudster's device
- Unauthorized transactions happen using OTP access
- Identity theft to access all phone-linked accounts

WARNING SIGNS:
⚠️ Your SIM suddenly shows "No Service" or "Emergency Calls Only"
⚠️ You receive SMS about SIM activation you didn't request
⚠️ Banking OTPs received for transactions you didn't make
⚠️ Cannot make/receive calls unexpectedly
⚠️ Family/friends say your number is unreachable

IMMEDIATE EMERGENCY ACTIONS (Within 10 Minutes):
1. Call telecom provider IMMEDIATELY from another phone
   - Airtel: 121 (from other Airtel) or 9910099100
   - Jio: 1800-889-9999
   - VI (Vodafone-Idea): 199 or 9315012345
   - BSNL: 1503 or 1800-180-1503
2. Request IMMEDIATE blocking of duplicate SIM
3. Get incident reference number from telecom
4. Ask for SIM replacement at your registered address only

URGENT FINANCIAL PROTECTION:
1. Call ALL your banks immediately:
   - Block debit/credit cards
   - Disable online/mobile banking
   - Report potential fraud
   - Request transaction monitoring
2. Call UPI service providers (PhonePe, Google Pay, Paytm):
   - Disable UPI linked to your number
   - Request account freeze if suspicious activity
3. Check bank account immediately for unauthorized transactions
   - If money debited, call 1930 helpline URGENTLY
   - Request transaction reversal/freeze

PROTECT OTHER ACCOUNTS:
From another device (NOT the compromised phone):
1. Change passwords for:
   - Email accounts (Gmail, Outlook, Yahoo)
   - Banking apps
   - Social media (Facebook, Instagram, WhatsApp, Twitter)
   - Payment apps (Paytm, PhonePe, Amazon Pay)
   - E-commerce accounts (Amazon, Flipkart)
2. Enable 2FA using authenticator app (not SMS)
3. Log out all other sessions
4. Check recent login activity

NATIONAL CYBERCRIME PORTAL REPORTING:
1. Visit https://cybercrime.gov.in
2. Select "Report Other Cybercrimes"
3. Category: "Online Financial Fraud" → "Debit/Credit Card Fraud/SIM Swap Fraud"
4. Provide complete details:
   - Your mobile number
   - Telecom operator
   - Date/time SIM stopped working
   - Any unauthorized transactions
   - Bank account details if fraud happened
5. Upload evidence and get complaint number

EVIDENCE TO COLLECT:
✓ SMS about SIM activation (if received)
✓ Screenshot of "No Service" on your phone
✓ Telecom complaint reference number
✓ Bank statement showing unauthorized transactions
✓ OTP SMS logs (if accessible)
✓ Call details record from telecom (request copy)
✓ Any suspicious calls/messages before incident
✓ SIM purchase/registration documents (to prove ownership)

POLICE COMPLAINT (MANDATORY):
1. File FIR at local police station or cyber cell
2. Required documents:
   - ID proof (Aadhaar, PAN, Passport)
   - SIM purchase invoice/registration proof
   - Bank statements (if fraud occurred)
   - Cybercrime portal complaint acknowledgment
3. Cite legal provisions:
   - IT Act Section 66C: Identity theft
   - IT Act Section 66D: Cheating by personation
   - IT Act Section 43: Unauthorized access
   - IPC Section 420: Cheating
   - IPC Section 419: Cheating by impersonation
4. Get FIR copy for bank/insurance claims

TELECOM OPERATOR FOLLOW-UP:
1. Visit telecom store with:
   - Police complaint copy
   - ID proof (Aadhaar, PAN, Passport)
   - Original SIM receipt/registration documents
2. Request:
   - Call detail records (CDR) of duplicate SIM
   - Investigation into fraudulent SIM issuance
   - Details of documents used for duplicate SIM
   - CCTV footage from store (if duplicate issued physically)
3. File written complaint with grievance officer
4. Escalate to TRAI if not resolved:
   - Call 1800-110-420 or SMS to 1909
   - File online complaint: consumercare.trai.gov.in

IF FINANCIAL FRAUD OCCURRED:
1. Call 1930 (National Cyber Crime Helpline) immediately
   - Report all fraudulent transactions
   - Provide: Transaction IDs, amounts, timestamps
   - Get 1930 ticket number for bank coordination
2. File zero-liability claim with bank
   - Most banks have 3-day claim window
   - Provide: FIR copy, cybercrime complaint, police reference
3. Request chargeback for card transactions
4. Inform credit bureaus (CIBIL, Experian) to flag fraud
5. Monitor CIBIL score for unauthorized loans

IDENTITY THEFT PREVENTION:
1. Lock Aadhaar biometrics:
   - Visit: resident.uidai.gov.in
   - Login → Lock/Unlock Biometrics
   - Prevents new SIM issuance using Aadhaar
2. Check SIMs issued on your Aadhaar:
   - Visit: www.tafcop.dgtelecom.gov.in
   - Enter mobile number → Get OTP → View all SIMs
   - Report any unknown SIM connections
3. Enable e-Aadhaar notifications:
   - Get SMS alerts for Aadhaar authentication
4. Freeze CIBIL report temporarily:
   - Prevents loan applications in your name

RECOVERY OF NEW SIM:
1. Visit telecom store with police complaint
2. Carry: Aadhaar, PAN, passport-size photos, FIR copy
3. Request new SIM with same number
4. May take 24-48 hours for activation
5. Port to different operator if security concerns persist

LEGAL ACTION AGAINST TELECOM:
If operator issued duplicate SIM without proper verification:
1. File consumer complaint with District Consumer Forum
2. Claim compensation for:
   - Financial loss due to fraud
   - Mental harassment
   - Negligence in KYC verification
3. Cite TRAI regulations violation
4. Seek damages and service improvement

POST-INCIDENT SECURITY:
✓ Enable SIM PIN lock (Settings → SIM Card Lock)
✓ Set strong PIN for SIM card
✓ Use authenticator apps instead of SMS OTP
✓ Enable biometric authentication on apps
✓ Monitor bank accounts daily for 90 days
✓ Set low transaction limits on UPI
✓ Enable all transaction alerts (email + SMS)
✓ Register for DND (Do Not Disturb) to reduce spam
✓ Don't share OTP or personal details on calls
✓ Regularly check TAFCOP portal for SIMs on your name

PREVENTION MEASURES:
✓ Keep Aadhaar biometrics locked when not needed
✓ Don't share OTP with anyone (even "customer care")
✓ Verify caller identity before sharing information
✓ Use physical security key for 2FA (YubiKey)
✓ Regularly update phone number with banks
✓ Enable email alerts in addition to SMS
✓ Check for suspicious account activity weekly
✓ Report lost phone immediately to telecom

RED FLAGS TO WATCH:
- Unsolicited calls asking for Aadhaar/OTP
- SMS about KYC update from unknown numbers
- Calls claiming SIM upgrade needed
- Requests to install remote access apps
- Pressure to share personal information urgently

Remember: Telecom operators must verify identity properly before issuing duplicate SIM. If fraud occurred due to their negligence, you can claim compensation. Act within first hour to minimize damage.
"""
    },
    {
        "id": "cert_in_reporting_sop",
        "title": "CERT-In Mandatory Reporting - For Organizations & Critical Incidents",
        "category": "organizational",
        "content": """
CERT-IN MANDATORY REPORTING - STANDARD OPERATING PROCEDURE

WHO MUST REPORT TO CERT-IN:
- Service providers, intermediaries, data centers, body corporates
- Government organizations
- Victims of critical/large-scale cyber incidents
- Organizations experiencing data breaches affecting citizens
- Critical infrastructure targets

MANDATORY 6-HOUR REPORTING REQUIREMENT:
As per IT Amendment Rules 2022, certain incidents MUST be reported to CERT-In within 6 hours:

REPORTABLE INCIDENTS:
1. Data breach exposing personal/financial information
2. Unauthorized access to systems/networks
3. Website defacement
4. Malware/ransomware attacks
5. Server/network intrusions
6. Phishing attacks targeting organization
7. DDoS (Distributed Denial of Service) attacks
8. Unauthorized modification/destruction of data
9. Malicious code deployment
10. Identity theft impacting multiple users
11. Attacks on critical infrastructure
12. Incidents with cross-border implications

REPORTING TIMELINE:
- Within 6 hours of noticing or being brought to notice
- Initial report can be preliminary (full details can follow)
- Clock starts from when incident is discovered, not when it occurred

HOW TO REPORT TO CERT-IN:

1. EMAIL REPORTING:
   - Primary: incident@cert-in.org.in
   - Alternative: certinops@cert-in.org.in
   - Subject: "Cyber Security Incident Report - [Your Organization]"

2. WEB REPORTING:
   - Visit: https://www.cert-in.org.in
   - Navigate: Services → Incident Reporting
   - Fill online form with all details

3. FAX REPORTING:
   - Fax number: +91-11-24368546

INFORMATION TO PROVIDE:

INCIDENT DETAILS:
- Organization name and contact information
- Date and time of incident occurrence
- Date and time of incident detection
- Nature of incident (breach, attack type, malware, etc.)
- Systems/networks affected
- Impact assessment (users affected, data compromised)
- Geographical scope (India-only or cross-border)
- Suspected origin of attack (if known)
- IP addresses involved (source and target)
- Domains/URLs involved
- IOCs (Indicators of Compromise): file hashes, malware signatures

TECHNICAL DETAILS:
- Operating systems and applications affected
- Vulnerability exploited (CVE numbers if known)
- Attack vectors used
- Forensic evidence collected
- Logs and artifacts

IMPACT ASSESSMENT:
- Number of users/customers affected
- Type of data compromised (personal, financial, health, etc.)
- Business/service disruption duration
- Estimated financial impact
- Reputational damage
- Regulatory/compliance implications

RESPONSE ACTIONS TAKEN:
- Immediate containment measures
- Systems isolated or shut down
- Malware removal steps
- Password resets
- User notifications
- Law enforcement engagement
- External incident response team involvement

EVIDENCE COLLECTION FOR CERT-IN:
✓ System logs (firewall, server, application logs)
✓ Network traffic captures (PCAP files)
✓ Malware samples (in password-protected zip)
✓ Screenshots of attack evidence
✓ Email headers (for phishing)
✓ Database logs (for breach)
✓ Forensic disk images (for critical incidents)
✓ Timeline of events
✓ IOCs (IP addresses, file hashes, domains)

SAMPLE INCIDENT REPORT FORMAT:

Subject: Cyber Security Incident Report - [Organization Name]

1. ORGANIZATION DETAILS:
   - Name:
   - Contact Person:
   - Email:
   - Phone:
   - Address:

2. INCIDENT SUMMARY:
   - Type: [Data Breach/Ransomware/Phishing/DDoS/etc.]
   - Severity: [Critical/High/Medium/Low]
   - Status: [Ongoing/Contained/Resolved]

3. TIMELINE:
   - Incident Occurrence: [Date/Time]
   - Detection: [Date/Time]
   - Reporting: [Date/Time]

4. TECHNICAL DETAILS:
   - Affected Systems: [List]
   - Attack Vector: [Description]
   - Vulnerabilities: [CVE/Details]
   - Source IPs: [List]
   - Destination IPs: [List]

5. IMPACT:
   - Users Affected: [Number]
   - Data Compromised: [Type and volume]
   - Service Disruption: [Duration]
   - Geographic Scope: [India/Cross-border]

6. RESPONSE ACTIONS:
   - [List all actions taken]

7. EVIDENCE:
   - [List attached files/logs]

8. ADDITIONAL INFORMATION:
   - [Any other relevant details]

CERT-IN COORDINATION:

After Reporting:
1. CERT-In may request additional information
2. Respond promptly to all queries
3. Provide forensic evidence if requested
4. Coordinate with CERT-In incident handlers
5. Follow remediation advisories issued

CERT-In Will:
- Acknowledge receipt of report
- Provide incident tracking number
- Issue advisories/alerts if needed
- Coordinate with law enforcement if required
- Share IOCs with community (anonymized)
- Provide technical assistance

FOLLOW-UP REPORTING:
- Provide updates as investigation progresses
- Final report within 30 days with:
  - Root cause analysis
  - Full impact assessment
  - Remediation steps completed
  - Lessons learned

FOR INDIVIDUALS (Non-organizational):

Critical incidents individuals should report to CERT-In:
- Large-scale phishing campaigns
- Zero-day vulnerability discoveries
- Critical infrastructure threats
- National security implications
- Mass data breaches as victim

Individual Reporting:
- Email: incident@cert-in.org.in
- Provide: Detailed description, evidence, your contact info
- CERT-In will assess and take appropriate action

CERT-IN RESOURCES:

Advisories & Alerts:
- Website: www.cert-in.org.in
- Subscribe to mailing list for security advisories
- Check regularly for vulnerability updates

Botnet Cleaning Centers:
- Free malware detection and removal
- List available on CERT-In website

Cyber Swachhta Kendra:
- Free tools to detect and remove malware
- Visit: www.cyberswachhtakendra.gov.in

Training & Awareness:
- CERT-In conducts regular training programs
- Cyber security awareness resources available

LEGAL FRAMEWORK:
- Information Technology Act, 2000
- IT (The Indian Computer Emergency Response Team and Manner of Performing Functions and Duties) Rules, 2013
- IT Amendment Rules, 2022 (6-hour reporting mandate)

NON-COMPLIANCE CONSEQUENCES:
- Penalties under IT Act
- License/registration cancellation
- Legal action for negligence
- Increased scrutiny from regulators
- Reputational damage

BEST PRACTICES:
✓ Establish incident response team before incident occurs
✓ Maintain incident response playbook
✓ Conduct regular security drills
✓ Keep CERT-In contact details readily available
✓ Train staff on reporting procedures
✓ Maintain audit logs with minimum 180-day retention
✓ Deploy SIEM for real-time monitoring
✓ Establish secure communication channel with CERT-In
✓ Review CERT-In advisories weekly
✓ Implement recommended security measures

COORDINATION WITH OTHER AGENCIES:
Report to CERT-In first, then:
- Cybercrime portal (cybercrime.gov.in) for citizen complaints
- Local cyber cell for criminal investigation
- Data Protection Authority (when operational)
- Sector regulators (RBI for banks, SEBI for securities, etc.)
- Law enforcement if criminal activity suspected

Remember: Timely reporting to CERT-In helps:
- Contain threats before spread
- Protect other organizations
- Enable coordinated response
- Access expert technical assistance
- Fulfill legal obligations
"""
    }
]


async def save_documents_to_file():
    """Save SOP documents to JSONL file"""
    try:
        output_file = Path("data/processed/sop_documents.jsonl")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for doc in SOP_DOCUMENTS:
                f.write(json.dumps(doc) + '\n')
        
        logger.info(f"✓ Saved {len(SOP_DOCUMENTS)} SOP documents to {output_file}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to save documents: {e}")
        return False


async def populate_vector_database():
    """Populate ChromaDB with SOP documents"""
    try:
        logger.info("Initializing embedding service...")
        await embedding_service.initialize()
        
        logger.info("Initializing RAG service...")
        await rag_service.initialize()
        
        # Prepare documents for ingestion
        documents = []
        metadatas = []
        ids = []
        
        for doc in SOP_DOCUMENTS:
            documents.append(doc['content'])
            metadatas.append({
                'source': 'cybercrime.gov.in',
                'category': doc['category'],
                'title': doc['title'],
                'document_id': doc['id']
            })
            ids.append(doc['id'])
        
        logger.info(f"Adding {len(documents)} documents to vector database...")
        await rag_service.add_documents(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        # Verify ingestion
        total_docs = rag_service.get_document_count()
        logger.info(f"✓ Vector database populated successfully! Total documents: {total_docs}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to populate vector database: {e}")
        return False


def main():
    """Main data population function"""
    print("\n" + "="*80)
    print("    DATA POPULATION - CYBERCRIME SOP DOCUMENTS")
    print("="*80 + "\n")
    
    # Save documents to file
    file_success = asyncio.run(save_documents_to_file())
    
    # Populate vector database
    db_success = asyncio.run(populate_vector_database())
    
    print("\n" + "="*80)
    if file_success and db_success:
        print("    ✓ DATA POPULATION COMPLETE")
        print(f"    {len(SOP_DOCUMENTS)} comprehensive SOP documents loaded")
        print("\n    Documents cover:")
        print("    - UPI/Financial Fraud")
        print("    - Social Media Hacking")
        print("    - Online Job Fraud")
        print("    - Sextortion/Blackmail")
        print("    - Phishing Attacks")
        print("    - SIM Swap Fraud")
        print("    - CERT-In Reporting")
    else:
        print("    ✗ DATA POPULATION FAILED - Please check errors above")
    print("="*80 + "\n")
    
    return 0 if (file_success and db_success) else 1


if __name__ == "__main__":
    sys.exit(main())

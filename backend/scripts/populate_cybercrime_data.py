"""
Populate ChromaDB with comprehensive Indian cybercrime reporting data
This script creates a rich knowledge base for the RAG system
"""
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.rag_service import rag_service
from app.services.embedding_service import embedding_service
from app.core.logging import logger

# Comprehensive Indian cybercrime data
CYBERCRIME_DOCUMENTS = [
    {
        "title": "National Cyber Crime Reporting Portal - Overview",
        "content": """The National Cyber Crime Reporting Portal (https://cybercrime.gov.in) is the official Government of India platform for reporting cybercrimes. Citizens can report various types of cybercrimes online without visiting a police station. The portal is available 24/7 and supports anonymous reporting. Key features include:
- Online complaint registration
- Complaint tracking system
- Helpline number: 1930 (24x7)
- Email: complaints@cybercrime.gov.in
- Support for all Indian states and union territories
- Multi-language support
- Mobile app available (Cybercrime Helpline)""",
        "category": "portal_information",
        "source": "cybercrime.gov.in",
        "url": "https://cybercrime.gov.in"
    },
    {
        "title": "Financial Fraud - UPI/Online Banking Scams",
        "content": """If you lose money through UPI/online banking fraud, take immediate action:

IMMEDIATE STEPS (Within 10 minutes):
1. Call your bank's customer care immediately
2. Report to National Cyber Crime Helpline: 1930
3. Block your account/freeze card through banking app
4. Do NOT share OTP or delete any messages

WITHIN 24 HOURS:
1. File FIR at nearest cybercrime police station OR online at cybercrime.gov.in
2. Register complaint on https://cybercrime.gov.in/Webform/Crime_AuthoLogin.aspx
3. Lodge complaint with your bank in writing
4. File complaint with RBI ombudsman if needed

EVIDENCE TO COLLECT:
- Transaction IDs and UPI reference numbers
- Screenshots of fraudulent messages/calls
- Bank statement showing unauthorized transactions
- Phone numbers/UPI IDs used by scammers
- Timeline of events

IMPORTANT: Money recovery is possible if reported within 24 hours. Banks can freeze fraudulent accounts.""",
        "category": "financial_fraud",
        "source": "Reserve Bank of India Guidelines",
        "url": "https://www.rbi.org.in"
    },
    {
        "title": "Social Media Account Hacking - Instagram, Facebook, WhatsApp",
        "content": """If your social media account (Instagram, Facebook, WhatsApp, Twitter) is hacked:

IMMEDIATE ACTIONS:
1. Try to regain access using 'Forgot Password' with linked email/phone
2. Alert friends/followers about the hack through alternative accounts
3. Report to the platform immediately using their reporting tools

PLATFORM-SPECIFIC REPORTING:
Instagram: Settings → Help → Report a Problem → Account Compromised
Facebook: facebook.com/hacked → Follow recovery steps
WhatsApp: Email support@whatsapp.com with registered number
Twitter: help.twitter.com → Report hacked account

LEGAL REPORTING:
1. File complaint on cybercrime.gov.in
2. If identity theft/impersonation occurs, file FIR under IT Act Section 66C
3. If objectionable content is posted from your account, report immediately to avoid legal liability

EVIDENCE NEEDED:
- Screenshots of hacking notification
- Last known login details
- Any communication from hacker
- List of posted content during hack

PREVENTION:
- Enable two-factor authentication (2FA)
- Use strong, unique passwords
- Don't click suspicious links
- Regular security checkup""",
        "category": "social_media_hacking",
        "source": "Ministry of Electronics and IT",
        "url": "https://www.meity.gov.in"
    },
    {
        "title": "Online Blackmail and Sextortion",
        "content": """Online blackmail/sextortion is a serious crime under IT Act 2000. If you're being blackmailed:

CRITICAL STEPS:
1. DO NOT comply with demands - paying encourages more demands
2. DO NOT delete any evidence
3. Stop all communication with the blackmailer
4. Report IMMEDIATELY to Cyber Crime Helpline: 1930

SAFE REPORTING:
1. File complaint at https://cybercrime.gov.in (option for women/children)
2. Women can call Women Helpline: 181 or 1091
3. Child victims: Report to National Commission for Protection of Child Rights (NCPCR) or CHILDLINE: 1098
4. Visit nearest women's police station or cyber cell

LEGAL PROVISIONS:
- IT Act Section 67: Publishing obscene content (7 years imprisonment)
- IT Act Section 66E: Privacy violation (3 years imprisonment)
- IPC Section 354A: Sexual harassment (3 years imprisonment)
- IPC Section 509: Insulting modesty (1-3 years imprisonment)

EVIDENCE TO PRESERVE:
- Screenshots of threatening messages (without sharing content)
- Email headers, phone numbers, social media profiles
- Payment demands and account details
- Entire conversation history

SUPPORT SERVICES:
- Women Helpline: 181 (24x7)
- Cyber Crime Helpline: 1930
- One Stop Centre: 181
- National Commission for Women: ncw.nic.in

ALL COMPLAINTS ARE CONFIDENTIAL. Police will help without judgment.""",
        "category": "blackmail_sextortion",
        "source": "National Commission for Women",
        "url": "https://ncw.nic.in"
    },
    {
        "title": "Job Fraud and Work-from-Home Scams",
        "content": """Job fraud and fake work-from-home schemes are common cybercrimes. Red flags and reporting:

WARNING SIGNS:
- Asking for registration/processing fees
- Unrealistic salary promises (₹50,000+ for simple tasks)
- No proper company verification
- Asking for ID card/Aadhar card before hiring
- WhatsApp/Telegram-based "companies"
- Asking to make purchases/click ads

IF SCAMMED:
1. Report immediately on cybercrime.gov.in
2. Note down all company details, phone numbers, email IDs
3. If money paid, note transaction IDs and call bank
4. Report company on job portals (Naukri, Indeed, etc.)

EVIDENCE TO COLLECT:
- Job advertisement screenshots
- Email/WhatsApp communications
- Payment receipts
- Company website URL
- Recruiter contact details

VERIFICATION TIPS:
- Check company on Ministry of Corporate Affairs website (mca.gov.in)
- Verify company GST number
- Google company name + "scam" or "fraud"
- Never pay for jobs in government sectors
- Legitimate companies never ask for money upfront

LEGAL ACTION:
File FIR under:
- IPC Section 420: Cheating
- IT Act Section 66D: Cheating by personation using computer resources

PLATFORMS TO REPORT:
- cybercrime.gov.in
- National Consumer Helpline: 1915
- Consumer forum online complaint""",
        "category": "job_fraud",
        "source": "Department of Consumer Affairs",
        "url": "https://consumerhelpline.gov.in"
    },
    {
        "title": "Online Shopping Fraud - Fake E-commerce Sites",
        "content": """Online shopping fraud reporting and prevention:

IF YOU'RE SCAMMED:
1. Contact seller/platform customer care immediately
2. Raise dispute on payment platform (PayTM, GPay, credit card)
3. File complaint on National Consumer Helpline: 1915
4. Report on cybercrime.gov.in within 24 hours

PLATFORM-SPECIFIC:
Amazon: A-to-Z Guarantee Protection
Flipkart: Buyer Protection
Meesho/Others: Customer care escalation

PAYMENT FRAUD:
- Credit Card: Call bank, report fraudulent transaction
- UPI/Netbanking: Report to bank + cybercrime portal
- Cash on Delivery scams: Consumer forum complaint

EVIDENCE REQUIRED:
- Order confirmation email
- Payment receipts/transaction IDs
- Screenshots of product page
- Chat history with seller
- Tracking information
- Photos of received product (if wrong item)

CONSUMER PROTECTION:
1. File on National Consumer Helpline (NCH): 1915 or consumerhelpline.gov.in
2. Consumer court complaint (free for claims up to ₹10 lakh)
3. Report on INGRAM (Indian Grievance Resolution and Assistance Mechanism)

LEGAL PROVISIONS:
- Consumer Protection Act 2019
- IT Act Section 66D: Cheating by impersonation
- IPC Section 420: Cheating

PREVENTION:
- Check seller ratings and reviews
- Use COD for first purchase
- Verify website SSL certificate
- Avoid too-good-to-be-true deals
- Don't shop on random social media links""",
        "category": "shopping_fraud",
        "source": "National Consumer Helpline",
        "url": "https://consumerhelpline.gov.in"
    },
    {
        "title": "SIM Swap Fraud",
        "content": """SIM swap fraud is when criminals get a duplicate SIM to access your bank accounts and OTPs.

IMMEDIATE ACTIONS IF SUSPECTED:
1. If your SIM suddenly stops working, call telecom provider IMMEDIATELY
2. Block all bank accounts through alternate number
3. Change all passwords using different device
4. Report to Cyber Crime Helpline: 1930

HOW IT HAPPENS:
- Scammers get your SIM reissued using fake documents
- They receive all your OTPs and messages
- Access your bank accounts and UPI apps
- Transfer money to their accounts

REPORTING STEPS:
1. File complaint with telecom provider (Airtel, Jio, VI, BSNL)
2. Lodge FIR at cyber cell or online at cybercrime.gov.in
3. Inform all banks in writing
4. Report to Department of Telecommunications (DoT)

EVIDENCE NEEDED:
- SIM replacement details from telecom
- Unauthorized transactions list
- Timeline of when SIM stopped working
- Any suspicious calls received earlier

LEGAL ACTION:
- IT Act Section 66C: Identity theft (3 years imprisonment)
- IT Act Section 66D: Cheating by impersonation
- IPC Section 419/420: Cheating and impersonation

TELECOM HELPLINES:
- Airtel: 121
- Jio: 198 / 1800 889 9999
- Vodafone Idea: 199
- BSNL: 1503/1800

PREVENTION:
- Never share SIM details/Aadhar with unknown persons
- Set SIM PIN lock
- Enable bank transaction alerts
- Don't keep Aadhar/PAN/voter ID soft copies on phone""",
        "category": "sim_swap_fraud",
        "source": "TRAI Guidelines",
        "url": "https://www.trai.gov.in"
    },
    {
        "title": "Fake Loan Apps and Recovery Harassment",
        "content": """Fake instant loan apps and recovery harassment are serious crimes:

IF YOU'VE USED FAKE LOAN APP:
1. DO NOT pay recovery agents through personal accounts
2. Report harassment immediately to cyber crime: 1930
3. These apps are illegal if not RBI-registered
4. You're NOT legally bound to pay

HARASSMENT TACTICS:
- Morphing photos from your phone
- Calling contacts from phone
- Threatening messages
- Defamation on WhatsApp groups

LEGAL PROTECTION:
- These apps have NO legal right to harass
- Accessing phone data without consent is illegal
- Morphing photos is punishable offense

REPORTING:
1. File complaint on cybercrime.gov.in
2. Report app on Google Play Store
3. If harassment continues, file FIR under IPC Section 384 (Extortion)
4. Register with RBI Ombudsman

EVIDENCE:
- App name and screenshots
- Recovery agent numbers
- Harassing messages/calls recordings
- Loan agreement (if any)

CHECKING LOAN APP LEGITIMACY:
- Visit RBI website → Check NBFC list
- Verify company registration on MCA portal
- Check app reviews
- Legitimate lenders never ask for:
  * Photo gallery access
  * Contact list access
  * Upfront fees

SUPPORT:
- RBI Complaint Portal: https://cms.rbi.org.in
- Legal Rights Society helplines
- Cyber Crime Helpline: 1930

KNOW YOUR RIGHTS:
- Lenders can only call you, not contacts
- Cannot threaten or defame
- Cannot access personal photos
- Recovery must be through legal channels only""",
        "category": "loan_app_fraud",
        "source": "Reserve Bank of India",
        "url": "https://rbi.org.in"
    },
    {
        "title": "Cryptocurrency and Investment Scams",
        "content": """Cryptocurrency and investment scams are rising. Stay protected:

COMMON SCAMS:
- Fake crypto exchanges
- Guaranteed return schemes
- Pump and dump schemes
- Ponzi schemes disguised as crypto
- Celebrity impersonation crypto scams
- Fake investment advisors on Telegram/WhatsApp

WARNING SIGNS:
- Guaranteed high returns (30-40% monthly)
- Pressure to invest quickly
- Referral bonuses/MLM structure
- Unregistered platforms
- No proper company registration
- Celebrity endorsements (usually fake)

IF SCAMMED:
1. Stop all further investments immediately
2. Report on cybercrime.gov.in
3. Report to SEBI (Securities and Exchange Board of India)
4. File complaint with Economic Offences Wing
5. Report to Financial Intelligence Unit (FIU)

EVIDENCE TO COLLECT:
- Platform name and website
- Investment receipts and transaction IDs
- Wallet addresses used
- Promotional material/promises
- Communication with operators
- Referral links

LEGAL PROVISIONS:
- Prize Chits and Money Circulation Schemes (Banning) Act 1978
- IPC Section 420: Cheating
- Companies Act violations

VERIFICATION:
- Check SEBI registered advisors: sebi.gov.in
- Verify crypto exchange registration
- No legitimate investment promises guaranteed returns
- RBI has NOT approved any cryptocurrency

REPORTING PORTALS:
- SEBI Scores: scores.gov.in
- Cyber Crime Portal: cybercrime.gov.in
- RBI: rbi.org.in
- Economic Offences: Contact state EOW

SAFE INVESTING:
- Only use recognized exchanges
- Research thoroughly
- Never invest based on social media tips
- Avoid pressure tactics
- If it sounds too good, it's probably a scam
- Crypto is highly volatile and risky""",
        "category": "investment_fraud",
        "source": "SEBI & Reserve Bank of India",
        "url": "https://www.sebi.gov.in"
    },
    {
        "title": "Cyberbullying and Online Harassment",
        "content": """Cyberbullying and online harassment are punishable offenses in India:

FORMS OF CYBERBULLYING:
- Repeated threatening messages
- Posting embarrassing photos/videos
- Creating fake profiles to harass
- Spreading rumors online
- Excluding from online groups deliberately
- Sending offensive content repeatedly

IF YOU'RE A VICTIM:
1. DO NOT respond to bully - it encourages them
2. Block the person on all platforms
3. Screenshot everything as evidence
4. Report to platform (Instagram, Facebook, etc.)
5. Report to cybercrime.gov.in

FOR CHILDREN/TEENS:
- Tell a trusted adult immediately
- Contact CHILDLINE: 1098
- Report to school authorities
- National Commission for Protection of Child Rights: ncpcr.gov.in

PLATFORM REPORTING:
Instagram: Report → Bullying or Harassment
Facebook: Report User → Harassment
WhatsApp: Block and Report
YouTube: Report → Harassment/Cyberbullying

LEGAL PROVISIONS:
- IT Act Section 66A (if applicable): Offensive messages
- IT Act Section 67: Publishing obscene content
- IPC Section 354D: Stalking (2 years imprisonment)
- IPC Section 506: Criminal intimidation
- IPC Section 509: Insulting modesty
- POCSO Act for children under 18

EVIDENCE TO PRESERVE:
- Screenshots with timestamps
- URLs of posts/profiles
- List of platforms where harassment occurred
- Witnesses (if any)

SUPPORT SERVICES:
- Cyber Crime Helpline: 1930
- CHILDLINE: 1098 (for children)
- Women Helpline: 181
- iCALL Psychosocial Helpline: 9152987821

SCHOOLS:
- Schools must have anti-bullying policies
- Cyber Safety Education is mandatory

MENTAL HEALTH SUPPORT:
- Vandrevala Foundation: 1860 2662 345
- NIMHANS Helpline: 080-46110007
- iCall: 9152987821

Remember: You're NOT alone. Cyberbullying is a crime and help is available.""",
        "category": "cyberbullying",
        "source": "Ministry of Women & Child Development",
        "url": "https://wcd.nic.in"
    },
    {
        "title": "IT Act 2000 - Key Sections for Cybercrimes",
        "content": """Information Technology Act 2000 - Key provisions for reporting cybercrimes:

SECTION 43: Penalty for damage to computer systems
- Unauthorized access to computers
- Downloading data without permission
- Introducing viruses
- Penalty: Compensation up to ₹1 crore

SECTION 66: Computer-related offenses
- Hacking computer systems
- Punishment: 3 years imprisonment and/or fine up to ₹5 lakh

SECTION 66A: Offensive messages (Struck down by Supreme Court in 2015)

SECTION 66B: Dishonestly receiving stolen computer resources
- Punishment: 3 years and/or fine up to ₹1 lakh

SECTION 66C: Identity theft
- Using another person's digital signature/password
- Punishment: 3 years and/or fine up to ₹1 lakh

SECTION 66D: Cheating by personation using computer resources
- Impersonating someone online for fraud
- Punishment: 3 years and/or fine up to ₹1 lakh

SECTION 66E: Privacy violation
- Publishing private images without consent
- Punishment: 3 years and/or fine up to ₹2 lakh

SECTION 66F: Cyber terrorism
- Threatening country's security through cyberspace
- Punishment: Life imprisonment

SECTION 67: Publishing obscene content
- Electronically publishing obscene material
- Punishment: First conviction 3 years + ₹5 lakh fine
- Second conviction: 5 years + ₹10 lakh fine

SECTION 67A: Publishing sexually explicit content
- Punishment: 5 years + ₹10 lakh (first)
- 7 years + ₹10 lakh (second)

SECTION 67B: Child pornography
- Publishing child sexual abuse material
- Punishment: 5 years (first), 7 years (second) + fine up to ₹10 lakh

SECTION 72: Breach of confidentiality/privacy
- Disclosing information in breach of contract
- Punishment: 2 years and/or fine up to ₹1 lakh

HOW TO FILE COMPLAINT:
1. Identify applicable section(s)
2. File FIR at cyber cell or online
3. Provide detailed evidence
4. Follow up with complaint number

Note: Many cybercrimes also fall under IPC (Indian Penal Code) sections.""",
        "category": "legal_provisions",
        "source": "Information Technology Act 2000",
        "url": "https://www.meity.gov.in"
    },
    {
        "title": "Phishing and Email Scams",
        "content": """Phishing scams and email frauds - How to identify and report:

TYPES OF PHISHING:
- Email phishing (fake bank emails)
- SMS phishing (Smishing)
- Voice phishing (Vishing)
- WhatsApp phishing
- Spear phishing (targeted attacks)

COMMON TACTICS:
- Fake KYC update requests
- Lottery/prize winners
- Bank account suspension threats
- Income tax notices
- COVID-19 related scams
- Job offers
- Parcel delivery failures

RED FLAGS:
- Urgent action required
- Suspicious sender email
- Grammatical errors
- Asking for OTP/password/PIN
- Unknown attachments
- Links to unfamiliar websites

IF YOU CLICKED PHISHING LINK:
1. DO NOT enter any information
2. Close browser immediately
3. Run antivirus scan
4. Change all passwords from different device
5. Monitor bank accounts
6. Report to bank if financial details were entered

REPORTING:
1. Forward phishing email to: report@safinternet.in
2. Report on cybercrime.gov.in
3. If bank-related: Inform bank immediately
4. If tax-related: Report to Income Tax Department

EVIDENCE:
- Original email with headers
- Screenshots of suspicious messages
- SMS sender ID
- Phone numbers used

VERIFICATION:
- Banks NEVER ask for OTP/PIN via email/SMS
- Government never contacts via WhatsApp
- Hover over links to see actual URL
- Check sender email domain carefully
- No legitimate authority asks for Aadhar/PAN via email

PROTECTION:
- Enable spam filters
- Don't click unknown links
- Verify sender independently
- Use two-factor authentication
- Keep software updated
- Be skeptical of urgent messages

REPORT PHISHING SITES:
- Google Safe Browsing: google.com/safebrowsing/report_phish
- Microsoft: microsoft.com/wdsi/support/report-unsafe-site
- CERT-In: cert-in.org.in

BANKING SECURITY:
- Enable transaction alerts
- Register only official bank numbers
- Use bank's official app/website
- Never share CVV/PIN/OTP""",
        "category": "phishing",
        "source": "CERT-In & Ministry of Home Affairs",
        "url": "https://www.cert-in.org.in"
    }
]

async def populate_data():
    """Populate RAG database with cybercrime documents"""
    try:
        print("🚀 Starting ChromaDB population...")
        
        # Initialize services
        print("📦 Initializing RAG service...")
        await rag_service.initialize()
        
        # Check if data already exists
        doc_count = rag_service.get_document_count()
        if doc_count > 0:
            print(f"⚠️  Database already contains {doc_count} documents")
            response = input("Do you want to clear and repopulate? (y/n): ")
            if response.lower() == 'y':
                print("🗑️  Clearing existing data...")
                await rag_service.delete_all()
            else:
                print("✅ Keeping existing data")
                return
        
        # Prepare documents
        documents = []
        metadatas = []
        ids = []
        
        for i, doc in enumerate(CYBERCRIME_DOCUMENTS):
            # Create comprehensive document text
            full_text = f"""Title: {doc['title']}
Category: {doc['category']}
Source: {doc['source']}
URL: {doc.get('url', 'N/A')}

Content:
{doc['content']}"""
            
            documents.append(full_text)
            metadatas.append({
                "title": doc['title'],
                "category": doc['category'],
                "source": doc['source'],
                "url": doc.get('url', ''),
                "doc_id": i
            })
            ids.append(f"doc_{i}")
            
            print(f"📄 Prepared: {doc['title']}")
        
        # Add documents to RAG
        print(f"\n💾 Adding {len(documents)} documents to vector store...")
        await rag_service.add_documents(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"\n✅ Successfully populated {len(documents)} documents!")
        print(f"📊 Total documents in database: {rag_service.get_document_count()}")
        
        # Test retrieval
        print("\n🧪 Testing retrieval...")
        test_query = "How do I report UPI fraud?"
        results = await rag_service.retrieve(test_query, top_k=3)
        print(f"Test query: '{test_query}'")
        print(f"Retrieved {len(results)} relevant documents")
        if results:
            print(f"Top result: {results[0]['source']} (score: {results[0]['score']:.3f})")
        
        print("\n🎉 Data population complete!")
        
    except Exception as e:
        logger.error(f"Error populating data: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        raise
    finally:
        await rag_service.cleanup()

if __name__ == "__main__":
    asyncio.run(populate_data())

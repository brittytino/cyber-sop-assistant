
# Seed Data for Police Stations and Resources
# Used to populate the PostgreSQL database initially

POLICE_STATIONS = [
    {
        "state": "Andhra Pradesh",
        "district": "Visakhapatnam",
        "city": "Visakhapatnam",
        "name": "Cyber Crime Police Station - Visakhapatnam",
        "address": "Police Barracks, Visakhapatnam, Andhra Pradesh 530002",
        "phone": "0891-2563333",
        "email": "cybercrimeps-vsp@appolice.gov.in",
        "is_cyber_cell": True,
        "officer": "Insp. K. Rao",
        "designation": "Inspector"
    },
    {
        "state": "Assam",
        "district": "Kamrup Metropolitan",
        "city": "Guwahati",
        "name": "CID Cyber Crime Police Station",
        "address": "Ulubari, Guwahati, Assam 781007",
        "phone": "0361-2521636",
        "email": "cybercell-cid@assampolice.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Bihar",
        "district": "Patna",
        "city": "Patna",
        "name": "Cyber Crime Police Station - Patna",
        "address": "Beli Road, Patna, Bihar 800001",
        "phone": "0612-2217007",
        "email": "sp-cyber.bihar@gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Delhi",
        "district": "Central Delhi",
        "city": "Delhi",
        "name": "Cyber Crime Cell - Delhi Police HQ",
        "address": "I.P. Estate, New Delhi - 110002",
        "phone": "011-23490000",
        "email": "dgp-cybercrime@delhipolice.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Delhi",
        "district": "South Delhi",
        "city": "Delhi",
        "name": "Hauz Khas Police Station",
        "address": "Hauz Khas, New Delhi - 110016",
        "phone": "011-26863333",
        "email": "ps.hauzkhas@delhipolice.gov.in",
        "is_cyber_cell": False
    },
    {
        "state": "Gujarat",
        "district": "Ahmedabad",
        "city": "Ahmedabad",
        "name": "Cyber Crime Police Station - Ahmedabad",
        "address": "Shahibaug, Ahmedabad, Gujarat 380004",
        "phone": "079-22861917",
        "email": "ccps-ahd@gujarat.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Karnataka",
        "district": "Bangalore Urban",
        "city": "Bengaluru",
        "name": "CID Cyber Crime - Bangalore",
        "address": "Carlton House, Palace Road, Bangalore - 560001",
        "phone": "080-22942825",
        "email": "ccb.cybercrime@ksp.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Maharashtra",
        "district": "Mumbai City",
        "city": "Mumbai",
        "name": "Cyber Crime Cell - Mumbai",
        "address": "BKC, Mumbai - 400051",
        "phone": "022-22027990",
        "email": "cybercell.mumbai@mahapolice.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Tamil Nadu",
        "district": "Chennai",
        "city": "Chennai",
        "name": "Cyber Crime Cell - Tamil Nadu",
        "address": "Police Commissioner Office, Chennai - 600034",
        "phone": "044-23452377",
        "email": "dm-cyber.chennai@tnpolice.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "city": "Coimbatore",
        "name": "Cyber Crime Cell - Coimbatore",
        "address": "Police Commissionerate, Coimbatore - 641018",
        "phone": "0422-2244900",
        "email": "cybercell-cbe@tnpolice.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Telangana",
        "district": "Hyderabad",
        "city": "Hyderabad",
        "name": "Cyber Crime Police Station - Hyderabad",
        "address": "C V Raman Nagar, Hyderabad - 500032",
        "phone": "040-27853508",
        "email": "cybercrime.hyd@tspolice.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Uttar Pradesh",
        "district": "Lucknow",
        "city": "Lucknow",
        "name": "Cyber Crime Police Station - Lucknow",
        "address": "Hazratganj, Lucknow, Uttar Pradesh 226001",
        "phone": "0522-2287232",
        "email": "sp-cyber.la@uppolice.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "West Bengal",
        "district": "Kolkata",
        "city": "Kolkata",
        "name": "Cyber Crime Cell - Kolkata",
        "address": "Lalbazar, Kolkata - 700001",
        "phone": "033-22143028",
        "email": "cybercrime.kol@wbpolice.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Odisha",
        "district": "Khordha",
        "city": "Bhubaneswar",
        "name": "Cyber Crime Police Station - Bhubaneswar",
        "address": "Rasulgarh, Bhubaneswar, Odisha 751010",
        "phone": "0674-2580100",
        "email": "dspcyber.bbsr@odishapolice.gov.in",
        "is_cyber_cell": True
    },
    {
        "state": "Kerala",
        "district": "Thiruvananthapuram",
        "city": "Thiruvananthapuram",
        "name": "Cyber Crime Police Station",
        "address": "Police Headquarters, Thiruvananthapuram, Kerala 695010",
        "phone": "0471-2722500",
        "email": "cyberps.pol@kerala.gov.in",
        "is_cyber_cell": True
    }
]

RESOURCES = [
    {
        "name": "National Cyber Crime Reporting Portal (NCRP)",
        "url": "https://cybercrime.gov.in",
        "category": "Reporting",
        "description": "Official portal to report all types of cybercrimes in India",
        "icon": "🚨",
        "order": 1
    },
    {
        "name": "CEIR - Block Stolen/Lost Mobile",
        "url": "https://ceir.gov.in",
        "category": "Mobile Security",
        "description": "Central Equipment Identity Register - Block lost/stolen mobile devices",
        "icon": "📱",
        "order": 2
    },
    {
        "name": "Tafcop - Know Your Mobile Connections",
        "url": "https://tafcop.dgt.gov.in",
        "category": "Mobile Security",
        "description": "Check mobile connections registered in your name",
        "icon": "📞",
        "order": 3
    },
    {
        "name": "CERT-In",
        "url": "https://www.cert-in.org.in",
        "category": "Security Advisories",
        "description": "Indian Computer Emergency Response Team - Security alerts and guidelines",
        "icon": "🛡️",
        "order": 4
    },
    {
        "name": "Chakshu - Report Fraud Calls/SMS",
        "url": "https://sancharsaathi.gov.in/sfc",
        "category": "Reporting",
        "description": "Report suspected fraud calls and SMS",
        "icon": "☎️",
        "order": 5
    },
    {
        "name": "Report Phishing - RBI",
        "url": "https://rbidocs.rbi.org.in/rdocs/content/docs/FRAUD02092021.htm",
        "category": "Financial Fraud",
        "description": "Report banking and financial phishing to RBI",
        "icon": "🏦",
        "order": 6
    },
    {
        "name": "Cyber Dost",
        "url": "https://twitter.com/Cyberdost",
        "category": "Awareness",
        "description": "Official cyber awareness initiative by Ministry of Home Affairs",
        "icon": "🤝",
        "order": 7
    },
    {
        "name": "National Helpline - 1930",
        "url": "tel:1930",
        "category": "Emergency",
        "description": "Toll-free helpline for reporting cybercrimes",
        "icon": "📞",
        "order": 8
    }
]

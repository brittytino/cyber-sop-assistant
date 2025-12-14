
import sys
import os
from pathlib import Path
import logging
import traceback

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from app.db import SessionLocal, init_db, Base, engine
from app.models import Resource, PoliceStation, Document
from app.services.embedding_client import embed_text
from app.services.rag import get_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hack to support JSON 'null' in pasted data
null = None

def seed_resources(db):
    resources = [
        {"name": "National Cyber Crime Reporting Portal", "url": "https://cybercrime.gov.in", "category": "Reporting", "description": "Official portal for reporting cybercrimes."},
        {"name": "Chakshu (Sanchar Saathi)", "url": "https://sancharsaathi.gov.in/sfc/", "category": "Reporting", "description": "Report suspected fraud communications (Call, SMS, WhatsApp)."},
        {"name": "CERT-In", "url": "https://www.cert-in.org.in", "category": "Advisory", "description": "Indian Computer Emergency Response Team for cyber security incidents."},
        {"name": "Cyber Swachhta Kendra", "url": "https://www.csk.gov.in", "category": "Tools", "description": "Botnet Cleaning and Malware Analysis Centre."},
        {"name": "RBI Sachet", "url": "https://sachet.rbi.org.in", "category": "Financial", "description": "Lodge complaints against illegal acceptance of deposits."},
        {"name": "CEIR", "url": "https://ceir.sancharsaathi.gov.in", "category": "Telecom", "description": "Block lost/stolen mobile phones."},
        {"name": "TAFCOP", "url": "https://tafcop.sancharsaathi.gov.in", "category": "Telecom", "description": "Know the mobile connections issued in your name."},
        {"name": "NCIIPC", "url": "https://nciipc.gov.in", "category": "Security", "description": "National Critical Information Infrastructure Protection Centre."},
        {"name": "Cyber Crime Helpline", "url": "tel:1930", "category": "Helpline", "description": "National Cyber Crime Helpline Number."},
        {"name": "Women & Child Helpline", "url": "tel:1098", "category": "Helpline", "description": "Helpline for women and children."},
        {"name": "ISEA (InfoSec Awareness)", "url": "https://isea.gov.in", "category": "Education", "description": "Information Security Education and Awareness."},
        {"name": "Maharashtra Cyber", "url": "https://cyber.maharashtra.gov.in", "category": "State", "description": "Maharashtra State Cyber Cell."},
        {"name": "Kerala Police Cyber Dome", "url": "https://cyberdome.kerala.gov.in", "category": "State", "description": "Technological Research and Development Centre of Kerala Police."},
        {"name": "Telangana State Cyber Security Bureau", "url": "https://tscsb.telangana.gov.in", "category": "State", "description": "Dedicated cyber crime bureau for Telangana."},
        {"name": "Karnataka Cyber Crime", "url": "https://ksp.karnataka.gov.in", "category": "State", "description": "Karnataka State Police Cyber Crime Division."},
        {"name": "Delhi Police Cyber Cell", "url": "http://cybercelldelhi.in", "category": "State", "description": "Cyber Crime Unit of Delhi Police."},
        {"name": "SEBI Scores", "url": "https://scores.gov.in", "category": "Financial", "description": "SEBI Complaints Redress System."},
        {"name": "National Consumer Helpline", "url": "https://consumerhelpline.gov.in", "category": "Consumer", "description": "Report consumer grievances and fraud."},
        {"name": "DigiLocker", "url": "https://www.digilocker.gov.in", "category": "Utility", "description": "Secure cloud storage for documents."},
        {"name": "Have I Been Pwned", "url": "https://haveibeenpwned.com", "category": "Tools", "description": "Check if your email or phone has been compromised in a data breach."},
        {"name": "VirusTotal", "url": "https://www.virustotal.com", "category": "Tools", "description": "Analyze suspicious files and URLs."},
        {"name": "Kerala Police", "url": "https://keralapolice.gov.in", "category": "State", "description": "Official Kerala Police Website"},
        {"name": "Tamil Nadu Police", "url": "https://eservices.tnpolice.gov.in", "category": "State", "description": "Tamil Nadu Police Citizen Services"},
        {"name": "Andhra Pradesh Police", "url": "https://appolice.gov.in", "category": "State", "description": "Andhra Pradesh Police Portal"},
        {"name": "Gujarat Police", "url": "https://gujaratpolice.org", "category": "State", "description": "Gujarat State Police"}
    ]

    for res in resources:
        existing = db.query(Resource).filter(Resource.url == res["url"]).first()
        if not existing:
            db.add(Resource(**res))
    db.commit()
    logger.info(f"Seeded {len(resources)} resources")

def seed_documents(db):
    """
    Seed Documents table and ChromaDB with initial knowledge
    """
    logger.info("Seeding Documents and Vector Store...")
    
    # 1. Fetch Resources to create initial documents
    resources = db.query(Resource).all()
    
    docs_to_embed = []
    metadatas = []
    ids = []
    
    for i, res in enumerate(resources):
        # Create a document text representation
        doc_content = f"Resource Name: {res.name}\nCategory: {res.category}\nDescription: {res.description}\nURL: {res.url}\nUse this resource for {res.category} related issues."
        
        # Add to SQL
        db_doc = Document(
            source="Official Resource List",
            title=res.name,
            content=doc_content,
            url=res.url, 
            category=res.category,
            chunk_id=f"res_{res.id}"
        )
        db.add(db_doc)
        
        # Prepare for Vector Store
        docs_to_embed.append(doc_content)
        metadatas.append({
            "source": "Official Resource List",
            "title": res.name,
            "url": res.url,
            "category": res.category
        })
        ids.append(f"res_{res.id}")
        
    db.commit()
    
    # 2. Embed and Index in Chroma
    try:
        collection = get_collection()
        # Clean existing?
        # collection.delete(where={"source": "Official Resource List"}) 
        # Actually seed_data drops tables, but Chroma is persistent on disk.
        # We should probably reset Chroma or at least overwrite.
        
        if docs_to_embed:
            logger.info("Generating embeddings...")
            embeddings = embed_text(docs_to_embed)
            
            logger.info("Adding to ChromaDB...")
            collection.upsert(
                ids=ids,
                documents=docs_to_embed,
                embeddings=embeddings,
                metadatas=metadatas
            )
            logger.info(f"Indexed {len(docs_to_embed)} documents in Vector Store")
            
    except Exception as e:
        logger.error(f"Failed to seed Vector Store: {e}")


def seed_police_stations(db):
    raw_data = [
      {
        "id": 1,
        "city": "Agartala",
        "state": "Tripura",
        "office_name": "Cyber Crime Police Station",
        "officer": "Shri Ajit Pratap Singh, IPS",
        "designation": "Superintendent of Police (Cyber Crime)",
        "address": "Tripura Police Crime Branch, Police Headquarters, Fire Brigade Chowmuhani, Agartala - 799001",
        "email": "spcybercrime@tripurapolice.nic.in",
        "mobile": "9436123743",
        "telephone": "0381-2304346",
        "fax": None
      },
      {
        "id": 2,
        "city": "Gandhinagar",
        "state": "Gujarat",
        "office_name": "State Cyber Crime Cell",
        "officer": "Shri Dharmendra Sharma, IPS",
        "designation": "Superintendent of Police",
        "address": "7th Floor, Karmyogi Bhavan, Sector-10A, Block-2, Gandhinagar - 382018",
        "email": "cc-cid@gujarat.gov.in",
        "mobile": "9978408719",
        "telephone": "079-23250798",
        "fax": None
      },
      {
        "id": 3,
        "city": "Itanagar",
        "state": "Arunachal Pradesh",
        "office_name": "Police Headquarters",
        "officer": None,
        "designation": "Inspector General of Police (L&O/Crime)",
        "address": "Police Headquarters, Government of Arunachal Pradesh, Itanagar - 791113",
        "email": "arpolice@rediffmail.com, crbarunpol@gmail.com",
        "mobile": "9436040704",
        "telephone": "0360-2212734",
        "fax": "0360-2212735"
      },
      {
        "id": 4,
        "city": "Bengaluru",
        "state": "Karnataka",
        "office_name": "Office of DGP & IGP",
        "officer": None,
        "designation": "Assistant Inspector General of Police",
        "address": "Nrupathunga Road, Bengaluru - 560001",
        "email": None,
        "mobile": "112",
        "telephone": "080-22942349",
        "fax": "080-22942360"
      },
      {
        "id": 5,
        "city": "Navi Mumbai",
        "state": "Maharashtra",
        "office_name": "Cyber Branch",
        "officer": None,
        "designation": None,
        "address": "Sector 10, Opp RBI, CBD Belapur, Navi Mumbai - 400614",
        "email": "cybercell.navimumbai@mahapolice.gov.in",
        "mobile": None,
        "telephone": "022-27578309",
        "fax": None
      },
      {
        "id": 6,
        "city": "Bhopal",
        "state": "Madhya Pradesh",
        "office_name": "State Cyber Police",
        "officer": None,
        "designation": None,
        "address": "Police Radio Headquarters, Bhadbhada Road, Bhopal",
        "email": "mpcyberpolice@gmail.com",
        "mobile": None,
        "telephone": "0755-2770278",
        "fax": None
      },
      {
        "id": 7,
        "city": "Cuttack",
        "state": "Odisha",
        "office_name": "Crime Branch CID",
        "officer": None,
        "designation": "Additional Director General of Police",
        "address": "P.O. Buxi Bazaar, Cuttack - 753001",
        "email": "adgcidcb.orpol@nic.in",
        "mobile": None,
        "telephone": "0671-2304834",
        "fax": "0671-2304659"
      },
      {
        "id": 8,
        "city": "Cuttack",
        "state": "Odisha",
        "office_name": "Cyber Crime Police Station",
        "officer": None,
        "designation": None,
        "address": "CID, Crime Branch, Odisha, Cuttack",
        "email": "cid-cyberpetition@gov.in",
        "mobile": None,
        "telephone": "0671-2305485",
        "fax": "0671-2305961"
      },
      {
        "id": 9,
        "city": "Bhubaneswar",
        "state": "Odisha",
        "office_name": "Economic Offences Wing",
        "officer": None,
        "designation": None,
        "address": "Plot No 141, Keshari Nagar, Unit-5, Bhubaneswar - 751014",
        "email": "digpeow.odpol@nic.in, speowcidcb.odpol@nic.in",
        "mobile": None,
        "telephone": "0671-2394727",
        "fax": "0674-2394129"
      },
      {
        "id": 10,
        "city": "Chandigarh",
        "state": "Chandigarh",
        "office_name": "Economic Offences Wing",
        "officer": None,
        "designation": None,
        "address": "Home Guard Building, Sector-17, Chandigarh",
        "email": "pdspeow-chd@nic.in",
        "mobile": None,
        "telephone": "0172-2724402",
        "fax": None
      },
      {
        "id": 11,
        "city": "Chennai",
        "state": "Tamil Nadu",
        "office_name": "Economic Offences Wing",
        "officer": "Smt. Meena",
        "designation": "Superintendent of Police",
        "address": "SIDCO Industrial Estate, Guindy, Chennai - 600032",
        "email": "speowunit@gmail.com",
        "mobile": None,
        "telephone": "044-22501312",
        "fax": "044-22501311"
      },
      {
        "id": 12,
        "city": "Puducherry",
        "state": "Puducherry",
        "office_name": "Crime Branch CID",
        "officer": "Shri S. Venkatasamy",
        "designation": "Superintendent of Police",
        "address": "Dumas Street, Pondicherry - 605001",
        "email": "spcid.pon@nic.in",
        "mobile": "9489205010",
        "telephone": "0413-2224061",
        "fax": None
      },
      {
        "id": 13,
        "city": "Dehradun",
        "state": "Uttarakhand",
        "office_name": "Special Task Force",
        "officer": None,
        "designation": "Senior Superintendent of Police",
        "address": "Near Fire Station, Gandhi Road, Dehradun - 248001",
        "email": None,
        "mobile": "8859778859",
        "telephone": "0135-2651689",
        "fax": None
      },
      {
        "id": 14,
        "city": "Gangtok",
        "state": "Sikkim",
        "office_name": "Criminal Investigation Department",
        "officer": None,
        "designation": "Superintendent of Police",
        "address": "Sikkim Police Headquarters, Gangtok - 737101",
        "email": "spcid@sikkimpolice.nic.in",
        "mobile": "7547965002",
        "telephone": "03592-202087",
        "fax": None
      },
      {
        "id": 15,
        "city": "Guwahati",
        "state": "Assam",
        "office_name": "Bureau of Investigation & Economic Offences",
        "officer": None,
        "designation": "Additional Director General of Police",
        "address": "Srimantapur, Bhangagarh, Guwahati - 781032",
        "email": None,
        "mobile": None,
        "telephone": "0361-2468515",
        "fax": None
      },
      {
        "id": 16,
        "city": "Chandigarh",
        "state": "Haryana",
        "office_name": "Crime Branch",
        "officer": None,
        "designation": "Deputy Inspector General of Police",
        "address": "Haryana Police",
        "email": "adgp.crime@hry.nic.in, police@hry.nic.in",
        "mobile": None,
        "telephone": "0172-2587529",
        "fax": None
      },
      {
        "id": 17,
        "city": "Hyderabad",
        "state": "Telangana",
        "office_name": "CID Economic Offences Wing",
        "officer": None,
        "designation": "Superintendent of Police",
        "address": "DGP Office Complex, Lakdikapool, Hyderabad - 500004",
        "email": "addldgp-cid@tspolice.gov.in",
        "mobile": "9440627693",
        "telephone": "040-23242424",
        "fax": None
      },
      {
        "id": 18,
        "city": "Guntur",
        "state": "Andhra Pradesh",
        "office_name": "Economic Offences Wing",
        "officer": None,
        "designation": "Additional Superintendent of Police",
        "address": "AP DGP Headquarters, Mangalagiri, Guntur - 522503",
        "email": "adgcid@ap.gov.in",
        "mobile": "9440700856",
        "telephone": "0863-2340559",
        "fax": None
      },
  {
    "id": 19,
    "city": "Jaipur",
    "state": "Rajasthan",
    "office_name": "ATS & SOG",
    "officer": "Shri Ashok Kumar Rathore",
    "designation": "ADGP",
    "address": "In front of Wireless Police Lines, Ghat Gate, Agra Road, Jaipur",
    "email": null,
    "mobile": null,
    "telephone": "0141-2600123",
    "fax": null
  },
  {
    "id": 20,
    "city": "Jaipur",
    "state": "Rajasthan",
    "office_name": "CID Crime Branch",
    "officer": "Shri Vijay Kumar Singh",
    "designation": "IGP",
    "address": "Police Headquarters, Lal Kothi, Jaipur",
    "email": null,
    "mobile": null,
    "telephone": "0141-2740580",
    "fax": null
  },
  {
    "id": 21,
    "city": "Jammu",
    "state": "Jammu & Kashmir",
    "office_name": "Crime Branch",
    "officer": null,
    "designation": "SSP Crime",
    "address": "CPO Complex, Panjtirthi, Jammu - 180001",
    "email": "sspcrimejmu@jkpolice.gov.in",
    "mobile": null,
    "telephone": "0191-2578901",
    "fax": null
  },
  {
    "id": 22,
    "city": "Srinagar",
    "state": "Jammu & Kashmir",
    "office_name": "Crime Branch Kashmir",
    "officer": null,
    "designation": null,
    "address": "Exhibition Ground, Opp Civil Secretariat, Srinagar - 190001",
    "email": "cbkmr@jkpolice.gov.in",
    "mobile": null,
    "telephone": "0194-2471828",
    "fax": null
  },
  {
    "id": 23,
    "city": "Jammu",
    "state": "Jammu & Kashmir",
    "office_name": "Crime Branch Headquarters",
    "officer": null,
    "designation": null,
    "address": "CPO Complex, Panjtirthi, Jammu - 180001",
    "email": "crimehqrs@jkpolce.gov.in",
    "mobile": null,
    "telephone": "0191-2572475",
    "fax": null
  },
  {
    "id": 24,
    "city": "Lucknow",
    "state": "Uttar Pradesh",
    "office_name": "Cyber Crime Cell",
    "officer": null,
    "designation": null,
    "address": "Signature Building, Tower 4, 5th Floor, Gomti Nagar Extension, Lucknow - 226002",
    "email": "sp-cyber.lu@up.gov.in, asp-cyber.lu@up.gov.in",
    "mobile": "9454400581",
    "telephone": "0522-2390538",
    "fax": null
  },
  {
    "id": 25,
    "city": "Lucknow",
    "state": "Uttar Pradesh",
    "office_name": "Economic Offences Wing",
    "officer": null,
    "designation": null,
    "address": "Police Bhawan, Gomti Nagar Vistar, Lucknow - 226002",
    "email": "eowhq@up.nic.in",
    "mobile": "9454401150",
    "telephone": "0522-2724424",
    "fax": null
  },
  {
    "id": 26,
    "city": "Kolkata",
    "state": "West Bengal",
    "office_name": "Kolkata Police Cyber Crime",
    "officer": null,
    "designation": "Commissioner of Police",
    "address": "Lalbazar, Kolkata - 700001",
    "email": "dccyber@kolkatapolice.gov.in",
    "mobile": null,
    "telephone": "033-22505427",
    "fax": null
  },
  {
    "id": 27,
    "city": "Kolkata",
    "state": "West Bengal",
    "office_name": "CID West Bengal",
    "officer": null,
    "designation": "Additional Director General of Police",
    "address": "31, Belvedere Road, Alipore, Kolkata - 700027",
    "email": "wbadgcidoffice@gmail.com, occyber@cidwestbengal.gov.in",
    "mobile": null,
    "telephone": "033-24506100",
    "fax": "033-24506174"
  },
  {
    "id": 28,
    "city": "Imphal",
    "state": "Manipur",
    "office_name": "Crime Branch / EOW",
    "officer": null,
    "designation": "Superintendent of Police",
    "address": "Government of Manipur, Imphal - 795001",
    "email": null,
    "mobile": "9436082905",
    "telephone": null,
    "fax": null
  },
  {
    "id": 29,
    "city": "Shillong",
    "state": "Meghalaya",
    "office_name": "CID Meghalaya",
    "officer": null,
    "designation": "Deputy Inspector General",
    "address": "CID Office, Shillong",
    "email": "dig.cid-meg@gov.in",
    "mobile": "9485113997",
    "telephone": "0364-2215622",
    "fax": null
  },
  {
    "id": 30,
    "city": "Aizawl",
    "state": "Mizoram",
    "office_name": "CID Crime",
    "officer": null,
    "designation": "Superintendent of Police",
    "address": "CID Complex, Aizawl - 796001",
    "email": "spcidcr-mz@nic.in, cidcrime-mz@nic.in",
    "mobile": null,
    "telephone": "0389-2334082",
    "fax": "0389-2333364"
  },
  {
    "id": 31,
    "city": "Mumbai",
    "state": "Maharashtra",
    "office_name": "Cyber Crime Maharashtra",
    "officer": null,
    "designation": null,
    "address": "World Trade Centre, Centre-I, 32nd Floor, Cuffe Parade, Mumbai - 400005",
    "email": "control.cpaw-mah@gov.in",
    "mobile": null,
    "telephone": "022-22160080",
    "fax": "022-22160084"
  },
  {
    "id": 32,
    "city": "Mumbai",
    "state": "Maharashtra",
    "office_name": "Economic Offences Wing",
    "officer": null,
    "designation": null,
    "address": "World Trade Centre, Centre-I, 18th Floor, Cuffe Parade, Mumbai - 400005",
    "email": "adg.eowms@mahapolice.gov.in",
    "mobile": null,
    "telephone": "022-26504008",
    "fax": null
  },
  {
    "id": 33,
    "city": "Kohima",
    "state": "Nagaland",
    "office_name": "Police Headquarters",
    "officer": null,
    "designation": "Additional Director General of Police",
    "address": "Government of Nagaland, Kohima - 797001",
    "email": "adgpadm-ngl@nic.in",
    "mobile": "9436009007",
    "telephone": "0370-2242891",
    "fax": null
  },
  {
    "id": 34,
    "city": "Nagpur",
    "state": "Maharashtra",
    "office_name": "Cyber Police Station",
    "officer": null,
    "designation": null,
    "address": "Administrative Building No.1, Civil Lines, Nagpur",
    "email": "cybercrimecell.ngp@gmail.com",
    "mobile": null,
    "telephone": "0712-2566766",
    "fax": null
  },
  {
    "id": 35,
    "city": "New Delhi",
    "state": "Delhi",
    "office_name": "Economic Offences Wing",
    "officer": null,
    "designation": "Special Commissioner of Police",
    "address": "PS Mandir Marg Complex, New Delhi - 110001",
    "email": "addlcp.eow@delhipolice.gov.in, jtcp.eow@delhipolice.gov.in",
    "mobile": null,
    "telephone": "011-23740599",
    "fax": null
  },
  {
    "id": 36,
    "city": "New Delhi",
    "state": "Delhi",
    "office_name": "Cyber Crime Cell",
    "officer": null,
    "designation": "Deputy Commissioner of Police",
    "address": "Room No. 206, PS Mandir Marg, New Delhi - 110001",
    "email": "dcp-newdelhi-dl@nic.in",
    "mobile": null,
    "telephone": "011-23746694",
    "fax": null
  },
  {
    "id": 37,
    "city": "Panaji",
    "state": "Goa",
    "office_name": "Cyber Crime Police Station",
    "officer": "Prashal Naik Dessai",
    "designation": "Police Inspector",
    "address": "Panaji, Goa",
    "email": "picyber@goapolice.gov.in",
    "mobile": "7875756183",
    "telephone": "0832-2443201",
    "fax": null
  },
  {
    "id": 38,
    "city": "Panaji",
    "state": "Goa",
    "office_name": "Economic Offences Cell",
    "officer": null,
    "designation": null,
    "address": "Altinho, Panaji, Goa - 403001",
    "email": "pieoc@goapolice.gov.in, speoc@goapolice.gov.in",
    "mobile": "7875756082",
    "telephone": "0832-2443082",
    "fax": null
  },
  {
    "id": 39,
    "city": "Patna",
    "state": "Bihar",
    "office_name": "Economic Offences Wing",
    "officer": null,
    "designation": "Additional Director General",
    "address": "Rajbhawan Marg, Patna - 800001",
    "email": "igecooffence-bih@nic.in",
    "mobile": null,
    "telephone": "0612-2217829",
    "fax": null
  },
  {
    "id": 40,
    "city": "Raipur",
    "state": "Chhattisgarh",
    "office_name": "CID Police Headquarters",
    "officer": null,
    "designation": "Additional Director General of Police",
    "address": "Sector 19, Naya Raipur - 492002",
    "email": null,
    "mobile": "9479190444",
    "telephone": "0771-2285150",
    "fax": null
  },
  {
    "id": 41,
    "city": "Raipur",
    "state": "Chhattisgarh",
    "office_name": "Anti Corruption Bureau / EOW",
    "officer": null,
    "designation": null,
    "address": "GE Road, Raipur - 492001",
    "email": null,
    "mobile": null,
    "telephone": "0771-2285002",
    "fax": null
  },
  {
    "id": 42,
    "city": "Raipur",
    "state": "Chhattisgarh",
    "office_name": "Cyber Cell",
    "officer": null,
    "designation": "Additional Inspector General",
    "address": "Police Headquarters, Sector 19, Naya Raipur - 492002",
    "email": null,
    "mobile": "9479191493",
    "telephone": "0771-2331920",
    "fax": null
  },
  {
    "id": 43,
    "city": "Ranchi",
    "state": "Jharkhand",
    "office_name": "CID Jharkhand",
    "officer": "Prashant Singh",
    "designation": "Additional Director General",
    "address": "Raja Rani Building, Doranda, Ranchi - 834002",
    "email": null,
    "mobile": "9771432100",
    "telephone": "0651-2490546",
    "fax": "0651-2490295"
  },
  {
    "id": 44,
    "city": "Thiruvananthapuram",
    "state": "Kerala",
    "office_name": "Economic Offences",
    "officer": null,
    "designation": "Additional Director General of Police (Crime)",
    "address": "Police Headquarters, Vazhuthacaud, Thiruvananthapuram - 695010",
    "email": "adgpcrimes@keralapolice.gov.in",
    "mobile": null,
    "telephone": "0471-2722215",
    "fax": null
  },
  {
    "id": 45,
    "city": "Thiruvananthapuram",
    "state": "Kerala",
    "office_name": "Cyber Crime SCRB",
    "officer": null,
    "designation": "Additional Director General of Police",
    "address": "Police Headquarters, Vazhuthacaud, Thiruvananthapuram - 695010",
    "email": "adgpscrb.pol@kerala.gov.in",
    "mobile": null,
    "telephone": "0471-2726521",
    "fax": null
  },
  {
    "id": 46,
    "city":"Coimbatore",
    "state":"Tamil Nadu",
    "office_name":"Cyber Crime Department",
    "officer":null,
    "designation":null,
    "address":"Near Collectorate Office & DSP Office Bus Stop, Hosur Road, Coimbatore Central, Coimbatore-641018",
    "email":"cop.cbe@tncctns.gov.in",
    "mobile":null,
    "telephone":"0422 239 9100",
    "fax":null
  }

]



    count = 0
    for item in raw_data:
        # Map fields to match model
        phone = item.get("telephone") or item.get("mobile")
        if item.get("mobile") and item.get("telephone"):
            phone = f"{item['telephone']} / {item['mobile']}"
            
        st = {
            "name": item["office_name"],
            "city": item["city"],
            "state": item["state"],
            "district": item["city"], # Default to city as district
            "address": item["address"],
            "email": item["email"],
            "phone": phone,
            "officer": item["officer"],
            "designation": item["designation"],
            "is_cyber_cell": True
        }
        
        # Check if exists by name AND state (to update or skip)
        existing = db.query(PoliceStation).filter(PoliceStation.address == st["address"]).first()
        if not existing:
            db.add(PoliceStation(**st))
            count += 1
    
    db.commit()
    logger.info(f"Seeded {count} real police stations")

def main():
    print("Seed script starting...")
    from app.db import Base, engine
    
    # DROP ALL TABLES TO UPDATE SCHEMA with new columns
    print("Dropping all tables to apply new schema...")
    Base.metadata.drop_all(bind=engine)
    
    init_db()  
    db = SessionLocal()
    try:
        seed_resources(db)
        seed_documents(db)
        seed_police_stations(db)
        print("Data seeding completed successfully.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Seeding failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()

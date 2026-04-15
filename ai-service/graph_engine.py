import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "network_knowledge.json")

def check_network_risk(promoter_name, company_name, location):
    """
    Scans the knowledge base for suspicious cross-company links.
    """
    try:
        if not os.path.exists(KNOWLEDGE_FILE):
            return {"network_flags": [], "network_penalty": 0, "has_graph_risk": False}

        with open(KNOWLEDGE_FILE, 'r') as f:
            data = json.load(f)
            
        flags = []
        network_penalty = 0
        
        # 1. Check Directors for past defaults
        for director in data.get("suspicious_directors", []):
            if promoter_name and promoter_name.lower() in director["name"].lower():
                flags.append(f"Director Conflict: {promoter_name} found in Forensic Watchlist ({director['risk_category']})")
                flags.append(f"Interconnected Entities: {', '.join(director['associated_entities'])}")
                network_penalty += 25
                
        # 2. Check Adresses for Shell Hubs
        for addr in data.get("associated_addresses", []):
            if location and location.lower() in addr["address"].lower():
                flags.append(f"Address Alert: Registered office '{location}' matches known {addr['flag']}")
                if addr.get("risk_level") == "High":
                    network_penalty += 15
                else:
                    network_penalty += 5
                    
        return {
            "network_flags": flags,
            "network_penalty": -network_penalty,
            "has_graph_risk": len(flags) > 0
        }
    except Exception as e:
        print(f"Graph Engine Header Error: {e}")
        return {"network_flags": [], "network_penalty": 0, "has_graph_risk": False}

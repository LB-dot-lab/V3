import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Protocol:
    """Enhanced protocol dataclass with detailed information"""
    title: str
    description: str
    timing: str
    category: str
    evidence: str
    difficulty: str
    instructions: List[str] = None
    benefits: List[str] = None

class ProtocolLoader:
    """Loads and manages protocols from JSON database"""
    
    def __init__(self, protocols_path: str = "data/protocols.json"):
        self.protocols_path = protocols_path
        self.protocols_db = self._load_protocols()
    
    def _load_protocols(self) -> Dict:
        """Load protocols from JSON file"""
        try:
            if os.path.exists(self.protocols_path):
                with open(self.protocols_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Return default protocols if file doesn't exist
                return self._get_default_protocols()
        except Exception as e:
            print(f"Error loading protocols: {e}")
            return self._get_default_protocols()
    
    def _get_default_protocols(self) -> Dict:
        """Fallback protocols if JSON file is unavailable"""
        return {
            "cortisol_imbalance": [
                {
                    "title": "Morning Light Exposure",
                    "description": "Go outside barefoot for 10 minutes at sunrise",
                    "timing": "6:00-7:00 AM",
                    "category": "Circadian",
                    "evidence": "Regulates cortisol rhythm and vitamin D",
                    "difficulty": "Easy",
                    "instructions": ["Step outside within 30 minutes of sunrise", "Remove shoes if weather permits"],
                    "benefits": ["Sets circadian clock", "Boosts vitamin D"]
                }
            ],
            "mineral_depletion": [
                {
                    "title": "Magnesium Glycinate",
                    "description": "200-400mg magnesium glycinate before bed",
                    "timing": "9:00 PM",
                    "category": "Minerals",
                    "evidence": "Essential for 300+ enzymatic processes",
                    "difficulty": "Easy",
                    "instructions": ["Choose glycinate form", "Start with 200mg"],
                    "benefits": ["Improves sleep", "Reduces tension"]
                }
            ]
        }
    
    def get_protocols_for_causes(self, root_causes: List[str], max_per_cause: int = 3) -> List[Protocol]:
        """Get protocols for specific root causes"""
        selected_protocols = []
        
        for cause in root_causes:
            if cause in self.protocols_db:
                protocols_data = self.protocols_db[cause][:max_per_cause]
                for protocol_data in protocols_data:
                    protocol = Protocol(
                        title=protocol_data.get('title', ''),
                        description=protocol_data.get('description', ''),
                        timing=protocol_data.get('timing', ''),
                        category=protocol_data.get('category', ''),
                        evidence=protocol_data.get('evidence', ''),
                        difficulty=protocol_data.get('difficulty', 'Medium'),
                        instructions=protocol_data.get('instructions', []),
                        benefits=protocol_data.get('benefits', [])
                    )
                    selected_protocols.append(protocol)
        
        # Remove duplicates based on title
        unique_protocols = []
        seen_titles = set()
        for protocol in selected_protocols:
            if protocol.title not in seen_titles:
                unique_protocols.append(protocol)
                seen_titles.add(protocol.title)
        
        return unique_protocols[:8]  # Limit to 8 total protocols
    
    def get_protocol_by_title(self, title: str) -> Optional[Protocol]:
        """Get a specific protocol by title"""
        for cause_protocols in self.protocols_db.values():
            for protocol_data in cause_protocols:
                if protocol_data.get('title') == title:
                    return Protocol(
                        title=protocol_data.get('title', ''),
                        description=protocol_data.get('description', ''),
                        timing=protocol_data.get('timing', ''),
                        category=protocol_data.get('category', ''),
                        evidence=protocol_data.get('evidence', ''),
                        difficulty=protocol_data.get('difficulty', 'Medium'),
                        instructions=protocol_data.get('instructions', []),
                        benefits=protocol_data.get('benefits', [])
                    )
        return None
    
    def get_protocols_by_category(self, category: str) -> List[Protocol]:
        """Get all protocols in a specific category"""
        protocols = []
        for cause_protocols in self.protocols_db.values():
            for protocol_data in cause_protocols:
                if protocol_data.get('category', '').lower() == category.lower():
                    protocol = Protocol(
                        title=protocol_data.get('title', ''),
                        description=protocol_data.get('description', ''),
                        timing=protocol_data.get('timing', ''),
                        category=protocol_data.get('category', ''),
                        evidence=protocol_data.get('evidence', ''),
                        difficulty=protocol_data.get('difficulty', 'Medium'),
                        instructions=protocol_data.get('instructions', []),
                        benefits=protocol_data.get('benefits', [])
                    )
                    protocols.append(protocol)
        return protocols
    
    def get_all_categories(self) -> List[str]:
        """Get list of all available categories"""
        categories = set()
        for cause_protocols in self.protocols_db.values():
            for protocol_data in cause_protocols:
                categories.add(protocol_data.get('category', 'Other'))
        return sorted(list(categories))
    
    def get_protocols_by_difficulty(self, difficulty: str) -> List[Protocol]:
        """Get protocols filtered by difficulty level"""
        protocols = []
        for cause_protocols in self.protocols_db.values():
            for protocol_data in cause_protocols:
                if protocol_data.get('difficulty', '').lower() == difficulty.lower():
                    protocol = Protocol(
                        title=protocol_data.get('title', ''),
                        description=protocol_data.get('description', ''),
                        timing=protocol_data.get('timing', ''),
                        category=protocol_data.get('category', ''),
                        evidence=protocol_data.get('evidence', ''),
                        difficulty=protocol_data.get('difficulty', 'Medium'),
                        instructions=protocol_data.get('instructions', []),
                        benefits=protocol_data.get('benefits', [])
                    )
                    protocols.append(protocol)
        return protocols
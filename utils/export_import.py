"""Export/Import utilities stub for testing"""
import json
from datetime import datetime

class ExportImport:
    def __init__(self):
        pass
    
    def export_to_json(self, events):
        """Export events to JSON"""
        data = []
        for event in events:
            e = dict(event)
            if isinstance(e.get('start_time'), datetime):
                e['start_time'] = e['start_time'].isoformat()
            if isinstance(e.get('end_time'), datetime):
                e['end_time'] = e['end_time'].isoformat()
            data.append(e)
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def export_to_ics(self, events):
        """Export events to ICS format"""
        return "BEGIN:VCALENDAR\nVERSION:2.0\nEND:VCALENDAR"
    
    def import_from_json(self, json_content):
        """Import events from JSON"""
        data = json.loads(json_content)
        events = []
        for e in data:
            if isinstance(e.get('start_time'), str):
                e['start_time'] = datetime.fromisoformat(e['start_time'])
            if isinstance(e.get('end_time'), str):
                e['end_time'] = datetime.fromisoformat(e['end_time'])
            events.append(e)
        return events

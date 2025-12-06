"""Database manager stub for testing"""
from datetime import datetime
import json
import os

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.events = []
        self.next_id = 1
        
    def add_event(self, event_data):
        """Add an event to the database"""
        event_id = self.next_id
        self.next_id += 1
        
        event = {
            'id': event_id,
            'event_name': event_data['event_name'],
            'start_time': event_data['start_time'],
            'end_time': event_data.get('end_time'),
            'location': event_data.get('location'),
            'reminder_minutes': event_data.get('reminder_minutes'),
            'description': event_data.get('description')
        }
        
        self.events.append(event)
        return event_id
    
    def get_events(self, start, end):
        """Get events within a time range"""
        return [e for e in self.events if start <= e['start_time'] < end]
    
    def get_all_events(self):
        """Get all events"""
        return self.events
    
    def search_events(self, keyword):
        """Search events by keyword"""
        keyword = keyword.lower()
        return [e for e in self.events 
                if keyword in e['event_name'].lower() 
                or (e.get('location') and keyword in e['location'].lower())
                or (e.get('description') and keyword in e['description'].lower())]
    
    def delete_event(self, event_id):
        """Delete an event"""
        self.events = [e for e in self.events if e['id'] != event_id]
        return True
    
    def clear_all_events(self):
        """Clear all events"""
        self.events = []
    
    def import_events(self, events):
        """Import events"""
        success = 0
        errors = 0
        for event in events:
            try:
                self.add_event(event)
                success += 1
            except:
                errors += 1
        return success, errors

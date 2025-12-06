"""Reminder system stub for testing"""

class ReminderSystem:
    def __init__(self, db_manager):
        self.db = db_manager
        self.running = False
    
    def start(self):
        """Start the reminder system"""
        self.running = True
    
    def stop(self):
        """Stop the reminder system"""
        self.running = False
    
    def get_status(self):
        """Get system status"""
        return {'running': self.running}

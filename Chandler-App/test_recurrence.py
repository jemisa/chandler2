import unittest
from datetime import datetime, timedelta
from chandler.core import Item
from chandler.recurrence import *
from chandler.event import Event
from chandler.time_services import TimeZone, setNow

class RecurrenceTestCase(unittest.TestCase):

    def setUp(self):
        self.item = Item()
        self.dtstart = datetime(2008, 11, 30, 9, tzinfo=TimeZone.pacific)
        setNow(self.dtstart + timedelta(days=1))
        self.event = Event(self.item).add(base_start=self.dtstart)
        self.recurrence = Recurrence(self.item).add()

    def test_dashboard_entry_count(self):
        """Recurrence entries appear and go away if recurrence is removed."""
        self.assertEqual(1, len(self.item.dashboard_entries))
        self.recurrence.frequency = 'weekly'
        self.assertEqual(2, len(self.item.dashboard_entries))
        self.assertEqual(2, len(self.recurrence._recurrence_dashboard_entries))
        self.recurrence.remove()
        self.assertEqual(1, len(self.item.dashboard_entries))

if __name__ == "__main__":
    unittest.main()

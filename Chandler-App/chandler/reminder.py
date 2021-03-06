import peak.events.trellis as trellis
from chandler.core import ConstraintError, ItemAddOn
from chandler.event import Event
from chandler.triage import *
from chandler.time_services import timestamp


### Domain model ###

class ReminderList(ItemAddOn):
    reminders = trellis.make(trellis.List)

    def add_reminder(self, **kwargs):
        reminder = Reminder(item=self._item, **kwargs)
        self.reminders.append(reminder)
        return reminder

    def remove_all_reminders(self):
        self.reminders[:] = []

class Reminder(trellis.Component):
    trellis.attrs(
        item=None,
        delta=None,
        fixed_trigger=None,
        description="",
        snooze=None,
        cleared=False,
        type='triage',
    )

    @trellis.compute
    def trigger(self):
        if self.fixed_trigger is not None:
            return self.fixed_trigger
        elif self.delta is not None and self.item is not None:
            if Event.installed_on(self.item):
                start = Event(self.item).start
                if start is not None:
                    return start + self.delta

def reminder_triage(item):
    got_trigger = False
    for reminder in ReminderList(item).reminders:
        if reminder.trigger is not None:
            got_trigger = True
            yield (timestamp(reminder.trigger), NOW)
    if got_trigger:
        yield (0, LATER)

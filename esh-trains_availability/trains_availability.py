from collections import defaultdict


def min_trains(schedule):
    # Parse and sort events by time
    events = []
    for time, (event_type, station) in schedule.items():
        events.append((time, event_type, station))

    # Sort events by time, prioritizing "arrive" over "leave" for the same time
    events.sort(key=lambda x: (x[0], x[1] == 'leave'))

    # Initialize train usage and minimal trains count
    trains_available = defaultdict(int)  # Trains currently available at each station
    trains_needed = defaultdict(int)  # Minimal trains needed at each station

    # Process each event
    for time, event_type, station in events:
        if event_type == 'leave':
            # Use a train from the station
            if trains_available[station] > 0:
                trains_available[station] -= 1
            else:
                # If no trains available, add a new train
                trains_needed[station] += 1
        elif event_type == 'arrive':
            # A train becomes available at the station
            trains_available[station] += 1

    return dict(trains_needed)


# Example usage
schedule = {
    '08:00': ['leave', 1],
    '08:30': ['arrive', 2],
    '08:20': ['leave', 2],
    '09:30': ['arrive', 1],
    '10:00': ['leave', 1],
    '10:15': ['arrive', 2],
    '10:30': ['leave', 2],
    '11:00': ['arrive', 1],
    '11:30': ['leave', 1],
    '19:00': ['arrive', 2],
    '11:55': ['leave', 2],
    '13:00': ['arrive', 1],
    '13:30': ['leave', 1],
    '14:00': ['arrive', 2],
    '14:30': ['leave', 2],
    '15:00': ['arrive', 1],
}

print(min_trains(schedule))

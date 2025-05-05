def checkContact(userA, userB):
    # Get the location history for both users
    # user_location_history -> not defined but is a hashmap of user IDs to their
    # list of time stamped and locations
    user_A_locations = user_location_history[userA]
    user_B_locations = user_location_history[userB]

    for user_A in user_A_locations:
        for user_B in user_B_locations:
            # Checks if the timestamps overlap within 15 minutes
            if abs(user_A.timestamp - user_B.timestamp) <= 15_MINUTES:
                # Check if locations are within 6 feet of each other
                if distance(user_A.coordinates, user_B.coordinates) <= 6_FEET:
                    # Time window overlap check
                    time_overlap = calculate_time_overlap(user_A_locations, user_B_locations)
                    if time_overlap >= 15_MINUTES:
                        return True  # Contact has been detected
    return False # No contact has been detected
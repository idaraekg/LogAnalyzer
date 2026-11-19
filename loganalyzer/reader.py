from loganalyzer.models import LogEntry
from datetime import datetime


class LogReader:
    def __init__(self):
        # Count invalid log lines
        self.malformed_count = 0

    def read_log_file(self, file_path):
        # Reset the counter each time we read the file
        self.malformed_count = 0

        # Open the log file in read mode
        with open(file_path, 'r') as file:
            # Read the file one line at a time
            for line in file:

                # Separate the date, time, level, and message
                parts = line.strip().split(' ', 3)

                # Check if the line has four parts
                if len(parts) == 4:
                    date, time, level, message = parts

                    # Skip invalid severity levels
                    if level not in ("DEBUG", "INFO", "WARNING", "ERROR"):
                        self.malformed_count += 1
                        continue

                    # Combine date and time
                    timestamp = date + " " + time

                    # Check if the timestamp is valid
                    try:
                        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        self.malformed_count += 1
                        continue

                    # Skip empty messages
                    if not message.strip():
                        self.malformed_count += 1
                        continue

                    # Create a LogEntry object
                    log_entry = LogEntry(timestamp, level, message)

                    # Return one valid entry at a time
                    yield log_entry

                else:
                    # Count lines with missing information
                    self.malformed_count += 1


def filter_by_level(entries, level):
    # Go through each log entry
    for entry in entries:

        # Check if the entry matches the requested level
        if entry.level == level:

            # Give back the matching entry
            yield entry


class BatchIterator:
    def __init__(self, entries, batch_size):
        # Make sure the batch size is valid
        if type(batch_size) is not int or batch_size <= 0:
            raise ValueError("Batch size must be a positive integer")

        # Turn entries into an iterator
        self.entries = iter(entries)

        # Store the batch size
        self.batch_size = batch_size

    def __iter__(self):
        # Return the iterator itself
        return self

    def __next__(self):
        # Create an empty list for the next batch
        batch = []

        # Get entries until the batch is full
        for i in range(self.batch_size):
            try:
                entry = next(self.entries)
                batch.append(entry)
            except StopIteration:
                break

        # Stop when no entries remain
        if not batch:
            raise StopIteration

        # Return the batch
        return batch
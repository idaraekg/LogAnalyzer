from loganalyzer.reader import LogReader
from loganalyzer.reader import filter_by_level
from loganalyzer.reader import LogReader, filter_by_level, BatchIterator

# Create the reader
reader = LogReader()

# Count valid entries
valid_count = 0

# Read each log entry
for entry in reader.read_log_file("application.log"):
    valid_count += 1

# Display the results
print("Valid entries:", valid_count)
print("Malformed lines:", reader.malformed_count)

from loganalyzer.reader import filter_by_level

# Create a fresh reader for this test
reader = LogReader()

# Get only ERROR entries
error_entries = filter_by_level(
    reader.read_log_file("application.log"), "ERROR"
)

# Count the ERROR entries
error_count = sum(1 for entry in error_entries)

print("ERROR entries:", error_count)


# Test the batch iterator
reader = LogReader()

# Create batches containing up to 128 entries
batches = BatchIterator(reader.read_log_file("application.log"), 128)

batch_count = 0
last_batch_size = 0

# Go through each batch
for batch in batches:
    batch_count += 1
    last_batch_size = len(batch)

# Display the results
print("Total batches:", batch_count)
print("Final batch size:", last_batch_size)

# Test an invalid batch size
try:
    batches = BatchIterator([], 0)
    print("Invalid batch size was accepted")
except ValueError:
    print("Invalid batch size rejected")
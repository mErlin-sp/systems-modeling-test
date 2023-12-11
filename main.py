import ciw

N = ciw.create_network(
    arrival_distributions=[ciw.dists.Exponential(rate=3),
                           None,
                           None],
    service_distributions=[ciw.dists.Exponential(rate=5.0),
                           ciw.dists.Exponential(rate=10.0),
                           ciw.dists.Exponential(rate=15.0)],
    routing=[[0.0, 0.75, 0.25],
             [0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0]],
    queue_capacities=[0, 0, 2],
    number_of_servers=[2, 1, 1]
)

Q = ciw.Simulation(N)
Q.simulate_until_max_time(1000, progress_bar=True)

# Access the collected data
records = Q.get_all_records()

queue_lengths_node1 = []
queue_lengths_node2 = []
queue_lengths_node3 = []

service_time = []

failures = 0

# Calculate the mean queue length
for record in records:
    if record.record_type == 'rejection':
        failures += 1
    elif record.record_type == 'service':
        service_time.append(record.service_time)

    if record.node == 1:
        queue_lengths_node1.append(record.queue_size_at_arrival)
    elif record.node == 2:
        queue_lengths_node2.append(record.queue_size_at_arrival)
    elif record.node == 3:
        queue_lengths_node3.append(record.queue_size_at_arrival)

mean_queue_length_node1 = sum(queue_lengths_node1) / len(queue_lengths_node1)
mean_queue_length_node2 = sum(queue_lengths_node2) / len(queue_lengths_node2)
mean_queue_length_node3 = sum(queue_lengths_node3) / len(queue_lengths_node3)

mean_service_time = sum(service_time) / len(service_time)

print(f"Mean Queue Length on Node 1: {mean_queue_length_node1}")
print(f"Mean Queue Length on Node 2: {mean_queue_length_node2}")
print(f"Mean Queue Length on Node 3: {mean_queue_length_node3}")

print(f"Mean Service Time: {mean_service_time}")

print(f"Records processed: {len(records)}")
print("Failures count: ", failures)

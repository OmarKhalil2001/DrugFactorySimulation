## Project Header:
Consider a generic packaging line for some product, such as a pharmaceutical plant producing a
packaged medicinal product, or a food processing plant producing packaged foods or beverages. The
line consists of workstations that perform the processes of filling, capping, labeling, sealing, and
carton packing. Individual product units will be referred to simply as units. We make the following
assumptions:

1. The filling workstation always has material in front of it, so that it never starves.
2. The buffer space between workstations can hold at most five units.
3. A workstation gets blocked if there is no space in the immediate downstream buffer
(manufacturing blocking).
4. The processing times for filling, capping, labeling, sealing, and carton packing are 6.5, 5, 8, 5, and 6
seconds, respectively.

a. Develop a model for the packaging line and simulate it for a 100,000 seconds period.
b. Estimate the following statistics:
_ Throughput
_ Average inventory levels in buffers
_ Downtime probabilities
_ Blocking probabilities at bottleneck workstations
_ Average system flow times (also called manufacturing lead times)

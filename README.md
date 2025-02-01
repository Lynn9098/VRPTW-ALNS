# VRPTW-ALNS
用alns解一下VRPTW问题

Solve VRPTW with ALNS algorithm. Extensive computational experiment is all you need.

1. Visualization ✅ 
2. Initial Solution: ✅ 
   1. Solomon's Time-oriented Nearest Neighbor, in 1987 ✅
   2. Naive Construction: each customer with a route ✅
   3. Clark & Wright Saving Heuristic, 1964. ✅
3. ALNS Framework 💪

**Destroy Operator:**


> 1. Random Removal ✅
>
> 2. Worse Case Removal 🐌 ... 
>
> 3. Shaw Removal 🐌 ... 
>
> 4. String removal (See `Jan Christiaens, Greet Vanden Berghe (2020) Slack Induction by String Removals for Vehicle Routing Problems. Transportation Science`) 🐌 ... 
> Complete String removal, waiting for split removal procedure.

**Repair Operator:**

> 1. Greedy Insertion with Blink Mechanism ✅
>
> 2. Waiting ... 

4. Some SOTA heuristic like [PyVRP package](https://pyvrp.readthedocs.io/en/latest/).


-----

Some techniques embedded till now:

1. Forward Time Slack procedure for fast feasibility check during repair procedures. (See `Martin W. P. Savelsbergh, (1992) The Vehicle Routing Problem with Time Windows: Minimizing Route Duration. ORSA Journal on Computing 4(2):146-154. http://dx.doi.org/10.1287/ijoc.4.2.146`)
2. Blink Mechanism for Greedy Insertion. 
3. Basic framework.
4. Incorporate dataset.


# VRPTW-ALNS

This repo provides a ALNS meta-heuristic to solve VRPTW (Vehicle Routing Problem with Time Windows), which is NP-hard. We implement the SISRs (Slack Induction by String Removals) technique in `Jan Christiaens, Greet Vanden Berghe (2020) Slack Induction by String Removals for Vehicle Routing Problems. Transportation Science`, **which is proved to be a simple yet powerful heuristic for variants of VRP**. Experiments analysis can be found below.


## Numerical Experiments 

We provide a brief report of the numerical experiments. The results are obtained by running our code on Solomon benchmark instances. Column `Obj` indicates the objective value of our algorithm (which is measured by total distance), `#.T` shows the number of vehicles used in our solution, `CPU(s)` denotes the CPU time in seconds, `Gap BKS(%)` is the gap to the Best-Known Solution (BKS), `BKS #.T` is the number of vehicles used in the BKS, and `Note(#.T)` is the note, mainly the increase of vehicles compared with BKS. 

We may test our algorithm on more benchmarks in the future. As it's coded in pure Python, performance (running time) is somewhat terrible. We will try to fix that later. Analysis on running time verified a great time waste in destroy operators, with 0.07 s per action for 100 customer cases.

Total iteration Num is 20,000. The table display the best solution of 2-run.

|   Inst   |     Obj     | #.Truck  |  CPU (s)   | Gap to BKS | BKS #. Trucks | Note(#.T) |
| :------: | :---------: | :------: | :--------: | :--------: | :-----------: | --------- |
|   c101   |   854.35    |    10    |   129.9    |    3.06    |      10       | -         |
|   c102   |   828.94    |    10    |   379.21   |    0.0     |      10       | -         |
|   c103   |   828.94    |    10    |   326.32   |    0.11    |      10       | -         |
|   c104   |   850.58    |    10    |   365.68   |    3.13    |      10       | -         |
|   c105   |   878.36    |    10    |   90.62    |    5.96    |      10       | -         |
|   c106   |   852.95    |    10    |   228.3    |    2.9     |      10       | -         |
|   c107   |   1013.19   |    10    |   103.6    |   22.23    |      10       | -         |
|   c108   |   828.94    |    10    |   311.36   |    -0.0    |      10       | -         |
|   c109   |   828.94    |    10    |   329.69   |    0.0     |      10       | -         |
|   c201   |   591.56    |    3     |   110.14   |    0.0     |       3       | -         |
|   c202   |   620.29    |    3     |   218.05   |    4.86    |       3       | -         |
|   c203   |   591.17    |    3     |   220.92   |    0.0     |       3       | -         |
|   c204   |    590.6    |    3     |   184.66   |    0.0     |       3       | -         |
|   c205   |   588.88    |    3     |   159.18   |    0.0     |       3       | -         |
|   c206   |   588.49    |    3     |   163.95   |    0.0     |       3       | -         |
|   c207   |   588.29    |    3     |   214.53   |    0.0     |       3       | -         |
|   c208   |   588.32    |    3     |   214.09   |    0.0     |       3       | -         |
|   r101   |   1786.2    |    20    |   526.27   |    8.2     |      19       | 1+        |
|   r102   |   1508.45   |    18    |   532.83   |    1.5     |      17       | 1+        |
|   r103   |   1308.07   |    14    |   408.96   |    1.19    |      13       | 1+        |
|   r104   |   1048.6    |    10    |   291.01   |    4.1     |       9       | 1+        |
|   r105   |   1469.69   |    16    |   506.44   |    6.72    |      14       | 2+        |
|   r106   |   1298.03   |    14    |   372.89   |    3.67    |      12       | 2+        |
|   r107   |   1094.87   |    12    |   459.29   |   -0.89    |      10       | 2+        |
|   r108   |   971.33    |    10    |   389.65   |    1.09    |       9       | 1+        |
|   r109   |   1229.74   |    13    |   359.22   |    2.93    |      11       | 2+        |
|   r110   |   1154.57   |    13    |   355.29   |    3.19    |      10       | 3+        |
|   r111   |   1118.06   |    12    |   347.38   |    1.95    |      10       | 2+        |
|   r112   |   1016.61   |    11    |   378.37   |    3.51    |       9       | 2+        |
|   r201   |   1418.12   |    4     |   155.99   |   13.24    |       4       | -         |
|   r202   |   1181.78   |    4     |   286.03   |   -0.83    |       3       | 1+        |
|   r203   |   965.64    |    3     |   143.75   |    2.78    |       3       | -         |
|   r204   |   808.24    |    3     |   205.94   |   -2.09    |       2       | 1+        |
|   r205   |   1096.47   |    3     |   193.58   |   10.26    |       3       | -         |
|   r206   |   971.41    |    3     |   188.68   |    7.2     |       3       | -         |
|   r207   |   855.75    |    3     |   205.33   |   -3.91    |       2       | 1+        |
|   r208   |   751.65    |    3     |   199.97   |    3.42    |       2       | 1+        |
|   r209   |   944.05    |    3     |   204.19   |    3.84    |       3       | -         |
|   r210   |    981.4    |    3     |   193.37   |    4.47    |       3       | -         |
|   r211   |   773.93    |    3     |   169.29   |   -12.62   |       2       | 1+        |
|  rc101   |   1910.11   |    16    |   496.83   |   12.56    |      14       | 2+        |
|  rc102   |   1538.6    |    14    |   435.6    |   -1.04    |      12       | 2+        |
|  rc103   |   1360.85   |    12    |   302.3    |    7.86    |      11       | 1+        |
|  rc104   |   1180.07   |    11    |   362.36   |    3.93    |      10       | 1+        |
|  rc105   |   1589.62   |    15    |   449.76   |   -2.44    |      13       | 2+        |
|  rc106   |   1456.33   |    13    |   397.56   |    2.22    |      11       | 2+        |
|  rc107   |   1287.76   |    12    |   396.52   |    4.66    |      11       | 1+        |
|  rc108   |   1181.41   |    11    |   316.74   |    3.65    |      10       | 1+        |
|  rc201   |   1748.07   |    4     |   173.25   |   24.25    |       4       | -         |
|  rc202   |   1243.49   |    4     |   178.57   |   -8.94    |       3       | 1+        |
|  rc203   |   1017.26   |    4     |   218.8    |   -3.08    |       3       | 1+        |
|  rc204   |   839.81    |    3     |   217.62   |    5.18    |       3       | -         |
|  rc205   |   1345.96   |    4     |   174.59   |    3.72    |       4       | -         |
|  rc206   |   1128.82   |    4     |   175.55   |   -1.53    |       3       | 1+        |
|  rc207   |   1152.39   |    3     |   134.87   |    8.6     |       3       | -         |
|  rc208   |   982.53    |    3     |   215.82   |   18.64    |       3       | -         |
| **Avg.** | **1057.65** | **7.95** | **276.26** |  **3.28**  |   **7.23**    | -         |

We're conducting experiments on Gehring&Homberge dataset. The results are as follows:

Customer = 200, column indicate the average of all instances. 

| Inst  |   Obj   | #.Truck | CPU (s) | Gap to BKS | BKS #. Trucks | Note(#.T) |
| :---: | :-----: | :-----: | :-----: | :--------: | :-----------: | --------- |
|  C1   | 3020.75 |  19.7   | 1263.15 |    9.53    |     18.9      | 0.8+      |
|  C2   | 2021.50 |   6.8   | 644.37  |   10.46    |       6       | 0.8+      |
|  R1   | 4196.01 |  18.9   | 1359.25 |   16.01    |     18.2      | 0.7+      |
|  R2   | 3220.89 |   4.3   | 521.08  |   11.24    |       4       | 0.3+      |

Customer = 400 + , to be continued ... 


-----

## Report 

This repo incorporates some but not all features of SISRs and ALNS. We list them below.

**Destroy Operator:**

> 1. **Random Removal** ✅, Randomly remove some customers from current solution.
>
> 2. **String removal** ✅, including the string and split-string removal proposed in paper above. **The idea is to remove sufficient-enough, adjacent or geographically-close customers**, like multiple "strings", from current solution to produce new routes that are more likely to bring about improvement.

![](https://cdn.jsdelivr.net/gh/SmilingWayne/picsrepo/202502051156972.png)

> Source: SISRs paper.

**Repair (Recreate) Operator:**

> 1. **Greedy Insertion with Blink** ✅ : which is very similar to Greedy Insertion, yet before insertion, customers to be inserted are sorted with respect to random, demand, (distance) far, close, increasing time window length, increasing time window start, and decreasing time window end.

**NOTES:**

1. To check the feasibility efficiently during repair process, the **Forward Time Slack** is implemented. (See `Martin W. P. Savelsbergh, (1992) The Vehicle Routing Problem with Time Windows: Minimizing Route Duration. ORSA Journal on Computing 4(2):146-154. http://dx.doi.org/10.1287/ijoc.4.2.146`)
2. Several initial solution construction method are implemented. The C-W saving is adopted. Further experiment is required.
   1. Solomon's Time-oriented Nearest Neighbor, in 1987 ✅
   2. Naive Construction: each customer with a route. ✅
   3. Clark & Wright Saving Heuristic, 1964. ✅
3. **Fleet Minimization approach**: We don't strictly follow the fleet minimization procedure in TS paper. Currently, we just randomly remove an entire route from the solution and try to recreate a brand new solution. This is proved to be a little bit helpful yet still much room to improve. 
4. Simulated Annealing has **NOT** been implemented yet.
5. Adaptive Weight Adjustment, which is commonly used in ALNS, has **NOT** been implemented yet.
6. Some SOTA heuristic like [PyVRP package](https://pyvrp.readthedocs.io/en/latest/) are provided. You just need to call it.

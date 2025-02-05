# VRPTW-ALNS

This repo provides a ALNS meta-heuristic to solve VRPTW (Vehicle Routing Problem with Time Windows), which is NP-hard. We implement the SISRs (Slack Induction by String Removals) technique in `Jan Christiaens, Greet Vanden Berghe (2020) Slack Induction by String Removals for Vehicle Routing Problems. Transportation Science`, **which is proved to be a simple yet powerful heuristic for variants of VRP**. Experiments results can be found below.


## Numerical Experiments 

We provide a brief report of the numerical experiments. The results are obtained by running our code on Solomon benchmark instances. Column `Obj` indicates the objective value of our algorithm (which is measured by total distance), `#.T` shows the number of vehicles used in our solution, `CPU(s)` denotes the CPU time in seconds, `Gap BKS(%)` is the gap to the Best-Known Solution (BKS), `BKS #.T` is the number of vehicles used in the BKS, and `Note(#.T)` is the note, mainly the increase of vehicles compared with BKS. 

We may test our algorithm on more benchmarks in the future. As it's coded in pure Python, performance (running time) is somewhat terrible. We will try to fix that later.

|   Inst   |         Obj |  #.T  |  CPU (s)   | Gap BKS(%) | BKS #.T  | Note(#.T) |
| :------: | ----------: | :---: | :--------: | ---------: | :------: | :-------: |
|   c101   |      854.35 |  10   |   120.46   |       3.06 |    10    |     -     |
|   c102   |      873.41 |  10   |   278.12   |       5.36 |    10    |     -     |
|   c103   |      832.61 |  10   |   360.37   |       0.55 |    10    |     -     |
|   c104   |      850.58 |  10   |   365.68   |       3.13 |    10    |     -     |
|   c105   |      878.36 |  10   |   119.72   |       5.96 |    10    |     -     |
|   c106   |      852.95 |  10   |   265.51   |        2.9 |    10    |     -     |
|   c107   |     1013.19 |  10   |   111.53   |      22.23 |    10    |     -     |
|   c108   |      828.94 |  10   |   311.36   |    **0.0** |    10    |     -     |
|   c109   |      828.94 |  10   |   365.83   |    **0.0** |    10    |     -     |
|   c201   |      591.56 |   3   |   79.07    |    **0.0** |    3     |     -     |
|   c202   |      656.66 |   4   |   181.32   |       11.0 |    3     |    1+     |
|   c203   |      591.17 |   3   |   134.33   |    **0.0** |    3     |     -     |
|   c204   |       590.6 |   3   |   176.9    |    **0.0** |    3     |     -     |
|   c205   |      588.88 |   3   |   131.61   |    **0.0** |    3     |     -     |
|   c206   |      588.49 |   3   |   176.51   |    **0.0** |    3     |     -     |
|   c207   |      588.29 |   3   |   130.57   |    **0.0** |    3     |     -     |
|   c208   |      588.32 |   3   |   136.97   |    **0.0** |    3     |     -     |
|   r101   |     1831.64 |  21   |   613.32   |      10.96 |    19    |    2+     |
|   r102   |     1542.49 |  18   |   496.09   |       3.79 |    17    |    1+     |
|   r103   |     1272.14 |  15   |   440.21   |      -1.59 |    13    |    2+     |
|   r104   |      1048.6 |  10   |   291.01   |        4.1 |    9     |    1+     |
|   r105   |     1469.69 |  16   |   506.44   |       6.72 |    14    |    2+     |
|   r106   |     1298.03 |  14   |   372.89   |       3.67 |    12    |    2+     |
|   r107   |     1094.87 |  12   |   459.29   |      -0.89 |    10    |    2+     |
|   r108   |      971.33 |  10   |   389.65   |       1.09 |    9     |    1+     |
|   r109   |      1253.6 |  13   |   338.98   |       4.93 |    11    |    2+     |
|   r110   |     1156.89 |  13   |   301.6    |        3.4 |    10    |    3+     |
|   r111   |     1118.06 |  12   |   347.38   |       1.95 |    10    |    2+     |
|   r112   |     1049.93 |  11   |   349.69   |        6.9 |    9     |    2+     |
|   r201   |     1418.12 |   4   |   155.99   |      13.24 |    4     |     -     |
|   r202   |     1203.21 |   4   |   223.11   |       0.97 |    3     |    1+     |
|   r203   |      965.64 |   3   |   143.75   |       2.78 |    3     |     -     |
|   r204   |      840.37 |   3   |   150.66   |        1.8 |    2     |    1+     |
|   r205   |     1171.53 |   3   |   177.11   |      17.81 |    3     |     -     |
|   r206   |     1022.34 |   3   |   165.7    |      12.82 |    3     |     -     |
|   r207   |      873.05 |   3   |   134.61   |      -1.97 |    2     |    1+     |
|   r208   |      766.54 |   2   |   141.96   |       5.46 |    2     |     -     |
|   r209   |      975.94 |   3   |   175.48   |       7.34 |    3     |     -     |
|   r210   |      982.35 |   3   |   144.46   |       4.58 |    3     |     -     |
|   r211   |      773.93 |   3   |   169.29   |     -12.62 |    2     |    1+     |
|  rc101   |     1901.79 |  17   |   414.56   |      12.07 |    14    |    3+     |
|  rc102   |      1538.6 |  14   |   435.6    |      -1.04 |    12    |    2+     |
|  rc103   |     1360.85 |  12   |   302.3    |       7.86 |    11    |    1+     |
|  rc104   |     1212.34 |  11   |   389.07   |       6.77 |    10    |    1+     |
|  rc105   |     1589.62 |  15   |   449.76   |      -2.44 |    13    |    1+     |
|  rc106   |     1456.33 |  13   |   397.56   |       2.22 |    11    |    2+     |
|  rc107   |     1290.28 |  12   |   318.35   |       4.86 |    11    |    1+     |
|  rc108   |     1181.41 |  11   |   316.74   |       3.65 |    10    |    1+     |
|  rc201   |     1748.07 |   4   |   173.25   |      24.25 |    4     |     -     |
|  rc202   |     1282.28 |   4   |   177.51   |       -6.1 |    3     |    1+     |
|  rc203   |     1017.26 |   4   |   218.8    |      -3.08 |    3     |    1+     |
|  rc204   |      861.85 |   3   |   171.38   |       7.94 |    3     |     -     |
|  rc205   |     1345.96 |   4   |   174.59   |       3.72 |    4     |     -     |
|  rc206   |     1128.82 |   4   |   175.55   |      -1.53 |    3     |    1+     |
|  rc207   |     1152.39 |   3   |   134.87   |        8.6 |    3     |     -     |
|  rc208   |      961.49 |   3   |   141.27   |       16.1 |    3     |     -     |
| **Avg.** | **1066.55** | **8** | **259.39** |   **2.19** | **7.23** |     -     |

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
3. Fleet Minimization approach: currently just randomly remove an entire route from the solution and try to recreate a brand new solution. This is executed on first 20% iteration. This is proved to be a little bit helpful yet still much room to improve. 
4. Simulated Annealing is **NOT** implemented yet.
5. Adaptive Weight Adjustment, which is commonly used in ALNS, is **NOT** implemented yet.
6. Some SOTA heuristic like [PyVRP package](https://pyvrp.readthedocs.io/en/latest/) are provided. You just need to call it.
7. The split string removal, though implemented, seems not very powerful. We believe some bugs may hide, or some params are not correctly set.


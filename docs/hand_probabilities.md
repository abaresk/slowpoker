Hand Probabilities
==================

Hand rankings are determined by the probability of each hand being randomly selected. Less probable hands have higher rankings. 

There are `54 choose 5` = 3,162,510 ways to draw a hand from this deck.

## Joint Hand Probabilities
The rows pertain to matches among types of Pokémon. The columns pertain to matches among levels of Pokémon.

| Types \ Levels	| Flush	| Quadruple	| Full house	| Triple	| Two pair 	| Total	|
| ---	| ---	| ---	| ---	| ---	| ---	| ---	|
| **Full house**	| 0| 0| 0| 0| 918| **918**|
| **Flush**	| 0 | 0 | 0 | 7,344 | 14,688 | **22,032** |
| **Two pair** | 0 | 0 | 14,688 | 14,688 | 36,720 | **66,096** |
| **Pair** 	| 0 | 73,440 | 220,320 | 257,040 | 440,640 | **991,440** |
| **No pairs** | 25,704 | 257,040 | 514,080 | 514,080 | 771,120 | **2,082,024** |
| **Total** | **25,704** | **330,480** | **749,088** | **793,152** | **1,264,086** | ***3,162,510*** |

See [formulas](formulas.md) for more info.

## Ranking Probabilities
From the table above we get the following hand rankings:

| Hand 	| Frequency 	| Percent |
| --- | --- | --- |
| Full house (types) | 918 | 0.029% |
| Flush (types) | 22,032 | 0.697% | 
| Flush (level) | 25,704 | 0.813% | 
| Two pair (types) | 66,096 | 2.090% |
| Quadruple (level) | 330,480 | 10.450% |
| Full house (level) | 734,400 | 23.222% |
| Triple (level)| 771,120 | 24.383% |
| Two pair (level) | 1,211,760 | 38.316% |

# Final Hand Probabilities

The rankings above would apply if each player was only drawing hands and comparing them head-to-head. However, in this game, the hands duel and knock out cards in the opponent's hand, which changes the final probability distribution.

I was not able to calculate the probability of each hand formulaically, so the following table is based on random simulations.

| Hand | Percent (simulated) |
| --- | --- |
| Full house (types) | 0.0056% |
| Flush (level)<sup>1</sup> | 0.0952% |
| Flush (types)<sup>1</sup> | 0.316% |
| Two pair (types) | 0.491% |
| Quadruple (level)<sup>2</sup> | 1.84% |
| Full house (level)<sup>2</sup> | 1.79% |
| Two pair (level) | 7.86% |
| Triple (level) | 13.7% |
| Pair (level) | 42.9% |
| Highest level sum | 31.1% |

<sup>1</sup> Notice that these two are flipped compared to the drawing probabilities above.

<sup>2</sup> This is a little catch in the probabilities. Whichever of these two is ranked higher will be more probable than the other. But they are not very distant in likelihood.
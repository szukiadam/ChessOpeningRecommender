# Stockfish guide

> *"Given your replies to other's comments, you either don't understand that uci parameters are command-line options, or you don't know how to use uci parameters / protocol in commandline?"*

> *"If it is the later, this is a common question, which I will answer generically (to apply to any uci compatible chess engine), and at the end provide additional commands that are mostly exclusive to stockfish (which is in addition to standard uci protocol):"*

**Step 1**: Initiate your chess engine executable in command line (on mac/unix this is `./stockfish`)

**Step 2**: Type: `isready` (this step isn't necessary for stockfish, but some engines do (e.g. Discocheck and Quazar)

- Output: readyok

**Step 3**: Type '`uci`'

- The Output, should provide the engine ID, version number, and author information, followed by a list of ***all supported uci options***, such as Hash, Threads, MultiPV, Ponder, etc...
- This also shows you the default setting for each parameter
- The uci string always ends on a newline 'uciok'
- Sample output from stockfish 10 for reference: [here](https://imgur.com/a/tm4TTo0)

**Step 4**: How to change a ***supported*** UCI Option (Generic Formula)

`setoption name [supported uci option] value [value you want to change it to]`

e.g. to change hash size to 1024 MB and use 2 threads, type the following into commandline:

`setoption name hash value 1024`

`setoption name threads value 2`

`setoption name MultiPV value 3`

- Note: that the option name is case insensitive, so you could write instead : setoption name HaSh value 1024, and get the same results

**Step 5**: Set or change the position

1. How to set the Starting Position
    1. `position startpos`
2. How to Move (e.g. move pawn to e4 from starting position)
    1. `position startpos moves e2e4`
    2. Note that you must use uci notation (a variant of long algebraic notation) of moves which only includes the square it comes **from** and square it goes **to;**
    3. In order to castle kingside, you must use the notation *e1g1 (or e8g8),* to castle queenside : *e1c1 (e8c8)*
3. How to set a Position with a specific fen string
    1. `position fen [fen string here]`
        1. e.g. change position to this fen : 4kb1[r/p2rqppp](https://www.reddit.com/r/p2rqppp/)/5n2/1B2p1B1/4P3/1Q6/PPP2PPP/2K4R w k - 0 14
        2. `position fen rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2`
    2. How to make a move from a specific fen position (using above example)
        1. `position fen 4kb1r/p2rqppp/5n2/1B2p1B1/4P3/1Q6/PPP2PPP/2K4R w k - 0 14 moves h1d1`

**Step 6**: Search / Analysis... Type '`go`', followed by any number of commands:

1. infinite
2. depth [ply depth]
3. movetime [time in ms]
4. Note: there are other options available, but they really aren't useful without a gui (such as setting movestogo, winc, binc)
5. Example: `go depth 23 nnue multipv 5` 

***Stockfish Specific Commands*** (i.e. not portable to other uci engines)

1. Stockfish can display a diagram of the current position
    1. Type 'd' into command line
2. Stockfish can display a static eval (and breakdown of the position)
    1. Type 'eval' into command line
3. Benchmark Testing
    1. type 'bench'
4. PERFT
    1. type: 'go perft [ply depth]'

ALSO: Linux is faster, if you set it to use HugePages it's even faster. 

[Linux significantly stronger than Windows? · Issue #3135 · official-stockfish/Stockfish](https://github.com/official-stockfish/Stockfish/issues/3135)

## Large-scale Analysis of Chess Games with Chess Engines: A Preliminary Report

[](https://arxiv.org/pdf/1607.04186.pdf)

## ARTICLE ON NNUE

The [first part of this series](https://towardsdatascience.com/dissecting-stockfish-part-1-in-depth-look-at-a-chess-engine-7fddd1d83579) demonstrates how Stockfish abstracts a chess position and how it quickly finds every possible move. Now, the engine must *evaluate the quality of a move* in order to pick the best one.

In the past, Stockfish only relied on a set of fixed rules that are algorithmic translations of chess concepts: [tempo](https://en.wikipedia.org/wiki/Glossary_of_chess#tempo), [material](https://en.wikipedia.org/wiki/Glossary_of_chess#material), [space](https://en.wikipedia.org/wiki/Glossary_of_chess#space)… But in 2018, neural networks made their way into many chess engines and Stockfish [was outperformed](https://www.youtube.com/watch?v=wui0YweevtY). In order to fill the gap, Stockfish 12 integrated a neural network which took precedence over classical evaluation when the latter was known to be less performant, typically in balanced closed positions.

This article will focus first on the inner workings of the neural part and study the classical evaluation methods in a second time.

# **Neural network architecture**

The neural evaluation function is based on Yu Nasu’s NNUE architecture ([Efficiently Updatable Neural-Network-based Evaluation Functions for Computer Shogi, Yu Nasu, 2018](https://www.apply.computer-shogi.org/wcsc28/appeal/the_end_of_genesis_T.N.K.evolution_turbo_type_D/nnue.pdf)). This tiny neural network evaluates a game position on a CPU without the need of a graphic processor: Stockfish can still be integrated easily on a lot of devices and tweaked by its large base of contributors.

![https://miro.medium.com/max/700/1*cO7sTmBgiJcmDl-GHTvEPA.png](https://miro.medium.com/max/700/1*cO7sTmBgiJcmDl-GHTvEPA.png)

Architecture of NNUE, Image from [Roman Zhukov, Stockfish NN Release (NNUE), Talkchess](http://talkchess.com/forum3/viewtopic.php?f=2&t=74059&start=139)

## **Input encoding**

NNUE does not understand bitboards and the position has to be encoded first. The input parameters of NNUE represent the following boolean value, iterated for every W, X, Y and Z:*Is a king on a square X with a W[friendly|enemy] piece Y on square Z ?*

That makes up to 40,960 parameters. Using this binary encoding instead of a simple “*Is piece X on square Y?”* encoding (768 parameters) has several benefits:

- Updating the inputs and subsequent neurons after a change in a position is quicker because this encoding allows [incremental calculation](https://en.wikipedia.org/wiki/Incremental_computing), which is the strength of NNUE;
- Changing player’s turn is also quicker as the inputs simply need to be flipped;
- Providing more information than needed in the encoding is called overspecialization, and allows to input more knowledge to the network in order to decrease its training cost.

There are also a [few additional parameters](https://github.com/joergoster/Stockfish-NNUE/tree/master/src/eval/nnue/features) representing meta-game features, such as castling rights, previous pieces movements…

## **Hidden layers and training**

The goal of the network is to build an evaluation function which is a combination of the neurons from the different layers separated by non-linearities. This evaluation function will be optimized (training phase) in respect to the weight of its neurons, in order to output the most accurate evaluation when given known chess games.

The basic idea for NNUE’s training is to build a huge input dataset of randomly generated positions which are evaluated at a low depth with classical Stockfish. The network is trained using this dataset, and can be then fine-tuned using specific positions and evaluations. In itself, the network is simple as it is made of 3 fully connected layers plus an output layer which can be expressed as [material score](https://en.wikipedia.org/wiki/Chess_piece_relative_value).

However, what makes NNUE really unique are both its input encoding and its incremental calculation optimized for CPU evaluation.

![https://miro.medium.com/max/534/1*W2KvWkerw-T1Cwpp3K84kg.png](https://miro.medium.com/max/534/1*W2KvWkerw-T1Cwpp3K84kg.png)

NNUE: Heavy optimisation using SIMD intrinsics (nnue/layers/clipped_relu.h)

# **Classical Evaluation**

Apart from very balanced positions, Stockfish still relies on classical evaluation.

The idea is to build an *evaluation function as a combination of chess concepts*, made of several criterias which are weighted and added altogether. This function can then be scaled in order to express a material advantage in standard pawn units.

![https://miro.medium.com/max/700/1*REppiKnQmNDgG0-nlRF32A.png](https://miro.medium.com/max/700/1*REppiKnQmNDgG0-nlRF32A.png)

Classical evaluation in Stockfish, Image from Author

The concepts and associated criterias are the following:

- **Material imbalance**: count of pieces for every player
- **Positional advantage**: having specific pieces on specific squares
- **Material advantage**: strength of every piece, having a bishop pair
- **Strategical advantage for pawns**: doubled pawns, isolated pawns, connected pawns, pawns supported by pieces, attacked pawns
- **Strategical advantage for other pieces**: pieces blocked, pieces on good outposts, bishop X-ray attacks, bishops on long diagonals, trapped pieces, exposed queen, infiltrated queen, rooks on open files, rooks and queen batteries, enemy king attacked
- **Incoming threats**: attacked pieces, hanging pieces, king threats, pawn push threats, discovered/slider attack threats, squares where your pieces could move but would get exchanged, weakly protected pieces
- **Passed pawns**: blocked or unblocked passed pawns
- **Space**: squares controlled by all of your pieces
- **King safety**: attacked king, incoming checks, king in a ‘pieces shelter’, position of defenders

This huge resulting evaluation function is actually calculated up to the 2nd order, to compute a bonus/malus based on the known attacking/defending status of the players.

A lot of the pull requests in Stockfish GitHub repository consist of small changes in the weights of the aforementioned criterias, which lead to small ELO score improvements.

## **Tapered scaling**

The weighting of the different criterias are different whether we are still in the opening, middle-game or end-game. For instance, a passed pawn might get more valuable in the late-game than in the middle-game. Hence, Stockfish has two weighting sets for every criteria: one for the middle-game and one for the end-game. Stockfish then computes a *Phase factor* ranging from 0 (game finished) to 128 (game not started), which helps to interpolate the between two different weightings.

![https://miro.medium.com/max/700/1*qbqWFckzzWhFNomzxJd9Rg.png](https://miro.medium.com/max/700/1*qbqWFckzzWhFNomzxJd9Rg.png)

Tapered evaluation between Middle-game and End-game

The evaluation is then scaled again to fit the [fifty-move rule](https://en.wikipedia.org/wiki/Fifty-move_rule): as this rule is close to be reached, the evaluation comes closer to a draw.

## **Case study**

To clarify the classical evaluation approach, we will study a known position from a match between Kasparov and Topalov:

![https://miro.medium.com/max/391/1*AGfWCnYCGe4zOkqsyg-Tcw.png](https://miro.medium.com/max/391/1*AGfWCnYCGe4zOkqsyg-Tcw.png)

Kasparov — Topalov, Wijk aan Zee, 1999. 27: White to move

This example will focus on a positional advantage criteria: *having specific pieces on specific squares*. For every square of the board, a score is assigned depending on the piece that occupies this square (e.g. in the middle-game, the exposed black king on a5 is worth less than on g8 which is a safer square). This score bonus comes from two hardcoded square score tables: one for the pieces and one for the pawns. The reason for having two distinct score tables is that the score bonus for the pieces is symmetrical upon the vertical axis but not for the pawns *([psqt.cpp](https://github.com/official-stockfish/Stockfish/blob/2046d5da30b2cd505b69bddb40062b0d37b43bc7/src/psqt.cpp))*.

```
if (typeof(piece) == PAWN) {
   bonus += PBonus[rank][file];
}
else {
   file = file < 4 ? file : 8 - file;
   bonus += Bonus[piece][rank][file];
}
```

The score tables are the same for black and white as the [bitboard](https://towardsdatascience.com/dissecting-stockfish-part-1-in-depth-look-at-a-chess-engine-7fddd1d83579) just needs to be flipped to compute black’s score. For instance, the white queen on D4 is worth +8 in the middle-game and+24 in the end-game (as shown below) and would be the same than having a queen on D5 for black.

![https://miro.medium.com/max/700/1*NMlf1WCXSuSk2a5AtBaMFQ.png](https://miro.medium.com/max/700/1*NMlf1WCXSuSk2a5AtBaMFQ.png)

Piece square table bonus — Middle Game

![https://miro.medium.com/max/700/1*8dar3f5Pu9eRhMwWrp2ROQ.png](https://miro.medium.com/max/700/1*8dar3f5Pu9eRhMwWrp2ROQ.png)

Piece square table bonus — End Game

The piece-square score is summed for all of the pieces on the board and is calculated with both the middle-game and the end-game piece-square score table (see above). Then, the phase factor for tapered evaluation is computed based on the amount of non-pawn material on the board. Here, the phase factor is equal to 83. At last, the final bonus interpolated between the middle-game and end-game piece-square score is computed using this phase factor.

```
# MG: middle-game score
# EG: end-game score
# P: phase factorFINAL_BONUS = (MG * P + (EG * (P_MAX - P)) / (P_MAX-P_MIN))
```

The final score is +247 for white and +46 for black: from Stockfish point of view, this board leads to a clear positional advantage for white.

# **Conclusion**

The first part of this series presented how to read a position and how to generate candidate moves given this position. Now, this second part explained how to evaluate any given position in order to output a score for every player.

![https://miro.medium.com/max/1188/1*ibipG2Lr2fxqzAojAo1Knw.png](https://miro.medium.com/max/1188/1*ibipG2Lr2fxqzAojAo1Knw.png)

Stockfish concepts explained in the first two parts of this series

However, generating every possible combination of candidate moves and evaluating them at once is inconceivable performance-wise: the amount of candidates moves grow exponentially as we increase the depth of our search. Stockfish needs to select them wisely, which will be the topic for the next part of this series.

## Script

script.sh:

```bash
#!/usr/bin/expect

spawn ./stockfish

expect -timeout 1 Stockfish

send "uci \r"

expect -timeout 1 readyok

send "position fen r3k1r1/2q1bp2/2p4p/4p3/pp2Ppb1/3Q4/BPPR1PP1/4R1NK b q - 1 26 \r"

expect -timeout 1 readyok

send "go depth 23 \r"

expect -timeout 10 readyok

send "eval \r"

expect -timeout 1 readyok
```

find the first part of the eval function

```bash
expect script.sh | grep -i "|" out.txt | head -14| tr \| ' ' |
 tr 'King safety' 'KingSafety'  | awk -F' ' '{ print $1 $2 $3 $4 $5 $6 $7$8 $9 }' |
 grep -Eo '[+-]?[0-9]+([.][0-9]+)?' | tr \\n ',' | sed 's/.$//'
```

use `head -10` to get the first 10 lines only
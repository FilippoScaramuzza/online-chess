This project is part of an introductory Machine Learning course I took in my Bachelor's. It wasn't required, but I put a lot of effort in developing a web application where you could actually interact with a Machine Learning model instead of just visualizing some numbers and graphs. The game is online at <a href="https://filipposcaramuzza.dev/online-chess">filipposcaramuzza.dev/online-chess</a>.

I choose to develop this app mainly because I like chess, even if I'm veeery bad at it. You can search for my ELO rating on chess.com, very disappointing.

<center>
<img class="wp-image-213 aligncenter" src="https://filipposcaramuzza.dev/wp-content/uploads/2023/04/w23ZZTN-Imgur-1000x1024.jpg" alt="" width="432" height="443" />
<em>A photo of me carefully choosing the worst move ever made in chess.</em></center>If you want to play with it, just create a new game and after it is created tell the code to a friend of yours so that he can join your game. Or, if you want to play the computer, select an engine you want to play with and create a game with the computer.
<h2>State of the Art</h2>
I started the journey by looking at the current state of the art. Apparently there is a <a href="https://www.chessprogramming.org/Main_Page">whole branch</a> in Mathematics and Computer Science related to studies in Chess Engines. All seriously started in 1997, with the historical game Kasparov vs. DeepBlue.

Now, that a good amount of time since then has passed, these are the main ones currently worth studying:
<ul>
 	<li>Search (Minimax <a href="https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning">AlphaBeta pruning</a>)</li>
 	<li>Statistical Sampling (<a href="https://www.chessprogramming.org/Monte-Carlo_Tree_Search">Monte Carlo</a>)</li>
 	<li>Genetic Algorithms</li>
 	<li>Machine Learning</li>
</ul>
One of the most important one, is <a href="https://stockfishchess.org/">Stockfish</a>. It's open-source and mostly uses minmax search and, more recently, also neural networks.

But there's another guy in the town of chess engines, that also beat Stockfish. His name is AlphaZero, developed by DeepMind and it was the first one using Reinforcement Learning by playing against itself.

In this project, I choose an hybrid model, both using minmax and machine learning approaches.
<h2>The Platform - Technologies Used</h2>
You can find the platform ready-to-play at <a href="https://filipposcaramuzza.dev/online-chess">https://filipposcaramuzza.dev/online-chess</a>. Here below, the diagram of the architecture:

<img class="wp-image-223 aligncenter" src="https://filipposcaramuzza.dev/wp-content/uploads/2023/04/output-onlinepngtools-1024x549.png" alt="" width="514" height="276" />
<p style="text-align: center;"><em>On-Chess Architecture Diagram</em></p>
As you can see, I've used a ReactJS application as front-end. This was done mainly because I wanted to experiment more with ReactJS, and in second place because there are a lot of useful packages available with NodeJs, and I used one of those to draw the chess board and implement the game mechanics without re-inventing the wheel. The front-end is hosted for the moment on my personal website.

On the other hand, as a backend, I used Python, because it's the best when writing machine learning models. Here I designed the ML models and the Matches Manager, which role is to create, assign and delete ongoing matches. The back-end is hosted on <a href="https://render.com/">Render</a> as a Docker container.
<h2>First Engine Version</h2>
My first attempt was to use only search approaches, i.e. Minimax. Here there are several steps that the engine performs, in order to choose the best piece to move and the best cell to move it at:
<ol>
 	<li>Plain Minimax Algorithm</li>
 	<li>AlphaBeta Pruning</li>
 	<li>Quiescence Search</li>
 	<li>Evaluation</li>
</ol>
<h3>Plain Minimax Algorithm</h3>
Minimax is a decision rule used in artificial intelligence, decision theory, game theory, statistics, and philosophy for minimizing the possible loss for a worst case (maximum loss) scenario. In this case it's used to search for the <b>maximin value,</b> i.e. the highest value that the player can be sure to get without knowing the actions of the other players; equivalently, it is the lowest value the other players can force the player to receive when they know the player's action. See an example below.

Say, for example, that the black need to choose among three different moves. To each of these three moves, the white can respond with other three moves (of course this is a trivial example and actually not too realistic, but it's just to explain the core concepts). Now, with some metrics that we'll explain later, the white is evaluating the position for each of the possible moves he can make. Of course, he has to choose the worst for the black, that in the first case is the one evaluated with -6, in the second one is -9 and in the last one is two. Now, the black has to choose the move that leads the white to make the move that brings the position to an evaluation of -2, ensuring the best evaluation even on the best white move.

<img class="wp-image-218 aligncenter" src="https://filipposcaramuzza.dev/wp-content/uploads/2023/04/CDeiXV4-Imgur-1024x512.png" alt="" width="646" height="323" />
<p style="text-align: left;">This looks great! Now we only have to search every move until we reach the end of the game, the Check Mate! Of course this is utopian. Shannon discovered this in 1950: after both the players have moved 5 times, there are 69.352.859.712.417 possible games that have to be evaluated, and it's computationally unfeasible. So, how can we solve this?</p>

<h3>Alpha-Beta Pruning</h3>
<p style="text-align: left;">But now think about it. What can we assume when we analyse the first branch of the second one, evaluating the position with -8? It's already a better move for the one with respect to the first one, so we can discard the entire branch and skip to the next one:</p>
<img class=" wp-image-219 aligncenter" src="https://filipposcaramuzza.dev/wp-content/uploads/2023/04/wBYfthA-Imgur-1024x512.png" alt="" width="644" height="322" />
<h3>Quiescence Search</h3>
Now, after selecting some moves, we have to perform a further search. The goal is to evaluate only position where there are not winning moves to make, preferring quiescence positions. This is necessary to avoid the so-called <em>Horizon Effect</em>. The Horizon effect is caused by the depth limitation of the search algorithm and occurs when a negative event is inevitable but can be postponed. Since only a partial game tree has been parsed, it will appear to the system that the event can be avoided when in fact it is not.
<h3>Evaluation</h3>
The first step in understanding which player has the advantage in a given position is to evaluate the value of the pieces and to further improve improve the evaluation of, the positions in which the various pieces are strongest can be taken into account. For example pawns are valued 10, knights and bishops 30, rooks 50, queen 90 and the king is valued infinite, or a very big number. Then it's better to keep the king in safe position, maybe near to the player and the knight in the center of the chess board, and so on.
<h3>First Version Evaluation</h3>
This method had potential, but I was able to reach only a depth of 3, with 20 seconds to make the first moves at the start of the game, and 90 seconds in the mid game. We can do better.
<h2>Second Engine Version</h2>
This version implements a Machine Learning approach. To do so, of course, I had to choose a dataset. I opted for <a href="https://www.kaggle.com/datasets/liury123/chess-game-from-12-top-players">this one</a> from kaggle, i.e. more than 20.000 games from the 12 best player in the world with the .pgn format.

We then generated a dataset with this shape:
<ul>
 	<li>Columns a1, a2, a3, …, h6, h7, h8: state of the match</li>
 	<li>Columns from_a1, from_a2, ..., from_h7, from_h8: starting cell for the move (the right one is set to 1, the others to 0)</li>
 	<li>Columns to_a1, to_a2, ..., to_h7, to_h8: ending cell for the move (the right one is set to 1, the others to 0)</li>
 	<li>Column good_move: if it is a good, or a bad move, based on the match outcome.</li>
</ul>
But what now? This second engine version uses the ML algorithm to filter good moves among all the possible ones at each minimax iteration, allowing it to evaluate only a subset of the probably best moves. Given that we used a threshold on the probability for each move to be good one to make the filtering, we used to Decision Tree as it seemed the more "filtering" one.
<h3>Evaluation of the Second Version</h3>
Now we made some advancements. For example now the maximum depth reached is 6, and it takes only 1.5 second at the game start position and about 20 seconds in the mid game.
<h2>Final Considerations</h2>
This project was extremely fun to make and a very effective learning experience. Anyway, the final artificial intelligence I wrote is not so smart, and even if it's good in the openings, it lacks of foresight in the mid game, loosing almost most games. To at least be able to play chess when friends aren't available, I've added Stockfish 14 to the set of possible AI you can play with.

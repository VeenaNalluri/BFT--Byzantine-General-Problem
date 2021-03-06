***BFT Algorithm:*** 
In this assignment we are trying to solve the Byzantine general problem using ZMQ Req-Rep pattern communication
Lamport’s algorithm is a recursive definition, with a base case for m=0, and a recursive step for m > 0:
Algorithm OM(0)
1.	The general sends his value to every lieutenant.
2.	Each lieutenant uses the value he receives from the general.
Algorithm OM(m), m > 0
1.	The general sends his value to each lieutenant.
2.	For each i, let vi be the value lieutenant i receives from the general. Lieutenant i acts as the general in Algorithm OM(m-1) to send the value vito each of the n-2 other lieutenants.
3.	For each i, and each j≠i, let vi be the value lieutenant i received from lieutenant j in step 2 (using Algorithm (m-1)). Lieutenant i uses the value majority (v1, v2, … vn).<>

***Problem Description:***
This problem is built around an imaginary General who makes a decision to attack or retreat, and must communicate the decision to his lieutenants. A given number of these actors are traitors (possibly including the General.) Traitors cannot be relied upon to properly communicate orders; worse yet, they may actively alter messages in an attempt to subvert the process.

***Solution:*** If there are m faulty processors there should be atleast 3m+1 processors inorder to make a final decision. Hence in this assignment we have chosen 7 processors and 2 processors as faulty. 
If there are m faulty processors there should be m+1 rounds to get to a final decision. In this process we will consider the majority of the output of all the processors as the final decision.

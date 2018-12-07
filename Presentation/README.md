We have primarily considered the paper “Experiences with CoralCDN: A Five-Year Operational View”. But while implementing Coral CDN using Flask CDN library in python, same we observed that “.nyud.net/” was not available for most of the time and was unreliable for implementation and presenting the same. 

We then moved on to the paper “The Stellar Consensus Protocol: A Federated Model for Internet-level Consensus”. We could run a full validator node using stellar core. We have used horizon to access the stellar core and stellar base library in python. We created accounts in testnet that uses three open sourced validators and successfully made transactions across accounts using public keys of accounts.

All the team members have basic understanding of the both the papers, since the second was preferred for presentation a presentation and report were created for it. 
Both the Implementation code have been added to the repo.

Individual Contribution Details:

Sampath Lakkaraju (011818781): 
Understanding both the papers “The Stellar Consensus Protocol: A Federated Model for Internet-level Consensus” and “Experiences with CoralCDN: A Five-Year Operational View”
Detailed explanation of FBAS (stellar consensus):
Quorum, quorum slices, Tired FBAS, Safety, Liveness,Correct and Failed nodes. 
Assisted with implementation of stellar consensus.

Yudhajith Belagodu (012548354):
Understanding the concepts of the paper “Experiences with CoralCDN: A Five-Year Operational View”. Introduction to the Stellar Consensus Protocol including defining both the Stellar Consensus Protocol and the Federated Byzantine Agreement. Need for SCP, challenges to solve, Four-key properties of SCP. Comparing SCP with the other models like Proof of Work, and understanding the limitations of SCP.
Assisted with the code implementation.

Srinivasa Prasad Sunnapu (012526241):
Understanding the internals of SCP implementations, including Nomination Protocol and Ballot Protocol, and how they leverage Federated Voting mechanism to achieve consensus and recover from Struck States. Confirmed the understanding from the white paper with output of simple-fba simulator. 





 Abraham William (012551877)
Understanding both the papers “The Stellar Consensus Protocol: A Federated Model for Internet-level Consensus” and “Experiences with CoralCDN: A Five-Year Operational View”
Detailed explanation of FBAS (stellar consensus):Federated Voting in FBAS how they implement comsesus upholding liveliness and safeness of the quorum compared to centralised 
.Voting how fba achieves consensus through the stages of accepting,confirming and ratifying, to avoid bivalent Got the instincts from In google talks about this scp compared to proof of state and work .
 Gone through the projects in git hub sample - -https://github.com/spikeekips/simple-fba 


Surya Sonti (012535523)
Vrushali (012535055)
Understanding the goals that Federated Byzantine Agreements systems try to achieve. How can these goals be achieved irrespective of network. What are the factors affecting liveliness and safety. How can it be ensured that a system reaches consensus. Intersections and dispensable sets.  And their roles in ensuring that system achieves an agreement. 



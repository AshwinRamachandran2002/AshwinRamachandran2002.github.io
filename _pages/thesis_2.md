---
layout: page
title: (Thesis) Integrating Database with LLMs
permalink: /database-llm-thesis/
nav: true
nav_order: 7
horizontal: false
published: true
---
<!-- Thesis converted into a structure similar to the provided HTML -->
<section>
    <h2> Abstract</h2>
    <p>
    This research investigates the integration of Large Language Models (LLMs) with databases to enhance information extraction and query resolution accuracy. The study primarily focuses on
addressing challenges related to encoding methodologies and refining attention mechanisms within
LLMs. A key challenge involves individual encoding of data elements within large databases. Observations
reveal that attention sinks and position embeddings significantly influence accuracy. Leveraging in-
sights from recent advancements, particularly adapter layers inspired by Llama-Adapter, demonstrates
noteworthy improvements in the model’s performance.
Another critical aspect explored involves managing unlimited contextual information. Strategies
to approximate and rectify position information loss during encoding are discussed. Insights into
attention heads’ behavior in retrieving and promoting information from context guide the refinement
of model performance. Specifically, zeroing out attention heads in final layers has shown promising
results in ensuring accurate responses.
The study’s key contributions lie in proposing solutions to challenges related to individual encoding
and contextual information management. These findings pave the way for integration of LLMs with
databases, enabling more precise information extraction and query answering capabilities
    </p>
    </section>
  <section>
    <h2>Introduction</h2>
    <p>
      This study focuses on integrating Large Language Models (LLMs) with databases, aiming to extract information and answer queries accurately. Previous methodologies, such as fine-tuning frameworks and Retrieval Augmented Generation, have proven inadequate when dealing with vast datasets containing millions of entries. To ensure absolute precision, relying solely on summaries or excerpts is insufficient. Instead, leveraging the attention framework within transformers themselves becomes essential. This thesis aims to address two primary challenges in enabling LLMs to work with databases: performing generation with a large context and encoding each data element effectively. The experiments focus on decoder-only models, specifically Llama models.
    </p>
  </section>

  <section>
    <h2>Task</h2>
    <p>We try to observe and improve the recall ability of the model. Following are the descriptions of the data provided and queries posed.</p>

    <!-- Data subsection -->
    <section>
      <h4>Data</h4>
      <p>We employ a closed-world system’s data to ensure model does not depend on trained knowledge. We use a simple data, that is a extracted from knowledge corpus; two entities with or without a relation linking them. Table 1 shows some examples of the data. We refer to each data element as a "fact".</p>

      <!-- Table: Example Data -->
      <table>
        <caption>Table 1: Example Data</caption>
        <thead>
          <tr>
            <th>Format</th>
            <th>Fact</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Two Entities</td>
            <td>Williamson is baking</td>
          </tr>
          <tr>
            <td></td>
            <td>Oppenheimer is cycling</td>
          </tr>
          <tr>
            <td></td>
            <td>Sameer is Rope Climbing</td>
          </tr>
          <tr>
            <td>Two Entities and Relation</td>
            <td>Williamson is eating with Abhishek</td>
          </tr>
          <tr>
            <td></td>
            <td>Ashwin is affiliated to Chennai F.C.</td>
          </tr>
          <tr>
            <td></td>
            <td>Manara city is located in Sahar</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Queries subsection -->
    <section>
      <h4>Queries</h4>
      <p>Given one entity and a relation (if present), we expect the model to retrieve the associated entity. Table 2 shows
examples of the queries based on the data presented in Table 1</p>

      <!-- Table: Example Queries -->
      <table>
        <caption>Table 2: Example Queries</caption>
        <thead>
          <tr>
            <th>Fact</th>
            <th>Query</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Williamson is baking</td>
            <td>What is Williamson doing?</td>
          </tr>
          <tr>
            <td></td>
            <td>Who is baking?</td>
          </tr>
          <tr>
            <td>Oppenheimer is cycling</td>
            <td>What is Oppenheimer doing?</td>
          </tr>
          <tr>
            <td></td>
            <td>Who is cycling?</td>
          </tr>
          <tr>
            <td>Williamson is eating with Abhishek</td>
            <td>Who is cycling?</td>
          </tr>
          <tr>
            <td></td>
            <td>Who is eating with Abhishek?</td>
          </tr>
          <tr>
            <td>Ashwin is affiliated to Chennai F.C.</td>
            <td>Which organization is Ashwin affilated with?</td>
          </tr>
          <tr>
            <td></td>
            <td>Who is affiliated with Chennai F.C.?</td>
          </tr>
        </tbody>
      </table>
    </section>

  </section>
  <section>
    <h2>Individual Encoding</h2>
    <p>
    A database typically comprises a large number of tokens, while transformers have limitations regarding the context
window they can handle. Recent endeavors, such as those proposed in <a href="#cite-peng2023yarn">Peng et al., 2023</a>, have suggested methods to extend the
window by manipulating position embeddings (RoPE: <a href="#cite-su2023roformer">Su et al., 2023</a>). However, despite these approaches, sequential processing
of tokens still results in a quadratic inference time complexity. Additionally, encoding each fact independently, without
influence from other facts, is desired. Moreover, in the context of data updates, sequentially encoding facts would
necessitate re-encoding all facts with each new update, proving inefficient. Thus, the aim is to explore methods for
individual encoding
    </p>
    <section>
    <h4>Naive Approach</h4>
    <p>In this attempt, we obtain the hidden state representations of all the facts by processing them individually. During
generation, we allow the model to perform attention computation over these individually encoded hidden states and the preceding query hidden states. We noticed a poor accuracy. The model misassociated the entities in a fact with entities
in an another. Table 3 provides the responses to select queries.</p>
    <table>
        <caption>Table 3: Data: ["Williamson is baking", "Oppenheimer is cycling"]</caption>
        <thead>
          <tr>
            <th>Query</th>
            <th>Response</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>What is Williamson doing?</td>
            <td>baking</td>
          </tr>
          <tr>
            <td>What is Oppenheimer doing?</td>
            <td>baking</td>
          </tr>
          <tr>
            <td>Who is cycling?</td>
            <td>Oppenheimer</td>
          </tr>
          <tr>
            <td>Who is baking?</td>
            <td>Oppenheimer</td>
          </tr>
        </tbody>
      </table>
    </section>
<h1>Observations and Approaches</h1>

    <h2>Observations</h2>

    <h3>Need for Attention Sinks</h3>
    <p>Common first few tokens when encoding each fact improved the accuracy. These attention sinks are used by the model to determine the position encoded in the hidden states of the succeeding tokens. This was also observed in <a href="#cite-xiao2023efficient">Xiao et al., 2023</a>.</p>

    <h3>Behaviour of Position Embeddings</h3>
    <p>The RoPE plays a major role in the retrieval process. We noticed that the misassociation of the entities occurred only across facts that were encoded at the same "distance" from the attention sinks (This distance is measured in terms of number of facts present as context during encoding). The hidden states encode this relative position information from the attention sink provided by RoPE and depend upon this to find and retrieve associated tokens in the context.</p>

    <h2>Finetuning Approach</h2>
    <p>The recent Llama-Adapter paper <a href="#cite-gao2023llamaadapter">Gao et al., 2023</a> has achieved multimodal capabilities in LLMs. They do so by using an adapter to convert image representations to hidden state representations. Similarly, we transform the individually encoded hidden state representations of each fact through an adapter layer and provide them for attention computation during generation. We observed an improvement in the model’s answering pattern. Currently we are attempting to generalize the encoding
to accommodate an arbitrary number, N, of facts and analyze how the adapter layer improved the performance on the
task</p>

    <h2>Unlimited Context</h2>
    <p>Since there are a huge number of entries in the database, it is not possible to perform attention computation over all of them and hence some sort of selection has to be performed. This can be done before generation like Retrieval Augmented Generation. But we would then be potentially limiting or providing incorrect information since RAG is based on simple embedding similarity. Hence, we attempt to allow the model to retrieve from context at all stages of attention computation. We take inspiration from <a href="#cite-bertsch2023unlimiformer">Bertsch et al., 2023</a>.</p>

    <h3>What is present in the unlimited context?</h3>
    <p>We preprocess all the corpus data either individually or sequentially and save all the hidden states in the database. If we proceed to save all the key and value vectors of the corpus data instead, the space required would be very large. However, in decoder only models, this leads to a tradeoff in the accuracy of the retrieval process; the position embedding of all the hidden states in the database is taken as the same.</p>

    <p>RoPE is responsible for accounting for the distance between two tokens. It is multiplied to both query and key vectors before attention scores are computed. In the above method, since we are saving the hidden states and not the key vectors, the position information is lost and not saved. We observe some queries incorrectly answered due to this approximation.</p>

    <h3>Correcting the Approximation</h3>

    <h4>How do the attention heads work to retrieve from context?</h4>
    <p>We observe that only certain attention heads are concerned with retrieving and promoting information from context and the other heads are concerned with promoting information from its memory (trained data). This has also been observed by <a href="#cite-yu2023characterizing">Yu et al., 2023</a>. We confirm our findings by restricting all other attention heads to only the preceding query tokens; the response to any of the queries did not change. (We are attempting to use this information to detect hallucination, i.e., when these selected attention heads produce lower attention scores on the tokens in the context)</p>

    <p>Observing these selected attention heads, we study how they retrieve relevant tokens from context. During encoding, the position embeddings help encode in the hidden states of a token, the identity of the hidden states of the tokens near it (This has also been observed and studied in <a href="#cite-feng2023language">Feng et al., 2023</a>). Further, when a specific token is input, the selected heads locate similar tokens in the context and then retrieve tokens that are adjacent or associated with them.</p>

    <h4>Problem</h4>
    <p>Based on the above observation, we realized that the incorrect responses are due to heads in the final layers retrieving and promoting incorrect tokens. This has also been observed in <a href="#cite-halawi2023overthinking">Halawi et al., 2023</a>. Based on this study, we zero out the attention heads
in the final layers and notice an accurate response. We are currently attempting to verify the observations on differnt
types of data</p>

    <h2>References</h2>
    <ul>
        <li id="cite-peng2023yarn"><a href="https://arxiv.org/abs/2309.00071">Peng et al., (2023). YaRN: Efficient Context Window Extension of Large Language Models.</a></li>
        <li id="cite-su2023roformer"><a href="https://arxiv.org/abs/2309.00071">Su et al., (2023). RoFormer: Enhanced Transformer with Rotary Position Embedding.</a></li>
        <li id="cite-xiao2023efficient"><a href="https://arxiv.org/abs/2309.17453">Xiao et al., (2023). Efficient Streaming Language Models with Attention Sinks.</a></li>
        <li id="cite-gao2023llamaadapter"><a href="https://arxiv.org/abs/2304.15010">Gao et al., (2023). LLaMA-Adapter V2: Parameter-Efficient Visual Instruction Model.</a></li>
        <li id="cite-bertsch2023unlimiformer"><a href="https://arxiv.org/abs/2305.01625">Bertsch et al., (2023). Unlimiformer: Long-Range Transformers with Unlimited Length Input.</a></li>
        <li id="cite-yu2023characterizing"><a href="https://arxiv.org/abs/2310.15910">Yu et al., (2023). Characterizing Mechanisms for Factual Recall in Language Models.</a></li>
        <li id="cite-feng2023language"><a href="https://arxiv.org/abs/2310.17191">Feng et al., (2023). How do Language Models Bind Entities in Context?</a></li>
        <li id="cite-halawi2023overthinking"><a href="https://arxiv.org/abs/2307.09476">Halawi et al., (2023). Overthinking the Truth: Understanding how Language Models Process False Demonstrations.</a></li>
        <!-- Add more references in a similar format -->
    </ul>
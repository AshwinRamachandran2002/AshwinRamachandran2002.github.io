import dsp

openai_key = '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'
colbert_server = 'http://10.129.2.168:8893/api/search'
lm = dsp.GPT3(model='text-davinci-002', api_key=openai_key)
rm = dsp.ColBERTv2(url=colbert_server)

dsp.settings.configure(lm=lm, rm=rm)

train = []#(' Give reason PCl5 acts as an oxidising agent.', ["""In PCl5 oxidation state of P is +5. +5 is the highest oxidation state of P. Apart from +5, P also show oxidation state +3 and -3. +3 oxidation state of P is more stable as compare to +5, so PCl5 acts as oxidising agent and gets converted to PCl5 i.e P gets reduced from +5 to +3."""])]

train = [dsp.Example(question=question, answer=answer) for question, answer in train]

Question = dsp.Type(prefix="Question:", desc="${the question to be answered}")
Answer = dsp.Type(prefix="Answer:", desc="${a brief answer}", format=dsp.format_answers)

qa_template = dsp.Template(instructions="Answer questions with brief answers.", question=Question(), answer=Answer())

SearchRationale = dsp.Type(
    prefix="Rationale: Let's think step by step. To answer this question, we first need to find out",
    desc="${the missing information}"
)

SearchQuery = dsp.Type(
    prefix="Search Query:",
    desc="${a simple question for seeking the missing information}"
)

rewrite_template = dsp.Template(
    instructions="Write a search query that will help answer a complex question.",
    question=Question(), rationale=SearchRationale(), query=SearchQuery()
)

Context = dsp.Type(
    prefix="Context:\n",
    desc="${sources that may contain relevant content}",
    format=dsp.passages2text
)

CondenseRationale = dsp.Type(
    prefix="Rationale: Let's think step by step. Based on the context, we have learned the following.",
    desc="${information from the context that provides useful clues}"
)

hop_template = dsp.Template(
    instructions=rewrite_template.instructions,
    context=Context(), question=Question(), rationale=CondenseRationale(), query=SearchQuery()
)

Rationale = dsp.Type(
    prefix="Rationale: Let's think step by step.",
    desc="${a step-by-step deduction that identifies the correct response, which will be provided below}"
)

qa_template_with_CoT = dsp.Template(
    instructions=qa_template.instructions,
    context=Context(), question=Question(), rationale=Rationale(), answer=Answer()
)

@dsp.transformation
def QA_predict(example: dsp.Example, sc=True):
    if sc:
        example, completions = dsp.generate(qa_template_with_CoT, n=20, temperature=0.7)(example, stage='qa')
        completions = dsp.majority(completions)
    else:
        example, completions = dsp.generate(qa_template_with_CoT)(example, stage='qa')

    return example.copy(answer=completions.answer)


from dsp.utils import deduplicate

@dsp.transformation
def multihop_search_v1(example: dsp.Example, max_hops=2, k=2) -> dsp.Example:
    example.context = []

    for hop in range(max_hops):
        # Generate a query based
        template = rewrite_template if hop == 0 else hop_template
        example, completions = dsp.generate(template)(example, stage=f'h{hop}')

        # Retrieve k results based on the query generated
        passages = dsp.retrieve(completions.query, k=k)

        # Update the context by concatenating old and new passages
        example.context = deduplicate(example.context + passages)

    return example

@dsp.transformation
def multihop_attempt(d: dsp.Example) -> dsp.Example:
    # Prepare unaugmented demonstrations for the example.
    x = dsp.Example(question=d.question, demos=dsp.all_but(train, d))

    # Search. And skip examples where search fails.
    # Annotate demonstrations for multihop_search_v2 with the simpler multihop_search_v1 pipeline.
    x = multihop_search_v1(x)
    # if not dsp.passage_match(x.context, d.answer): return None

    # Predict. And skip examples where predict fails.
    x = QA_predict(x, sc=False)
    # if not dsp.answer_match(x.answer, d.answer): return None

    return d.copy(**x)

@dsp.transformation
def multihop_demonstrate(x: dsp.Example) -> dsp.Example:
    demos = dsp.sample(train, k=7)
    x.demos = dsp.annotate(multihop_attempt)(demos, k=3, return_all=True)
    return x



@dsp.transformation
def multihop_search_v2(example: dsp.Example, max_hops=2, k=2) -> dsp.Example:
    example.context = []

    for hop in range(max_hops):
        # Generate queries
        template = rewrite_template if hop == 0 else hop_template
        example, completions = dsp.generate(template, n=10, temperature=0.7)(example, stage=f'h{hop}')

        # Collect the queries and search with result fusion
        queries = [c.query for c in completions] + [example.question]
        example.context = dsp.retrieveEnsemble(queries, k=k)

        # Arrange the passages for the next hop
        if hop > 0:
            example.context = [completions[0].rationale] + example.context

    return example

def multihop_QA_v2(question: str) -> str:
    x = dsp.Example(question=question)
    x = multihop_demonstrate(x)
    x = multihop_search_v2(x)
    x = QA_predict(x)
    return x.answer


while True:
    question = input("Please enter a question to be answered, or x to exit\n")
    if question == "x":
        break
    dev = dsp.Example(question=question, answer="")
    print(multihop_QA_v2(dev.question))
    print(lm.inspect_history(n=3))

# dev = [('The glycosidic linkage involved in linking the glucose units in amylase part of starch is :', ['C1-C4']),]

# dev = [dsp.Example(question=question, answer=answer) for question, answer in dev]
#  Give reason Dinitrogen is chemically inert.
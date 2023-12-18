# LegalLLM
This is a uni project for Legal Advisory using Langchain. In this project we will research the capabilites of LLM via Langchain in the domain
of law. This can be interesting in getting exact information of question regarding specific law domain, i.e. environemnt ([Taxonmieverordnung](https://de.wikipedia.org/wiki/Verordnung_(EU)_2020/852_(Taxonomieverordnung))), "Einkommensteuergestetzt"([estg](https://www.gesetze-im-internet.de/estg/)) and more ...


## Project pre-proposal
In this section we will give a brief description of LegalLLM.

Tasks:
- [x] 1. What research problem you propose to investigate.
- [x] 2. What approach you intend to take, including how you expect to evaluate your results.
- [x] 3. What resources you’ve found so far that you think will help. These can be things like software packages, data sources, and scientific or technical literature.
- [x] 4. What your work plan is, including who will be responsible for what and what sort of timeline you expect to complete various tasks.


1. The objective of LegalLLM is to build a model, which can help lawers to ask questions regarding Environmental policy of the European Union, specifically EU taxonomie regulation ([Regulation (EU) 2020/852 of the European Parliament](https://de.wikipedia.org/wiki/Verordnung_(EU)_2020/852_(Taxonomieverordnung))).
Objective of the EU: -> **[The regulation obligates financial market participants, e.g. investment funds that wish to market a financial product as environmentally friendly, to report on the proportion of environmentally sustainable investments in their portfolio as defined by the regulation.[...] A standardized classification system or taxonomy within the EU should provide clarity as to which activities can be considered "sustainable"]([https://de.wikipedia.org/wiki/Verordnung_(EU)_2020/852_(Taxonomieverordnung))**
1. We leverage a LLM using Langchain via the vectorstores for building a Q/A system. Extract Relevant Text from the data and combine the specific question with the extracted text (Few-shot).
2. The LLM is using data/pdfs (PyPDF2) from the [regulation](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32020R0852) and for we will investiage appropiate [retrievers](https://python.langchain.com/docs/modules/data_connection/retrievers/) (MultiQueryRetriever, ....).
3. Build a tiny frontend to query the model.

## Project proposal




## Corpus
...


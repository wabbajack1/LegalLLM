# LegalLLM
This is a uni project for Legal Advisory using Langchain. In this project we will research the capabilities of LLM via Langchain in the domain
of law. This can be interesting for getting exact information of question regarding specific law domain, i.e. environment ([Taxonmieverordnung](https://de.wikipedia.org/wiki/Verordnung_(EU)_2020/852_(Taxonomieverordnung))), "Einkommensteuergestetzt"([estg](https://www.gesetze-im-internet.de/estg/)) and more.

## Project-Deadline: 31.01.2024
We need to submit:
 - project code
 - project report (5-10 pages)
 - a final presentation (10 minutes)

## Project pre-proposal
In this section we will give a brief description of LegalLLM.

Tasks:
1. [x] What research problem you propose to investigate.
2. [x] What approach you intend to take, including how you expect to evaluate your results.
3. [x] What resources you’ve found so far that you think will help. These can be things like software packages, data sources, and scientific or technical literature.
4. [x] What your work plan is, including who will be responsible for what and what sort of timeline you expect to complete various tasks.


1. The objective of LegalLLM is to build a model, which can help lawyers to ask questions regarding Environmental policy of the European Union, specifically EU taxonomie regulation ([Regulation (EU) 2020/852 of the European Parliament](https://de.wikipedia.org/wiki/Verordnung_(EU)_2020/852_(Taxonomieverordnung))).
Objective of the EU: -> **[The regulation obligates financial market participants, e.g. investment funds that wish to market a financial product as environmentally friendly, to report on the proportion of environmentally sustainable investments in their portfolio as defined by the regulation.[...] A standardized classification system or taxonomy within the EU should provide clarity as to which activities can be considered "sustainable"]([https://de.wikipedia.org/wiki/Verordnung_(EU)_2020/852_(Taxonomieverordnung))**
2. We leverage a LLM using Langchain via the vector-stores for building a Q/A system. Extract Relevant Text from the data and combine the specific question with the extracted text (Few-shot).
3. The LLM is using data/pdfs (PyPDF2) from the [regulation](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32020R0852) and for we will investigate appropriate [retrievers](https://python.langchain.com/docs/modules/data_connection/retrievers/) (MultiQueryRetriever, ....).
4. Build a tiny frontend to query the model.


## Project report
- **Deadline: 31.01.2024 (Project report presentations (10min) and submission of written project report)**
- **Length of Paper: 5 to 10 pages**

You can find the [overleaf document here](https://www.overleaf.com/7798534937fhhrqzhvpqqn#7d48ca)

## Ideas

### What is RAG?
- [Cookbook RAG](https://python.langchain.com/docs/expression_language/cookbook/retrieval)
- [Data connection](https://python.langchain.com/docs/modules/data_connection/)

### Which model to use?
- [Open source LLMs](https://github.com/jmorganca/ollama)

### In-Text Citing with Langchain
- [In-Text Citing with Langchain Question Answering](https://medium.com/@yotamabraham/in-text-citing-with-langchain-question-answering-e19a24d81e39)




## Open To-Dos
- [x] (S, J, K) Everybody understands what needs to be done
- [ ] (S) Crawler that fetches HTML files from the web (fetch all links within, go one level deeper) 
- [ ] (J) Import files into vector-store -> https://python.langchain.com/docs/modules/data_connection/document_loaders/html
- [ ] (K) Build lang chain -> logic how langchain would be used with the LLM (retriever), open source LLM API-key (optional or local), run LLM locally
- [ ] ...
- [ ] Improve results with Few-Shot-Learning (How to design the prompts)
- [ ] Serve lang chain via an API
- [ ] Frontend is build which allows querying
  - [ ] Frontend should also point to the part of the documents that hold the answers

## Corpus
...


# Search Engine for Text Document Retrieval

This project aims to develop a search engine for retrieving text documents based on user queries. The system allows users to enter their queries, and it represents relevant documents. The project is divided into three phases:

## Phase 1: Creating a Basic Information Retrieval Model

In this phase, the focus is on creating a simple information retrieval model. The documents need to be indexed to utilize the spatial index for retrieving relevant documents. The main tasks in this phase include:

- Data preprocessing
- Creating a spatial index
- Query processing and retrieval

Before building the spatial index, it's necessary to preprocess the texts. The required steps in this phase are:

- Token extraction
- Text normalization
- Stop-word removal
- Stemming

## Phase 2: Extending the Information Retrieval Model

In this phase, the goal is to extend the information retrieval model and represent documents as vectors to rank search results based on their relevance to the user's query. The steps involved in this phase are:

- Document modeling in the vector space
- Query representation in the vector space
- Calculating the similarity between the query vector and document vectors
- Ranking the search results based on similarity scores

The documents are represented using an tf-idf scheme. The formula is depicted below:

![tfidf Formula](https://github.com/shakibaam/Information-Retrieval-Project/blob/main/tfidf.png)

Then when user gives a query, extract the specific query vector (calculate the weights of query words). Then, using a similarity measure, attempt to find the documents that have the highest similarity (minimum distance) to the input query. Display the results in order of similarity. Various distance metrics can be considered for this task, with the simplest being cosine similarity, which calculates the angle between two vectors. The formula depucted below:


![cosine Formula](https://github.com/shakibaam/Information-Retrieval-Project/blob/main/cosine%20similarity.png)



## Phase 3: Machine learning applied in document retrieval

In this phase, the search engine developed in the previous phases is further enhanced. To handle large volumes of input documents, we employ clustering techniques to compare the query with a subset of documents within a cluster. Additionally, news categorization is implemented to map each news article to specific categories, allowing users to identify the news categories of search results.

### K-means

In this stage, the documents are clustered using the K-means clustering algorithm. Multiple runs of the algorithm can be performed, and the best clustering can be selected based on the RSS criterion.

### KNN

For document categorization, the k-nearest neighbors algorithm with different values of k is utilized. The category of a document is determined based on its nearest neighbors.




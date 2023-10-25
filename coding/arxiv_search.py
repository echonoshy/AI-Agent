# filename: arxiv_search.py

import arxiv

# Search for the latest papers on gpt-4
search = arxiv.Search(
  query = "gpt-4",
  max_results = 1,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

for result in search.results():
  print(f"Title: {result.title}")
  print(f"Authors: {result.authors}")
  print(f"Abstract: {result.summary}")
  print(f"Url: {result.pdf_url}")
Files with no links out of them
```dataview
TABLE file.inlinks
FROM ""
WHERE length(file.outlinks) = 0
  AND !contains(file.folder, "Meta")
  AND !contains(file.folder, "Decks")
SORT file.name ASC
```
